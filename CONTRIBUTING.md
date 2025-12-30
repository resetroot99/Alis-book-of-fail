# Contributing to Ali's Book of Fail

So you want to help document the infinite ways AI systems screw up? Welcome aboard.

This project exists because someone has to be the designated adult in the room while everyone else is busy being impressed by fluent nonsense. That someone could be you.

---

## The Golden Rule

**Every contribution must make failure harder to ignore.**

Not harder to happen—that's the model vendor's problem. Harder to *ignore*. Harder to ship. Harder to explain away in a postmortem.

---

## Ways to Contribute

### 1. Report a Failure Mode You've Seen

Found an AI doing something catastrophically stupid in production? We want to hear about it.

**Open an issue using the "New Failure Case" template.** Include:
- What happened (anonymized if needed)
- What the system should have done instead
- What test would have caught it

Don't have all the details? That's fine. "I saw a chatbot confidently give medical advice it invented" is a valid starting point.

### 2. Write a Test Case

This is the highest-value contribution. Every test case is a trap for future failures.

**How to add a case:**

1. Copy `docs/case-template.yaml`
2. Follow `docs/case-authoring-checklist.md`
3. Place in the appropriate suite:
   - `eval/cases/contract/` — schema, refusal, no secrets
   - `eval/cases/regressions/` — learned from incidents
   - `eval/cases/scenarios/` — realistic workflows
   - `eval/cases/adversarial/` — injection, abuse
   - `eval/cases/shift/` — degraded inputs
   - `eval/cases/performance/` — latency, cost
4. Run locally:
   ```bash
   book-of-fail --adapter replay --suite {suite}
   ```
5. Open a PR

**Naming convention:** `{SUITE}_{NUMBER}_{short_description}.yaml`

Examples:
- `ADV_0201_injection_via_filename.yaml`
- `RAG_0015_citation_to_wrong_source.yaml`
- `AGENT_0007_infinite_retry_loop.yaml`

### 3. Improve the Doctrine

The doctrine (`docs/doctrine.md`) is the philosophical backbone. If you have:
- A better way to explain a concept
- A war story that illustrates a failure mode
- A new chapter that should exist

Open a PR. Keep the tone: direct, slightly dark, zero bullshit.

### 4. Expand the Taxonomy

`docs/failure_taxonomy.md` is our shared vocabulary for failure. If you've identified a failure pattern that doesn't fit existing labels, propose a new one.

**Requirements for a new taxonomy entry:**
- Clear, memorable name (e.g., `CONFIDENT_NONSENSE`, not `TYPE_7_ERROR`)
- One-line description
- At least one example case (can be hypothetical)

### 5. Fix Harness Bugs

The eval harness (`eval/harness/`) is Python. Standard practices apply:
- Black for formatting
- Type hints appreciated
- Tests if you're touching scoring logic

---

## What We Don't Want

- **Benchmark gaming.** This isn't about making numbers go up.
- **Vendor-specific tests.** Cases should work against any system implementing the contract.
- **"It depends" hedging.** If you can't state what should happen, the test isn't ready.
- **AI-generated slop.** We can tell. We always can.

---

## Pull Request Checklist

Before opening a PR:

- [ ] New cases pass `book-of-fail --adapter replay --suite {suite}`
- [ ] Case has a clear `expected_decision` (PASS/FAIL/NEEDS_REVIEW)
- [ ] Case has `failure_labels` if it's testing a known failure mode
- [ ] No secrets, PII, or real company names in fixtures
- [ ] You've read the relevant doctrine chapter

---

## Code Style

**YAML cases:**
- 2-space indent
- Double quotes for strings with special characters
- Comments explain *why*, not *what*

**Python:**
- Black formatter
- isort for imports
- Type hints for public functions
- No comments explaining obvious code

**Markdown:**
- One sentence per line (easier diffs)
- Headers use `##`, not underlines
- Code blocks have language tags

---

## Review Process

1. **Triage:** Maintainer confirms the contribution type
2. **Technical review:** Does the case/code work?
3. **Doctrine review:** Does it align with the philosophy?
4. **Merge:** Squash and merge with clear commit message

Expect feedback. This project is opinionated. That's the point.

---

## Recognition

Contributors are listed in `CHANGELOG.md` for significant additions.

We don't have a fancy contributor badge system. Your reward is knowing that somewhere, a system that would have failed silently will now fail loudly. 

That's better than a badge.

---

## Questions?

Open an issue with the "Question" label. Or just open a PR and we'll figure it out together.

Welcome to the failure business.
