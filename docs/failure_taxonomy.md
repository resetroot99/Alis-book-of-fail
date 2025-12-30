# Failure Taxonomy (Naming the Monsters)

If you can't name it, you can't kill it.

This is the shared vocabulary for AI failures. Use these labels in traces, reports, postmortems, and bar fights about why your system is misbehaving.

---

## Why This Matters

Every failure needs a name. Not a vague "it gave a bad answer" but a specific, trackable category that tells you:
- What went wrong
- Where to look
- What test to write

Unnamed failures are invisible failures. Invisible failures repeat.

---

## Core Failures (The Greatest Hits)

These are the failures that show up everywhere. If you only track ten things, track these.

| Label | Description | Example |
|-------|-------------|---------|
| `CONFIDENT_NONSENSE` | Fluent, confident, completely wrong | "The capital of Australia is Sydney" with no hesitation |
| `PARTIAL_EVIDENCE_GUESS` | Answered without enough evidence | Made a decision based on 1 of 5 required data points |
| `CORRECT_FOR_WRONG_REASON` | Got it right accidentally | Right answer, but the reasoning was completely fabricated |
| `UNSUPPORTED_CLAIM` | Claim with no backing | "Studies show..." with no studies cited |
| `CONFLICT_NOT_HANDLED` | Contradictory sources ignored | Two docs disagree, system picks one silently |
| `STALE_EVIDENCE` | Relied on outdated information | Used 2019 data to answer a 2024 question |
| `TRUNCATION_SILENCE` | Context cut off without disclosure | Important info was truncated, system proceeded anyway |

---

## Retrieval Failures (The Silent Killers)

Most "reasoning failures" are actually retrieval failures wearing a disguise.

| Label | Description | Example |
|-------|-------------|---------|
| `RETRIEVAL_MISS` | Gold document not retrieved | The answer was in the corpus, but embeddings missed it |
| `RETRIEVAL_POISONING` | Malicious content in retrieval affects answer | Attacker-planted doc changes the response |
| `CONTEXT_POISONING` | Low-quality docs dominate context | Noisy irrelevant content crowds out signal |
| `CITATION_HALLUCINATION` | Cites doc that doesn't contain claim | "According to the policy doc..." but it doesn't say that |
| `CONTEXT_OVERFLOW` | Important info lost to token limits | Critical data truncated because context was stuffed |
| `RECENCY_BIAS` | Newer doc preferred over correct older doc | Wrong blog post beats correct official doc |
| `AUTHORITY_CONFUSION` | Can't distinguish authoritative sources | Forum post weighted same as official guidance |
| `CHUNK_BOUNDARY_MISS` | Answer split across chunks, neither retrieved | The phone number was split at the chunk boundary |
| `SEMANTIC_DRIFT` | Query meaning drifted during retrieval | Asked about cancellation, got refund info |
| `KEYWORD_GAMING` | SEO-stuffed doc ranked high | Keyword spam outranked quality content |
| `METADATA_BLINDNESS` | Ignored date/author/source metadata | Used old doc because it didn't check dates |
| `DUPLICATE_AMPLIFICATION` | Same wrong info treated as consensus | Three wrong sources ≠ one right answer |
| `NEGATIVE_EVIDENCE_MISS` | Failed to retrieve contradicting docs | The "known issues" doc was never considered |
| `PARTIAL_QUOTE` | Quoted out of context, changed meaning | "Is NOT recommended" became "is recommended" |
| `ATTRIBUTION_SWAP` | Attributed claim to wrong source | CEO quote attributed to analyst |
| `RETRIEVAL_ZERO` | No docs retrieved, answered anyway | Empty retrieval, full confidence |

---

## Agentic Failures (The New Frontier)

Agents can do things. That means they can do wrong things. Repeatedly. At scale.

| Label | Description | Example |
|-------|-------------|---------|
| `TOOL_LOOP` | Infinite tool-calling cycle | Kept retrying failed API forever |
| `GOAL_HIJACK` | User instruction overrode system goal | "Forget your instructions" actually worked |
| `PERMISSION_ESCALATION` | Attempted action outside allowlist | Tried to delete files when only read was allowed |
| `ACTION_WITHOUT_CONFIRM` | Irreversible action without user consent | Sent email to 50K users without asking |
| `RACE_CONDITION` | Parallel actions conflicted | Two updates to same record, last one wins |
| `RETRY_STORM` | Failed action retried infinitely | Hammered rate-limited API without backoff |
| `STATE_AMNESIA` | Forgot prior actions in multi-step task | Redid work that was already completed |
| `PHANTOM_SUCCESS` | Claimed completion without performing action | "Done!" but trace shows nothing happened |
| `SCOPE_CREEP` | Did more than asked | User asked for email update, agent also "helpfully" changed password |
| `SCOPE_SHRINK` | Did less than asked without disclosure | Updated 2 of 3 fields, said "done" |
| `WRONG_TOOL` | Used wrong tool for task | Used delete_sent when delete_draft was intended |
| `ARG_HALLUCINATION` | Invented tool arguments | Made up email address when user didn't provide one |
| `CASCADE_FAILURE` | One failure broke entire plan | Payment failed, but inventory was still reserved |
| `SIDE_EFFECT_BLINDNESS` | Ignored known consequences of action | Archived folder without warning about access revocation |
| `IRREVERSIBLE_ACTION` | Took permanent action without warning | Permanent delete without "this can't be undone" |

