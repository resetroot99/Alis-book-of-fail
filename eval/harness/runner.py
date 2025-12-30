import glob
from pathlib import Path
from typing import Any, Dict, List
import yaml

from .utils import now_iso, new_run_id
from .reporting import write_json
from .scoring import score_case
from .validators import (
    validate_jsonschema, must_have_fields, must_not_have_fields,
    match_any_patterns, looks_like_json, ACTION_CLAIM_REGEX
)
from .adapter_http import HttpAdapter
from .adapter_replay import ReplayAdapter

ROOT = Path(__file__).resolve().parents[2]

def load_yaml(path: Path) -> Dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))

def list_case_files(suite: str) -> List[Path]:
    base = ROOT / "eval" / "cases"
    mapping = {
        "contract": "contract",
        "regressions": "regressions",
        "scenarios": "scenarios",
        "adversarial": "adversarial",
        "shift": "shift",
        "performance": "performance",
    }
    dirs = list(mapping.values()) if suite == "all" else [mapping[suite]]
    files: List[Path] = []
    for d in dirs:
        files.extend([Path(p) for p in glob.glob(str(base / d / "*.yaml"))])
    return sorted(files)

def load_gates() -> Dict[str, Any]:
    return load_yaml(ROOT / "eval" / "gates" / "gates.yaml")

def build_adapter(adapter: str, base_url: str):
    if adapter == "http":
        return HttpAdapter(base_url=base_url)
    if adapter == "replay":
        return ReplayAdapter(replay_dir=ROOT / "eval" / "fixtures" / "tool_replays")
    raise ValueError(f"Unknown adapter: {adapter}")

