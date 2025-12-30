# Ali’s Book of Fail — *Fail Loudly Edition*

A **vendor-agnostic**, **language-agnostic** evaluation harness + doctrine for AI systems:
- chatbots, RAG, agents/tools, extractors, classifiers, multimodal
- **hard gates** (binary) + **soft metrics** (trend)
- **diffable traces** (what it saw / did / said)
- **incident → regression** loop (governance that actually works)

> **No Trace, No Ship.**

---

## Repo layout (aligned to the book)

- `docs/doctrine.md` → *the book* (Oath + Chapters)
- `docs/adoption.md` → how to integrate in any org (one endpoint)
- `docs/failure_taxonomy.md` → shared language for failures
- `docs/why_most_eval_fails.md` → thought-leadership essay
- `eval/cases/*` → test suites (“Sacred Suites”)
- `eval/harness/*` → the executable harness (HTTP + replay adapters)
- `eval/schemas/*` → case/trace/output schemas (contracts)
- `eval/gates/gates.yaml` → hard gates + thresholds
- `eval/reports/*` → traces + summaries

---

## Quickstart

### 1) Install (editable)
```bash
pip install -e .
```

### 2) Run contract suite against your system (HTTP adapter)
Your system should expose: `POST /eval/run`

```bash
book-of-fail --adapter http --suite contract --base-url http://localhost:8000
```

### 3) Run with replay mode (deterministic CI without network/secrets)
```bash
book-of-fail --adapter replay --suite contract
```

### 4) Run everything (best for staging/nightly)
```bash
book-of-fail --adapter http --suite all --base-url http://localhost:8000
```

---

## What you need to implement (minimum viable)

Expose an endpoint:

### `POST /eval/run`
Request/response contract is in `docs/adoption.md`.

You can start by returning only:
- `outputs.final_text`
- `outputs.decision`

…and add `policy/retrieval/actions/steps` later.

---

## CI
See `.github/workflows/eval.yml` for a PR gate example.

---

## License
MIT


## v3 Additions
- Maturity model + standards mapping + governance roles + metrics + red-team guide
- Case pack expanded (100+)
- Case pack generator (`eval/tools/generate_case_pack.py`)
