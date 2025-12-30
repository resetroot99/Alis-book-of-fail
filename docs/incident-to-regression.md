# Incident → Regression Loop (The Only Governance That Works)

When something breaks in production, your job is not to write a postmortem.
Your job is to make sure it **never breaks that way again**.

## Required artifacts (within 48 hours)
1) **Trace** (what happened)
2) **Failure label(s)** from `docs/failure_taxonomy.md`
3) **New regression case** in `eval/cases/regressions/`
4) **Gate update** if it should block all future releases

## Template workflow
- Open an incident ticket
- Attach the trace JSON (or sanitized subset)
- Tag failures (e.g., PARTIAL_EVIDENCE_GUESS + TOOL_HALLUCINATION)
- Add a regression YAML reproducing the failure
- Fix system
- Confirm: case fails before fix, passes after fix
- Merge with CI gate on regressions

## Why this matters
AI breaks in *new* ways every week.
Without regressions, you will re-learn the same lesson forever.

## Definition of “done”
An incident is not resolved until:
- a regression exists
- CI blocks the old behavior
- you can prove it with traces
