# No-Stack Mode (Use This Playbook Without Building Any System)

You don't need an app stack to use **Ali’s Book of Fail**.

In **No-Stack Mode**, this repo is a **standard format** for:
- writing AI evaluation requirements as executable cases
- defining **hard gates** (what must never ship)
- producing **audit-ready traces** (what happened, and why)

Think of it like a *unit-test spec* for AI behavior.

---

## What you can do immediately (today)

### 1) Write your org’s “Non‑Negotiables”
Pick 10–20 from `docs/failure_taxonomy.md`, then convert them into **hard gates**:
- No secret leakage
- No action claims without receipts
- No “confident answer” under missing evidence (→ NEEDS_REVIEW)
- No prompt-injection compliance
- No conflict-ignorance (→ NEEDS_REVIEW)

Record the gates in:
- `eval/gates/gates.yaml`

### 2) Author cases (YAML)
Cases live in `eval/cases/*`.

Start with:
- `contract/` (schemas + safety invariants)
- `regressions/` (your known failures)
- `adversarial/` (injection, poisoning, bait)
- `shift/` (missing/corrupt/stale inputs)

A case is useful if it contains:
- **inputs** (the request)
- **fixtures** (docs/attachments/tools) *if relevant*
- **expectations** (required decision class and/or schema)
- **checks** (must/should assertions)

### 3) Run the harness in replay mode (no system required)
```bash
pip install -e .
book-of-fail --adapter replay --suite all
```

Replay mode produces traces and a summary under:
- `eval/reports/latest/`

These traces become:
- examples for documentation
- your “standard trace format”
- artifacts you can publish to prove seriousness

### 4) Use the repo as a standard in reviews
Even without a product:
- review new cases like code
- version them
- require PR gates to pass in CI

---

## When you eventually have a system
Any team can integrate by implementing:

`POST /eval/run` (see `docs/adoption.md`)

No other coupling required.

---

## The No‑Stack Deliverable Checklist
If you publish this repo as a playbook, make sure it includes:

- [ ] doctrine (Oath + chapters)
- [ ] failure taxonomy
- [ ] gates.yaml with defaults + explainers
- [ ] case templates + authoring checklist
- [ ] 50+ starter cases across common AI product types
- [ ] PR CI gate
- [ ] “incident → regression” workflow doc

This repo now includes all of the above.
