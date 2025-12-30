---
name: New Failure Case
about: Propose a new test case for a failure mode
title: "[CASE] "
labels: new-case
assignees: ''
---

## Failure Mode

What type of AI failure does this case catch?

**Taxonomy label** (if existing): `CONFIDENT_NONSENSE`, `PROMPT_INJECTION_SUCCESS`, etc.
**Or describe new failure type:** ...

## The Scenario

Describe the situation:

- **User intent:** What is the user trying to do?
- **System context:** What should the system know?
- **Input:** What does the user/system provide?
- **Failure:** How does the system fail?

## Expected Behavior

What should a well-behaved system do instead?

- [ ] Refuse
- [ ] Abstain with explanation
- [ ] Escalate to human
- [ ] Answer with qualification
- [ ] Other: ...

## Why This Matters

Real-world impact of this failure mode. Examples welcome (anonymized).

## Suggested Suite

Where should this case live?

- [ ] `adversarial` — injection, abuse
- [ ] `contract` — schema, refusal, secrets
- [ ] `regressions` — learned from incidents
- [ ] `scenarios` — realistic workflows
- [ ] `shift` — degraded/partial inputs
- [ ] `performance` — latency, cost

## Draft Case (Optional)

If you have a draft YAML, include it:

```yaml
id: ...
suite: ...
inputs:
  user: "..."
expected_decision: FAIL
failure_labels: [...]
```

---

**Quality checklist:**

- [ ] This tests a specific failure mode, not general quality
- [ ] The expected behavior is unambiguous
- [ ] This isn't vendor-specific
- [ ] I've checked existing cases for overlap
