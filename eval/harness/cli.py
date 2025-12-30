import argparse
from .runner import run_suite

def main():
    p = argparse.ArgumentParser(description="Ali's Book of Fail — Eval Harness")
    p.add_argument("--base-url", default=None, help="HTTP base URL for system under test (SUT)")
    p.add_argument("--adapter", default="http", choices=["http", "replay"])
    p.add_argument("--suite", default="contract", choices=["contract","regressions","scenarios","adversarial","shift","performance","all"])
    p.add_argument("--system-version", default="dev")
    p.add_argument("--out", default="eval/reports/latest")
    p.add_argument("--fail-fast", action="store_true")
    args = p.parse_args()

    ok = run_suite(
        suite=args.suite,
        adapter=args.adapter,
        base_url=args.base_url,
        system_version=args.system_version,
        out_dir=args.out,
        fail_fast=args.fail_fast,
    )
    raise SystemExit(0 if ok else 1)

if __name__ == "__main__":
    main()
