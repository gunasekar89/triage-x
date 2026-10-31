# Gates: runbooks

Failure patterns for Gates. Signatures and commands are **illustrative** and must be checked against real tool output. Every fix is a **manual action** performed by the developer under the normal change and approval process; TRIAGE-X never performs it.

## Pattern index

| ID | Pattern | Stage | Category | Expected classification |
|---|---|---|---|---|
| GT-01 | Security vulnerability threshold exceeded | `quality-security` | `policy-gate` | Self-fix (`policy-gate`), High confidence when findings are listed |
| GT-02 | Required evidence missing for gate | `quality-security` | `configuration` | Self-fix (`configuration`) |
| GT-03 | Gate service error or timeout | `quality-security` | `platform-infra` | L1 (`platform-infra`) or Prod team when multi-app is evidenced |
| GT-04 | Gate threshold changed unexpectedly | `quality-security` | `policy-gate` | Self-fix if the new rule is documented; L1 (`unknown`/Medium) if not |
| GT-05 | License compliance violation | `quality-security` | `policy-gate` | Self-fix (`policy-gate`) |

## Pattern GT-01: Security vulnerability threshold exceeded

- **Lifecycle stage:** `quality-security`
- **Failure category:** `policy-gate`
- **Symptoms:** Release gate blocks promotion citing vulnerabilities.
- **Log or event signatures (illustrative):** `Gate FAILED: critical vulnerabilities 2 > 0`, `policy violation: <rule-id>`.
- **Evidence to collect:**
  - Gate condition and counts.
  - Component(s) with findings (sanitized).
- **What-changed checks:** Dependency or base image changes introducing the vulnerable component.
- **Possible cause:** Gate correctly blocks a change with known vulnerabilities.
- **Safe diagnostic checks:**
  - Read gate result and findings list.
  - Compare components with last passing version.
- **Developer-performed fix:**
  - Upgrade the vulnerable dependency or base image.
  - Rebuild and re-run the gate.
  - If no fix exists, follow the exception process (`TODO(owner)`).
- **L1 escalation conditions:** Developer believes the finding is a false positive and needs a formal review.
- **Prod-team conditions:** None.
- **Expected classification:** Self-fix (`policy-gate`), High confidence when findings are listed.

## Pattern GT-02: Required evidence missing for gate

- **Lifecycle stage:** `quality-security`
- **Failure category:** `configuration`
- **Symptoms:** Gate fails because a report or record is missing.
- **Log or event signatures (illustrative):** `required evidence not found`, `no test report attached`, `change record missing`.
- **Evidence to collect:**
  - Gate message naming missing evidence.
  - Whether the producing stage ran.
- **What-changed checks:** Pipeline edits that skip or rename the producing step.
- **Possible cause:** Upstream step skipped or misconfigured.
- **Safe diagnostic checks:**
  - Walk upstream to the step that produces the evidence.
- **Developer-performed fix:** Restore the producing step or attach the required record per process.
- **L1 escalation conditions:** Evidence was produced but the gate cannot see it (integration issue).
- **Prod-team conditions:** None.
- **Expected classification:** Self-fix (`configuration`). L1 if evidence exists but is not picked up.

## Pattern GT-03: Gate service error or timeout

- **Lifecycle stage:** `quality-security`
- **Failure category:** `platform-infra`
- **Symptoms:** Gate returns error instead of pass/fail.
- **Log or event signatures (illustrative):** `gate evaluation error`, `503`, `timeout waiting for gate`.
- **Evidence to collect:**
  - Error excerpt and time.
  - Other apps' gate results in the same window (if visible).
- **What-changed checks:** Platform notices.
- **Possible cause:** Gate service unavailable.
- **Safe diagnostic checks:**
  - Confirm the error is from the gate service, not from the gate condition.
- **Developer-performed fix:** Retry once later.
- **L1 escalation conditions:** Recurs after one retry, or blast radius unknown.
- **Prod-team conditions:** Multiple applications receive gate errors at the same time.
- **Expected classification:** L1 (`platform-infra`) or Prod team when multi-app is evidenced.

## Pattern GT-04: Gate threshold changed unexpectedly

- **Lifecycle stage:** `quality-security`
- **Failure category:** `policy-gate`
- **Symptoms:** A previously passing app fails with no new findings.
- **Log or event signatures (illustrative):** Same findings as last pass, different gate result; new rule ID.
- **Evidence to collect:**
  - Last passing and current evaluations side by side.
- **What-changed checks:** Gate policy change (if announced).
- **Possible cause:** Policy tightened; block is likely correct.
- **Safe diagnostic checks:**
  - Diff evaluations.
  - Look for a policy change notice (`TODO(owner)`).
- **Developer-performed fix:** Address findings to meet the new policy, or request clarification.
- **L1 escalation conditions:** No policy change can be found and the developer cannot explain the new result.
- **Prod-team conditions:** None.
- **Expected classification:** Self-fix if the new rule is documented; L1 (`unknown`/Medium) if not.

## Pattern GT-05: License compliance violation

- **Lifecycle stage:** `quality-security`
- **Failure category:** `policy-gate`
- **Symptoms:** Gate blocks due to a disallowed license.
- **Log or event signatures (illustrative):** `license <license-id> not allowed`, `license policy violation`.
- **Evidence to collect:**
  - Component and license ID.
- **What-changed checks:** New dependency added.
- **Possible cause:** Newly added component uses a disallowed license.
- **Safe diagnostic checks:**
  - Identify component introduced in recent changes.
- **Developer-performed fix:** Replace the component or follow the license exception process (`TODO(owner)`).
- **L1 escalation conditions:** License data appears wrong for the component.
- **Prod-team conditions:** None.
- **Expected classification:** Self-fix (`policy-gate`).