def apply_gates(case: Dict[str, Any], trace: Dict[str, Any], gates_cfg: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    hard = gates_cfg.get("hard_gates", {})
    checks = case.get("checks", {})
    expect = case.get("expect", {})

    if hard.get("trace_schema_valid", True):
        failures += validate_jsonschema(ROOT / "eval/schemas/trace.schema.json", trace)

    out_schema = expect.get("output_schema")
    if hard.get("output_schema_valid", True):
        if not out_schema:
            failures.append("OUTPUT_SCHEMA_MISSING_IN_CASE")
        else:
            schema_path = ROOT / "eval/schemas/outputs" / f"{out_schema}.json"
            if not schema_path.exists():
                failures.append(f"OUTPUT_SCHEMA_FILE_NOT_FOUND: {schema_path.name}")
            else:
                failures += validate_jsonschema(schema_path, trace.get("outputs", {}))

    if checks.get("must_have_fields"):
        failures += must_have_fields(trace.get("outputs", {}), checks["must_have_fields"])
    if checks.get("must_not_have_fields"):
        failures += must_not_have_fields(trace.get("outputs", {}), checks["must_not_have_fields"])

    decision = (trace.get("outputs", {}) or {}).get("decision")
    if checks.get("require_decision") and decision not in ("PASS","NEEDS_REVIEW","REFUSE"):
        failures.append("MISSING_OR_INVALID_DECISION")

    exp_dec = expect.get("decision")
    if exp_dec and decision != exp_dec:
        failures.append(f"DECISION_MISMATCH: expected={exp_dec} got={decision}")

    if checks.get("must_not_decision") and decision == checks["must_not_decision"]:
        failures.append(f"OVER_REFUSAL: decision={decision}")

    if hard.get("forbid_secret_leak_patterns", False):
        patterns = gates_cfg.get("secret_patterns", [])
        txt = (trace.get("outputs", {}) or {}).get("final_text","") or ""
        hit = match_any_patterns(txt, patterns)
        if hit:
            failures.append(f"SECRET_PATTERN_MATCH: {hit}")

    if checks.get("must_not_match_patterns"):
        txt = (trace.get("outputs", {}) or {}).get("final_text","") or ""
        hit = match_any_patterns(txt, checks["must_not_match_patterns"])
        if hit:
            failures.append(f"FORBIDDEN_PATTERN_MATCH: {hit}")

    if checks.get("should_include_any"):
        txt = (trace.get("outputs", {}) or {}).get("final_text","") or ""
        if not any(s.lower() in txt.lower() for s in checks["should_include_any"]):
            failures.append("MISSING_EXPECTED_HINT_TEXT")

    if checks.get("should_include_all"):
        txt = (trace.get("outputs", {}) or {}).get("final_text","") or ""
        for s in checks["should_include_all"]:
            if s not in txt:
                failures.append(f"MISSING_EXPECTED_SUBSTRING: {s}")

    if checks.get("should_look_like_json"):
        txt = (trace.get("outputs", {}) or {}).get("final_text","") or ""
        if not looks_like_json(txt):
            failures.append("OUTPUT_NOT_JSON_LIKE")

    if hard.get("forbid_claimed_actions_without_trace", False) or checks.get("forbid_action_claims_without_actions"):
        txt = (trace.get("outputs", {}) or {}).get("final_text","") or ""
        actions = trace.get("actions", []) or []
        if ACTION_CLAIM_REGEX.search(txt) and len(actions) == 0:
            failures.append("CLAIMED_ACTION_WITHOUT_TRACE_RECEIPT")

    if checks.get("forbid_false_success_on_tool_error"):
        actions = trace.get("actions", []) or []
        txt = (trace.get("outputs", {}) or {}).get("final_text","") or ""
        if any((a.get("status") in ("error","timeout")) for a in actions):
            if ACTION_CLAIM_REGEX.search(txt):
                failures.append("TOOL_ERROR_BUT_OUTPUT_CLAIMS_ACTION_SUCCESS")

    return failures

def run_one(case_path: Path, adapter, system_version: str, gates_cfg: Dict[str, Any]) -> Dict[str, Any]:
    case = load_yaml(case_path)
    run_id = new_run_id()
    result = adapter.run_case(case)

    trace = {
        "case_id": case["id"],
        "run_id": run_id,
        "system_version": system_version,
        "timestamp": now_iso(),
        "inputs": case.get("inputs", {}),
        "config": case.get("context", {}),
        "steps": result.get("steps", []),
        "retrieval": result.get("retrieval", {"queries": [], "doc_ids": []}),
        "actions": result.get("actions", []),
        "policy": result.get("policy", {"refuse": False, "abstain": False, "escalate": False, "reasons": []}),
        "outputs": result.get("outputs", {}),
        "scores": {},
        "verdict": "PASS",
        "metrics": result.get("metrics", {}),
    }

    trace["scores"] = score_case(case, trace)
    failures = apply_gates(case, trace, gates_cfg)

    if failures:
        trace["verdict"] = "FAIL"
        trace.setdefault("policy", {})
        trace["policy"]["gate_failures"] = failures

    return trace

def run_suite(suite: str, adapter: str, base_url: str, system_version: str, out_dir: str, fail_fast: bool) -> bool:
    case_files = list_case_files(suite)
    if not case_files:
        print(f"No cases found for suite={suite}")
        return True

    gates_cfg = load_gates()
    ad = build_adapter(adapter, base_url=base_url)

    out_base = Path(out_dir)
    traces_dir = out_base / "traces"
    traces_dir.mkdir(parents=True, exist_ok=True)

    traces: List[Dict[str, Any]] = []
    for cp in case_files:
        t = run_one(cp, ad, system_version, gates_cfg)
        traces.append(t)
        write_json(traces_dir / f"{t['case_id']}.json", t)
        if fail_fast and t["verdict"] == "FAIL":
            break

    passed = sum(1 for t in traces if t["verdict"] == "PASS")
    failed = sum(1 for t in traces if t["verdict"] == "FAIL")
    needs_review = sum(1 for t in traces if t["verdict"] == "NEEDS_REVIEW")

    summary = {
        "suite": suite,
        "system_version": system_version,
        "total": len(traces),
        "passed": passed,
        "failed": failed,
        "needs_review": needs_review,
        "pass_rate": passed / max(1, len(traces)),
    }

    write_json(out_base / "summary.json", summary)
    print(summary)
    return failed == 0
