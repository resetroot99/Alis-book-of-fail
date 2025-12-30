# Governance Roles (Who Owns What)

This prevents the classic failure: “Everyone owns eval” → nobody does.

## Required roles (small org version)
- **Eval Owner**: gates, suites, CI rules, drift review
- **Product Owner**: scenario coverage for top workflows
- **Security Owner**: adversarial suite, secret/PII leak gates
- **Data Owner**: retrieval fixtures, dataset refresh cadence

## Decision rights
- Hard gates: security + eval owner sign-off
- Regression additions: eval owner sign-off
- Scenario updates: product owner sign-off

## Cadence
- Weekly: drift review + new incidents
- Monthly: refresh injection patterns + scenario fixtures
- Quarterly: re-audit gates vs new capabilities
