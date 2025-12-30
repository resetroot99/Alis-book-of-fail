# Security Policy

## The Irony Is Not Lost on Us

Yes, we're a project about AI security that also needs a security policy. Meta, isn't it?

---

## What This Project Is

Ali's Book of Fail is an **evaluation framework**. It defines test cases and runs them against AI systems you provide. It does not:

- Run AI models itself
- Store user data
- Make network calls (except to your test endpoint)
- Execute arbitrary code from test cases

The attack surface is minimal by design.

---

## Reporting a Vulnerability

If you find a security issue in the harness itself (not a test case for AI failures—that's a feature request), here's what to do:

### For Low-Severity Issues

Open a regular GitHub issue. Examples:
- Dependency with known CVE (we'll update it)
- Insecure default in example code
- Documentation that suggests insecure practices

### For High-Severity Issues

**Do not open a public issue.**

Email the maintainers directly. Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if you have one)

We'll acknowledge within 48 hours and provide a timeline for fix.

---

## Scope

### In Scope

- The evaluation harness (`eval/harness/`)
- CLI tool (`book-of-fail`)
- Any code that executes during test runs
- GitHub Actions workflows

### Out of Scope

- Test cases (YAML files) — these are data, not code
- Documentation — unless it instructs users to do something insecure
- The AI systems you're testing — that's your problem (and why this project exists)

---

## Responsible Disclosure

We follow responsible disclosure practices:

1. Reporter contacts us privately
2. We confirm and assess severity
3. We develop and test a fix
4. We release the fix
5. We credit the reporter (unless they prefer anonymity)
6. Reporter can publish details after fix is released

---

## Security of Your AI System

This framework helps you find security issues in your AI system. It is not a replacement for:

- Proper input validation
- Output sanitization
- Access controls
- Rate limiting
- Monitoring and alerting

If a test case in this repo successfully attacks your system, that's the test working as intended. You're welcome.

---

## Dependencies

We maintain minimal dependencies:

- `PyYAML` — YAML parsing
- `jsonschema` — Schema validation
- `requests` — HTTP client

We monitor these for CVEs and update promptly.

---

## Contact

For security issues: Open a private security advisory on GitHub or contact maintainers directly.

For everything else: Regular issues are fine.
