# Adoption Guide

You have one job: expose one endpoint. That's it.

Everything else—test cases, gates, reports—comes from this repo. You just need to answer when we call.

---

## The Contract

### `POST /eval/run`

We send you a case. You send back what happened.

**Request:**
```json
{
  "case_id": "SCENARIO_0001",
  "inputs": {
    "user": "Summarize the attached document in 5 bullets."
  },
  "context": {
    "mode": "summarize",
    "locale": "en-US"
  },
  "fixtures": {
    "retrieval_docs": [],
    "attachments": []
  },
  "options": {
    "trace": true,
    "deterministic": true
  }
}
```

**Response (full):**
```json
{
  "outputs": {
    "final_text": "Here are the 5 key points...",
    "decision": "PASS"
  },
  "policy": {
    "refuse": false,
    "abstain": false,
    "escalate": false,
    "reasons": []
  },
  "retrieval": {
    "queries": ["document summary requirements"],
    "doc_ids": ["doc_abc123"]
  },
  "actions": [
    {
      "tool": "document_reader",
      "status": "success",
      "latency_ms": 45,
      "input_hash": "sha256:...",
      "output_hash": "sha256:..."
    }
  ],
  "steps": [
    {"step": "parse_request", "duration_ms": 2},
    {"step": "retrieve_docs", "duration_ms": 45},
    {"step": "generate_summary", "duration_ms": 312}
  ]
}
```

---

## Start Minimal, Add Later

Day 1—just return this:
```json
{
  "outputs": {
    "final_text": "...",
    "decision": "PASS"
  }
}
```

The harness defaults empty `policy`, `retrieval`, `actions`, `steps`.

Add them when you're ready. The gates only check what you provide.

---

## Response Field Reference

| Field | Required | What It Proves |
|-------|----------|----------------|
| `outputs.final_text` | Yes | What the system said |
| `outputs.decision` | Yes | PASS, FAIL, NEEDS_REVIEW, ABSTAIN |
| `policy.refuse` | No | Did system refuse to engage? |
| `policy.abstain` | No | Did system admit it doesn't know? |
| `policy.escalate` | No | Did system flag for human review? |
| `policy.reasons` | No | Why the policy action was taken |
| `retrieval.queries` | No | What searches were run |
| `retrieval.doc_ids` | No | What documents were retrieved |
| `actions[]` | No | What tools were called (with hashes) |
| `steps[]` | No | Timing breakdown of the pipeline |

---

## Decision Values

| Value | Meaning | When to Use |
|-------|---------|-------------|
| `PASS` | Request handled successfully | Normal completion |
| `FAIL` | System could not complete | Error state |
| `NEEDS_REVIEW` | Output needs human verification | Low confidence, edge case |
| `ABSTAIN` | System chose not to answer | Insufficient evidence |

---

## Map Your Product

**Chatbots:**
- Return `final_text` with the response
- `decision` = PASS (or ABSTAIN if refusing)
- Add `policy.refuse = true` if declining unsafe request

**RAG Systems:**
- Include `retrieval.queries` and `retrieval.doc_ids`
- Add `policy.abstain = true` if no relevant docs found
- Citations should be in `final_text`

**Agents / Tool Use:**
- Include `actions[]` with every tool call
- Each action needs: tool name, status, latency, input/output hashes
- `decision` = FAIL if critical tool failed

**Extractors / Classifiers:**
- Return structured data as JSON string in `final_text`
- `decision` = NEEDS_REVIEW if confidence below threshold

---

## Determinism

For CI stability:
- Set `temperature = 0` when `options.deterministic = true`
- Use fixed seeds if your model supports them
- In CI, prefer replay mode (no network, no flakes)

---

## The Adoption Ladder

| Level | What You Do | What You Get |
|-------|-------------|--------------|
| 1 | Return `outputs` only | Basic coverage |
| 2 | Add `policy` fields | Refusal/abstention tracking |
| 3 | Add `retrieval` fields | RAG behavior visibility |
| 4 | Add `actions` with hashes | Tool use accountability |
| 5 | Add `steps` timing | Performance profiling |
| 6 | Implement all suites | Full behavioral coverage |

---

## Integration Checklist

```
[ ] Endpoint deployed: POST /eval/run
[ ] Returns outputs.final_text
[ ] Returns outputs.decision
[ ] Tested with: book-of-fail --adapter http --suite contract --base-url YOUR_URL
[ ] CI gate configured (see .github/workflows/eval.yml)
[ ] First incident converted to regression test
```

---

## Reference Implementation (Python/FastAPI)

```python
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class EvalRequest(BaseModel):
    case_id: str
    inputs: dict
    context: dict = {}
    fixtures: dict = {}
    options: dict = {}

class EvalResponse(BaseModel):
    outputs: dict
    policy: dict = {"refuse": False, "abstain": False, "escalate": False, "reasons": []}
    retrieval: dict = {"queries": [], "doc_ids": []}
    actions: list = []
    steps: list = []

@app.post("/eval/run")
async def eval_run(request: EvalRequest) -> EvalResponse:
    # Your AI system goes here
    result = your_ai_system.process(
        inputs=request.inputs,
        context=request.context,
        fixtures=request.fixtures,
        deterministic=request.options.get("deterministic", False)
    )
    
    return EvalResponse(
        outputs={
            "final_text": result.text,
            "decision": "PASS" if result.success else "FAIL"
        },
        policy={
            "refuse": result.refused,
            "abstain": result.abstained,
            "escalate": result.needs_review,
            "reasons": result.policy_reasons
        },
        retrieval={
            "queries": result.search_queries,
            "doc_ids": result.retrieved_doc_ids
        },
        actions=result.tool_calls,
        steps=result.timing_steps
    )
```

---

## FAQ

**Q: Do I need to implement all fields?**  
A: No. Start with `outputs`. Add fields as you mature.

**Q: What if my system doesn't use tools?**  
A: Leave `actions` empty. The harness ignores what you don't provide.

**Q: What if a test fails?**  
A: Good. That's the point. Fix the behavior, not the test.

**Q: Can I run this without deploying an endpoint?**  
A: Yes. Use replay mode for deterministic CI without network calls.

---

**No trace, no ship.**
