# Case Authoring Checklist (Write Tests That Actually Matter)

A case is good if it is **diffable**, **reproducible**, and **decision‑focused**.

## Every case should include
- **id**: stable, unique
- **type**: contract | regression | scenario | adversarial | shift | performance
- **risk**: low | medium | high
- **description**: what behavior is being enforced
- **inputs**: the user prompt (and any structured inputs your domain needs)
- **context**: mode (chat, summarize, rag_qa, agent, extract, classify, etc.)
- **expect.output_schema**: usually `GenericResponse.v1`

## If the case is high risk, include at least one of:
- `expect.decision`: PASS / NEEDS_REVIEW / REFUSE
- `checks.must_not_match_patterns`: secret/credential patterns
- `checks.forbid_action_claims_without_actions`: prevents fake tool execution
- `checks.should_include_any`: “uncertain / verify / needs review” disclosures
- fixtures: retrieval docs with conflicts, stale timestamps, injected content

## Make it punish the real failure
Bad eval asks: “Did it answer?”
Good eval asks: “Did it decide correctly under uncertainty?”

Examples:
- Missing required inputs → NEEDS_REVIEW
- Conflicting sources → NEEDS_REVIEW
- Dangerous request → REFUSE
- Tool error → disclose limitation, no fake success

## Avoid these traps
- Vibe-based scoring with no gates
- Single phrasing (no paraphrases)
- No degraded inputs
- No conflict tests
- No trace expectations

## Gold standard
A case becomes a regression when:
- it reproduced a real incident
- it fails before the fix and passes after
- it prevents recurrence
