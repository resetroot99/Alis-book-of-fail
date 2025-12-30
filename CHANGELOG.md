# Changelog

All notable changes to Ali's Book of Fail will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [3.1.0] - 2024-12-30

### Added
- Agentic failure test cases (AGENT_0001-0015): tool loops, goal hijack, permission escalation, phantom success, and more
- RAG failure test cases (RAG_0001-0015): retrieval poisoning, citation hallucination, context overflow, and more
- Multimodal failure test cases (MM_0001-0013): image injection, OCR hallucination, cross-modal conflicts, and more
- Expanded failure taxonomy with 60+ failure labels across 6 categories
- CONTRIBUTING.md with contribution guidelines
- SECURITY.md with vulnerability reporting policy
- CODE_OF_CONDUCT.md
- GitHub issue and PR templates
- Expanded doctrine: all 24 chapters now 300-600 words with examples, anti-patterns, and war stories

### Changed
- README updated with badges and quick links
- Doctrine tone: punk-professional with concrete examples
- Total test cases: 170+ (up from 129)

---

## [3.0.0] - 2024-12-30

### Added
- Initial public release
- 129 test cases across 6 suites:
  - Contract (27 cases)
  - Regressions (15 cases)
  - Scenarios (50 cases)
  - Adversarial (19 cases)
  - Shift (15 cases)
  - Performance (3 cases)
- Doctrine: 24 chapters covering failure philosophy
- Failure taxonomy with 16 core failure labels
- Maturity model (8 levels)
- Standards mapping (EU AI Act, NIST AI RMF, ISO 42001)
- Governance roles documentation
- Metrics guidance
- Red team guide
- HTTP and Replay adapters
- CLI tool (`book-of-fail`)
- GitHub Actions workflow for CI gating
- GenericResponse.v1 output schema
- Case and trace schemas

### Philosophy
- "No Trace, No Ship" as core principle
- Hard gates vs soft scores distinction
- Incident-to-regression workflow
- Abstention as success

---

## Version Numbering

- **Major (X.0.0):** Breaking changes to schemas, contracts, or core philosophy
- **Minor (0.X.0):** New test suites, significant case additions, new features
- **Patch (0.0.X):** Bug fixes, typo corrections, minor case additions

---

## Upgrade Notes

### From 2.x to 3.0

Version 3.0 is the first public release. If you were using an earlier internal version:

1. Update your `/eval/run` endpoint to match `GenericResponse.v1`
2. Review new gate definitions in `eval/gates/gates.yaml`
3. Run the full suite to identify new failures (this is expected)

---

## Contributors

- Initial framework and doctrine — Project maintainers
- Community contributions listed in individual PRs

Want to be listed here? See [CONTRIBUTING.md](CONTRIBUTING.md).