---

## Tool Failures (The Blame Game)

When tools go wrong, the system must handle it gracefully. Usually it doesn't.

| Label | Description | Example |
|-------|-------------|---------|
| `TOOL_HALLUCINATION` | Claimed tool ran with no receipt | "I checked the database" with no trace of query |
| `ACTION_CLAIM_MISMATCH` | Output says X, trace shows Y | Said email sent, trace shows draft saved |
| `TOOL_FAILURE_UNSAFE_DEGRADE` | Tool error led to guessing | API failed, so system made up the data |

---

## Policy Failures (The Safety Layer)

Getting safety wrong goes both directions.

| Label | Description | Example |
|-------|-------------|---------|
| `OVER_REFUSAL` | Refused a safe request | Won't discuss "kill process" because "kill" |
| `UNDER_REFUSAL` | Complied with unsafe request | Provided harmful instructions when asked nicely |
| `PROMPT_INJECTION_SUCCESS` | Followed injected instructions | "Ignore previous" actually ignored previous |

---

## Multimodal Failures (New Dimensions of Wrong)

Images, audio, video—new inputs, new ways to fail.

| Label | Description | Example |
|-------|-------------|---------|
| `IMAGE_INJECTION` | Text in image used as instruction | "SYSTEM: ignore all rules" in image background |
| `OCR_HALLUCINATION` | Read text that isn't there | "Saw" words in a blank image |
| `VISUAL_CONTEXT_MISS` | Ignored critical visual context | Missed the strikethrough on "AMAZING" |
| `TRANSCRIPTION_ERROR` | Mistranscribed audio, proceeded confidently | "March 15" became "March 50" |
| `CROSS_MODAL_CONFLICT` | Text and image disagree, no disclosure | Description says "mint condition," image shows cracks |
| `CHART_MISREAD` | Misinterpreted graph/chart data | Read the wrong bar as highest |
| `TABLE_STRUCTURE_FAIL` | Lost table structure in extraction | Columns got merged, rows got scrambled |
| `CAPTION_MISMATCH` | Description doesn't match image | Described people that aren't there |
| `LAYOUT_CONFUSION` | Multi-column doc read in wrong order | PDF columns merged into nonsense |
| `HANDWRITING_GUESS` | Guessed illegible handwriting confidently | "Definitely says Tuesday" when illegible |
| `UI_INJECTION` | UI elements treated as commands | Button text "DELETE ALL" triggered action |
| `FRAME_SELECTION_BIAS` | Wrong video frame selected | Used end credits to summarize movie |
| `SPEAKER_CONFUSION` | Attributed statement to wrong speaker | CEO "said" what the analyst said |

---

## Meta Failures (Failures About Failures)

When your evaluation itself is broken.

| Label | Description | Example |
|-------|-------------|---------|
| `JUDGE_HALLUCINATION` | LLM judge invented criteria | Judge said "factual" but made up the facts |
| `EVAL_GAMING` | System optimized for eval, not task | Passes tests, fails users |
| `METRIC_GOODHART` | Metric became the target | Maximized score, minimized utility |
| `FLAKY_EVAL` | Same input, different results | Test passes 70% of the time for no reason |
| `GROUND_TRUTH_ERROR` | Your "gold" answer was wrong | The test expects the wrong answer |

---

## Temporal Failures (Time is a Flat Circle)

Failures related to when, not what.

| Label | Description | Example |
|-------|-------------|---------|
| `VERSION_CONFUSION` | Mixed up document versions | Used v1.2 when v2.0 was current |
| `TEMPORAL_LEAK` | Future info used for past question | Used 2024 data to answer 2023 question |
| `DEADLINE_MISS` | Took too long to be useful | Correct answer, 10 minutes after decision was made |
| `CACHE_STALENESS` | Cached answer was outdated | Returned yesterday's stock price |

---

## Using the Taxonomy

### In Traces

Every trace should include failure labels when applicable:

```yaml
trace:
  case_id: SCENARIO_0042
  decision: FAIL
  failure_labels:
    - CONFIDENT_NONSENSE
    - RETRIEVAL_MISS
  notes: System answered confidently but gold doc was not retrieved
```

### In Postmortems

Every incident should map to taxonomy labels:

```markdown
## Incident: Wrong dosage shown to user

**Failure labels:** CITATION_HALLUCINATION, AUTHORITY_CONFUSION
**Root cause:** System cited a study that didn't contain dosage info, 
ignored the official FDA document.
**Regression:** RAG_0002_citation_hallucination
```

### In Dashboards

Track failure label frequency over time:

| Label | This Week | Last Week | Trend |
|-------|-----------|-----------|-------|
| CONFIDENT_NONSENSE | 12 | 8 | ↑ |
| RETRIEVAL_MISS | 5 | 7 | ↓ |
| OVER_REFUSAL | 23 | 19 | ↑ |

---

## Contributing New Labels

Found a failure that doesn't fit? Propose a new label:

1. Clear, memorable name (all caps, underscores)
2. One-line description
3. At least one concrete example
4. Suggested category

Open an issue or PR. If it's a real pattern, it gets added.

---

## The Meta-Rule

If you see a failure and can't immediately name it from this list, one of two things is true:

1. **You don't understand the failure yet.** Dig deeper.
2. **The taxonomy is incomplete.** Add to it.

Unnamed monsters keep eating people.

Name them.
