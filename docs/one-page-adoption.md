# Ali’s Book of Fail — One‑Page Adoption Pitch (for Execs + Engineers)

## What it is
A **vendor‑agnostic**, **stack‑agnostic** evaluation standard for AI systems that:
- blocks unsafe or non‑auditable behavior in CI
- produces **diffable traces** (what it saw / used / did / decided)
- turns incidents into regressions (so failures don’t repeat)

## Why it exists
Most AI failures look like success:
- fluent answers with missing evidence
- action claims with no receipts
- retrieval/tool errors silently ignored
- prompt injections overriding policy

This playbook makes those failures **testable** and **blockable**.

## How it works
Three layers:

1) **Contracts (schemas)**
- outputs must match a schema
- decisions must be explicit (PASS / NEEDS_REVIEW / REFUSE)

2) **Hard Gates**
- secret leak patterns → FAIL
- claimed external actions without trace receipts → FAIL
- unsafe requests not refused → FAIL

3) **Suites**
- contract (breakage)
- regressions (lessons)
- scenarios (realism)
- adversarial (abuse)
- shift (degraded inputs)
- performance (latency/cost trends)

## Cost to adopt
**Minimum:** implement `POST /eval/run` in your system (one endpoint).  
**Or:** use No‑Stack Mode to standardize cases and governance now.

## What success looks like
- PRs are gated on contract + regressions
- every incident becomes a new test case within 48 hours
- traces are always present (“No Trace, No Ship”)
- drift is measured and caught before it hits users

## Bottom line
Reliable AI is not the system that answers the most.
It’s the system that knows when to **refuse**, **abstain**, or **escalate**—and can prove why.
