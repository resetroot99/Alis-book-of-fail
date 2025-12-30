# Adoption Guide (Any Org)

This template is designed to be adopted with **one integration point**.

## Minimum integration: one endpoint

Expose:

### `POST /eval/run`

**Request**
```json
{
  "case_id": "SCENARIO_0001",
  "inputs": {"user": "Summarize the attached document in 5 bullets."},
  "context": {"mode": "summarize", "locale": "en-US"},
  "fixtures": {"retrieval_docs": [], "attachments": []},
  "options": {"trace": true, "deterministic": true}
}
```

**Response (minimum viable)**
```json
{
  "outputs": {
    "final_text": "…",
    "decision": "PASS"
  },
  "policy": {"refuse": false, "abstain": false, "escalate": false, "reasons": []},
  "retrieval": {"queries": [], "doc_ids": []},
  "actions": [],
  "steps": []
}
```

### Notes
- You can omit `policy/retrieval/actions/steps` initially; the harness will default them.
- If you support tool use, include `actions[]` entries (tool name, status, latency, hashes).
- If you support retrieval, include `retrieval` (queries + doc_ids at minimum).

## How to map your product to this contract
- **Chatbots:** return `final_text`, decision = PASS unless refusing
- **Extractors:** return JSON string in `final_text` (or extend schema later)
- **Classifiers:** return label in `final_text`, decision = PASS (or NEEDS_REVIEW)
- **Agents:** include `actions[]` and set decision appropriately

## Determinism options
If your system can accept these options, do it:
- set temperature to 0 in deterministic mode
- use a fixed seed (if supported)
- in CI, prefer replay mode

## The minimal adoption path (recommended)
1) Keep `GenericResponse.v1` schema
2) Start with the included starter cases (contracts + regressions)
3) Gate PRs on `contract + regressions`
4) Turn every incident into a new regression test
