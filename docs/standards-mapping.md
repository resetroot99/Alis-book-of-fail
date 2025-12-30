# Standards Mapping (Make This Enterprise-Legible)

This is not legal advice. It’s a translation table:
**engineering controls → evidence artifacts**.

## Mapping Table (starter)

| Playbook Control | Evidence Artifact | NIST AI RMF | ISO/IEC 23894 | EU AI Act (high-level) |
|---|---|---|---|---|
| Output schema contracts | `eval/schemas/outputs/*`, `contract` suite | MEASURE, MANAGE | Validation controls | Robustness/accuracy |
| Trace required | `trace.schema.json`, `eval/reports/*` | GOVERN, MEASURE | Monitoring & logs | Logging/traceability |
| Incident → regression | `incident-to-regression.md`, `regressions` suite | MANAGE | Continuous improvement | Post-market monitoring |
| Prompt injection defense | `adversarial` suite | MANAGE | Security risk | Security |
| Secret/PII leak gates | `gates.yaml` + cases | MANAGE | Privacy & security | Data governance |
| Conflict handling | conflict regressions | MEASURE | Data quality | Accuracy/robustness |
| Tool/action receipts | `actions[]` honesty checks | GOVERN | Auditability | Transparency & oversight |
| Shift testing | `shift` suite | MEASURE | Risk under change | Robustness under conditions |

## What auditors love
- PR gate that blocks unsafe behavior
- Replay suite (deterministic)
- Evidence retention (traces + summaries)
- Clear ownership (who approves gates)
