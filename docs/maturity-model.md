# Maturity Model (How Orgs Actually Adopt This)

This ladder is practical. Don’t skip rungs.

## Level 0 — Vibes (Default)
- No schemas, no traces, no gates
- “We test prompts sometimes”
**Result:** silent failures ship weekly

## Level 1 — Contract First
**Goal:** make outputs testable.
- Output schema (`GenericResponse.v1`)
- Contract suite in CI (schema + refusal + no secrets)
- “No Trace, No Ship” documented

**Exit criteria**
- PRs cannot merge if contract suite fails
- Every response includes `decision`

## Level 2 — Blood-to-Regression
**Goal:** incidents stop repeating.
- `incident → regression` workflow enforced
- Regression suite gates merges/releases

**Exit criteria**
- Every incident has a regression within 48 hours
- Regressions are non-flaky

## Level 3 — Realism (Scenario Suites)
**Goal:** test what users do, not toy prompts.
- Scenario suite (top workflows)
- Golden fixtures for retrieval/docs
- Constraint tests

**Exit criteria**
- Scenario suite runs nightly + trends are tracked

## Level 4 — Adversarial Reality
**Goal:** prove resistance to obvious attacks.
- Prompt injection suite (user + retrieval)
- PII bait and secret-leak suite
- Tool/action honesty enforced

**Exit criteria**
- Injection suite has near-zero false negatives

## Level 5 — Shift & Drift
**Goal:** tomorrow’s inputs don’t break you.
- Shift suite: missing/partial/stale/corrupt
- Drift dashboards: refusal rate, escalation rate, pass rate by risk

**Exit criteria**
- You catch regressions from drift before customers do

## Level 6 — Audit-Ready
**Goal:** compliance is a report, not a scramble.
- Standards mapping (EU AI Act / NIST AI RMF / ISO)
- Evidence retention policy
- Role ownership (who signs off on gates)

**Exit criteria**
- You can show traceability and test coverage to an auditor in 1 hour

## Level 7 — Continuous Assurance
**Goal:** evaluation is infrastructure.
- Canary evals in production
- Automated dataset refresh for scenarios
- Post-deploy regression replay (last N incidents)

**Exit criteria**
- Failures are caught in canaries before broad rollout
