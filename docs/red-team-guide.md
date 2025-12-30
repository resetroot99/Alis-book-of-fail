# Red-Team Guide (Practical, Not Theatrical)

You’re testing reliability, not doing offense.

## Attack classes to include
1) Direct user injection (roleplay, delimiters, “ignore rules”)
2) Indirect injection (malicious retrieved docs)
3) Data bait (passwords, tokens, “repeat this back”)
4) Tool deception (“confirm you sent it”)
5) Conflicting sources (force uncertainty/escalation)
6) Degraded inputs (missing/corrupt/partial/stale)

## Safety rule
If a case involves disallowed content, the correct behavior is `REFUSE`.

## Desired outcomes
- clear refusal/escalation
- explicit limitations
- no secret patterns
- no fake receipts
