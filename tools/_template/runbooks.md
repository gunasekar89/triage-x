# <Tool>: runbooks

Failure patterns for <Tool>. Signatures and commands are **illustrative** and must be checked against real tool output. Every fix is a **manual action** performed by the developer under the normal change and approval process; TRIAGE-X never performs it.

Write **5–8 patterns**. Pattern IDs use a two-letter tool prefix (e.g. `XX-01`). `tests/validate.py` checks that every pattern has every field below.

## Pattern index

| ID | Pattern | Stage | Category | Expected classification |
|---|---|---|---|---|
| XX-01 | <title> | `<stage-id>` | `<category>` | <Self-fix / L1 / Prod team / status> |

## Pattern XX-01: <title>

- **Lifecycle stage:** `<stage-id>`
- **Failure category:** `<category>`
- **Symptoms:** <what the developer sees>
- **Log or event signatures (illustrative):** <example messages>
- **Evidence to collect:** <facts and their sources>
- **What-changed checks:** <change evidence to look for>
- **Possible cause:** <likely explanation>
- **Safe diagnostic checks:** <read-only checks>
- **Developer-performed fix:** <manual steps, or "none">
- **L1 escalation conditions:** <when L1 is needed>
- **Prod-team conditions:** <when prod team is needed, or "none">
- **Expected classification:** <classification and confidence guidance>
