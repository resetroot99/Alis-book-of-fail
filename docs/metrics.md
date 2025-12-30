# Metrics That Matter (Not Vibes)

## Primary (ship blockers)
- Hard gate pass rate (must be 100% to ship)
- Regression pass rate (must be 100% to ship)
- Secret/PII leak rate (should be 0)
- Tool/action honesty violations (should be 0)

## Operational
- Refusal rate (by risk class)
- Escalation / NEEDS_REVIEW rate (by workflow)
- Failure rate by suite (contract/regression/adversarial/shift)

## Trend only (diagnostic)
- Latency p50/p95
- Cost per request (est.)
- Scenario “helpfulness” (only after gates pass)

## Publishable proof
- # cases by suite
- # regressions per incident
- example trace format
