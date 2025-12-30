# Failure Taxonomy (Naming the Monsters)

Use these labels in traces, reports, and postmortems.

## Core
- **CONFIDENT_NONSENSE** — fluent but wrong
- **PARTIAL_EVIDENCE_GUESS** — answered without enough evidence
- **CORRECT_FOR_WRONG_REASON** — got it right accidentally
- **UNSUPPORTED_CLAIM** — claim with no support
- **CONFLICT_NOT_HANDLED** — contradictory sources ignored
- **STALE_EVIDENCE** — relied on outdated/invalid source
- **TRUNCATION_SILENCE** — context cut off without disclosure

## Retrieval / context
- **RETRIEVAL_MISS** — gold doc not retrieved
- **CONTEXT_POISONING** — low-quality/noisy docs dominate

## Tools / actions
- **TOOL_HALLUCINATION** — claimed tool ran, but no receipt
- **ACTION_CLAIM_MISMATCH** — output says X happened, trace doesn’t
- **TOOL_FAILURE_UNSAFE_DEGRADE** — tool error leads to guessing

## Policy / safety
- **OVER_REFUSAL** — refused a safe request
- **UNDER_REFUSAL** — complied with unsafe request
- **PROMPT_INJECTION_SUCCESS** — followed injected instructions

## Use in practice
- Every incident must be tagged with at least one label.
- Every label must have at least one regression case over time.
