"""Generate a starter case pack quickly.

Usage:
  python -m eval.tools.generate_case_pack --out eval/cases/scenarios/pack_generated

Produces YAML cases you can edit. No model required.
"""
import argparse
from pathlib import Path
import yaml
import random

def write_case(out_dir: Path, case: dict):
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"{case['id']}.yaml").write_text(yaml.safe_dump(case, sort_keys=False), encoding="utf-8")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--n", type=int, default=25)
    args = ap.parse_args()

    prompts = [
        ("summarize", "Summarize the attached text in 5 bullets."),
        ("extract", "Extract JSON with keys: a, b, c from: a=1 b=2 c=3"),
        ("plan", "Give a 7-step plan to migrate a service to Kubernetes."),
        ("support", "Draft a support response asking 3 clarifying questions."),
        ("rag_qa", "Answer using sources: what is X?"),
    ]

    for i in range(args.n):
        mode, p = random.choice(prompts)
        cid = f"GEN_{i:04d}_{mode}"
        case = {
            "id": cid,
            "type": "scenario",
            "risk": "low",
            "description": "Generated starter scenario (edit to match your domain).",

            "inputs": {"user": p},
            "context": {"mode": mode},
            "expect": {"output_schema": "GenericResponse.v1"},
            "checks": {"schema_validation": True},
            "scoring": {"min_overall": 0.7},
        }
        write_case(Path(args.out), case)

if __name__ == "__main__":
    main()
