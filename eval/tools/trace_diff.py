#!/usr/bin/env python3
"""
Trace Diff Viewer — Pretty-print trace comparison for demos/debugging.
Usage: python -m eval.tools.trace_diff <trace_file.json> [--baseline <baseline.json>]
"""
import argparse
import json
from pathlib import Path

# ANSI colors
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
MAGENTA = '\033[0;35m'
CYAN = '\033[0;36m'
BOLD = '\033[1m'
DIM = '\033[2m'
NC = '\033[0m'

def load_trace(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))

def verdict_color(v: str) -> str:
    if v == "PASS":
        return GREEN
    if v == "FAIL":
        return RED
    return YELLOW

def print_trace(trace: dict, title: str = "Trace") -> None:
    v = trace.get("verdict", "UNKNOWN")
    vc = verdict_color(v)
    
    print(f"\n{CYAN}╔{'═' * 74}╗{NC}")
    print(f"{CYAN}║{NC} {BOLD}{title}{NC}")
    print(f"{CYAN}╠{'═' * 74}╣{NC}")
    print(f"{CYAN}║{NC} {BOLD}case_id:{NC}        {trace.get('case_id', 'N/A'):<52} {CYAN}║{NC}")
    print(f"{CYAN}║{NC} {BOLD}verdict:{NC}        {vc}{v:<52}{NC} {CYAN}║{NC}")
    print(f"{CYAN}║{NC} {BOLD}run_id:{NC}         {trace.get('run_id', 'N/A'):<52} {CYAN}║{NC}")
    print(f"{CYAN}║{NC} {BOLD}timestamp:{NC}      {trace.get('timestamp', 'N/A'):<52} {CYAN}║{NC}")
    print(f"{CYAN}╟{'─' * 74}╢{NC}")
    
    # Inputs
    inputs = trace.get("inputs", {})
    print(f"{CYAN}║{NC} {BOLD}inputs:{NC}")
    for k, v in inputs.items():
        val = str(v)[:60] + "..." if len(str(v)) > 60 else str(v)
        print(f"{CYAN}║{NC}   {DIM}{k}:{NC} {val}")
    
    # Actions
    actions = trace.get("actions", [])
    print(f"{CYAN}╟{'─' * 74}╢{NC}")
    print(f"{CYAN}║{NC} {BOLD}actions:{NC} ", end="")
    if not actions:
        print(f"{YELLOW}[] (empty){NC}")
    else:
        print(f"{GREEN}{len(actions)} action(s){NC}")
        for i, a in enumerate(actions):
            print(f"{CYAN}║{NC}   [{i}] {a.get('type', 'unknown')}: {a.get('status', 'N/A')}")
    
    # Outputs
    outputs = trace.get("outputs", {})
    print(f"{CYAN}╟{'─' * 74}╢{NC}")
    print(f"{CYAN}║{NC} {BOLD}outputs:{NC}")
    decision = outputs.get("decision", "N/A")
    dec_color = GREEN if decision == "PASS" else (RED if decision == "REFUSE" else YELLOW)
    print(f"{CYAN}║{NC}   {BOLD}decision:{NC} {dec_color}{decision}{NC}")
    
    final_text = outputs.get("final_text", "")
    if final_text:
        # Truncate for display
        lines = final_text.split("\n")[:3]
        print(f"{CYAN}║{NC}   {BOLD}final_text:{NC}")
        for line in lines:
            truncated = line[:65] + "..." if len(line) > 65 else line
            print(f"{CYAN}║{NC}     {DIM}{truncated}{NC}")
        if len(final_text.split("\n")) > 3:
            print(f"{CYAN}║{NC}     {DIM}... (truncated){NC}")
    
    # Gate failures
    policy = trace.get("policy", {})
    gate_failures = policy.get("gate_failures", [])
    if gate_failures:
        print(f"{CYAN}╟{'─' * 74}╢{NC}")
        print(f"{CYAN}║{NC} {BOLD}{RED}gate_failures:{NC}")
        for gf in gate_failures:
            print(f"{CYAN}║{NC}   {RED}✗{NC} {gf}")
    
    # Scores
    scores = trace.get("scores", {})
    if scores:
        print(f"{CYAN}╟{'─' * 74}╢{NC}")
        print(f"{CYAN}║{NC} {BOLD}scores:{NC}")
        for k, v in scores.items():
            score_color = GREEN if v >= 0.85 else (YELLOW if v >= 0.5 else RED)
            print(f"{CYAN}║{NC}   {k}: {score_color}{v:.2f}{NC}")
    
    print(f"{CYAN}╚{'═' * 74}╝{NC}")

def print_diff(actual: dict, baseline: dict) -> None:
    print(f"\n{MAGENTA}{'═' * 76}{NC}")
    print(f"{MAGENTA}  TRACE DIFF: {baseline.get('case_id', 'baseline')} → {actual.get('case_id', 'actual')}{NC}")
    print(f"{MAGENTA}{'═' * 76}{NC}\n")
    
    # Verdict diff
    bv, av = baseline.get("verdict"), actual.get("verdict")
    if bv != av:
        print(f"  {BOLD}verdict:{NC}")
        print(f"    {RED}- {bv}{NC}")
        print(f"    {GREEN}+ {av}{NC}")
        print()
    
    # Actions diff
    ba, aa = baseline.get("actions", []), actual.get("actions", [])
    if len(ba) != len(aa):
        print(f"  {BOLD}actions:{NC}")
        print(f"    {RED}- {len(ba)} action(s){NC}")
        print(f"    {GREEN}+ {len(aa)} action(s){NC}")
        print()
    
    # Gate failures diff
    bgf = baseline.get("policy", {}).get("gate_failures", [])
    agf = actual.get("policy", {}).get("gate_failures", [])
    if set(bgf) != set(agf):
        print(f"  {BOLD}gate_failures:{NC}")
        for gf in set(bgf) - set(agf):
            print(f"    {RED}- {gf}{NC}")
        for gf in set(agf) - set(bgf):
            print(f"    {GREEN}+ {gf}{NC}")
        print()
    
    # Outputs diff
    bo, ao = baseline.get("outputs", {}), actual.get("outputs", {})
    if bo.get("decision") != ao.get("decision"):
        print(f"  {BOLD}outputs.decision:{NC}")
        print(f"    {RED}- {bo.get('decision')}{NC}")
        print(f"    {GREEN}+ {ao.get('decision')}{NC}")

def main():
    parser = argparse.ArgumentParser(description="Trace Diff Viewer")
    parser.add_argument("trace", help="Path to trace JSON file")
    parser.add_argument("--baseline", "-b", help="Path to baseline trace for diff")
    parser.add_argument("--json", "-j", action="store_true", help="Output raw JSON")
    args = parser.parse_args()
    
    trace = load_trace(args.trace)
    
    if args.json:
        print(json.dumps(trace, indent=2))
        return
    
    if args.baseline:
        baseline = load_trace(args.baseline)
        print_trace(baseline, "Baseline Trace")
        print_trace(trace, "Actual Trace")
        print_diff(trace, baseline)
    else:
        print_trace(trace, "Trace Details")

if __name__ == "__main__":
    main()
