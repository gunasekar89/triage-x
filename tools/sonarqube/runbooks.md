# SonarQube: runbooks

Failure patterns for SonarQube. Signatures and commands are **illustrative** and must be checked against real tool output. Every fix is a **manual action** performed by the developer under the normal change and approval process; TRIAGE-X never performs it.

## Pattern index

| ID | Pattern | Stage | Category | Expected classification |
|---|---|---|---|---|
| SQ-01 | Coverage on new code below threshold | `quality-security` | `policy-gate` | Self-fix (`policy-gate`), High confidence |
| SQ-02 | New blocker/critical issues or security hotspots | `quality-security` | `policy-gate` | Self-fix (`policy-gate`) |
| SQ-03 | Duplication on new code above threshold | `quality-security` | `policy-gate` | Self-fix (`policy-gate`) |
| SQ-04 | Analysis did not complete; gate status unavailable | `quality-security` | `platform-infra` | L1 (`platform-infra`); Prod team if multi-app; Self-fix if project scanner config is wrong |
| SQ-05 | Coverage report not imported | `quality-security` | `configuration` | Self-fix (`configuration`), Medium-High |
| SQ-06 | Scanner authentication failure | `quality-security` | `credentials-access` | L1 (`credentials-access`) |

## Pattern SQ-01: Coverage on new code below threshold

- **Lifecycle stage:** `quality-security`
- **Failure category:** `policy-gate`
- **Symptoms:** Gate ERROR; Jenkins Quality Gate stage fails.
- **Log or event signatures (illustrative):** Condition `new_coverage` `LT` `80` actual `61.2` (values illustrative); `QUALITY GATE STATUS: FAILED`.
- **Evidence to collect:**
  - Gate condition with actual and threshold.
  - Jenkins gate line (reporter).
- **What-changed checks:** Commits adding untested code.
- **Possible cause:** New code lacks tests; gate correctly blocks.
- **Safe diagnostic checks:**
  - Read gate status.
  - Read `new_coverage` and uncovered files.
- **Developer-performed fix:**
  - Add tests for new or changed code.
  - Push and let CI re-run the analysis.
- **L1 escalation conditions:** Coverage report is produced but not imported (shows 0% though tests ran) → SQ-05.
- **Prod-team conditions:** None.
- **Expected classification:** Self-fix (`policy-gate`), High confidence.

## Pattern SQ-02: New blocker/critical issues or security hotspots

- **Lifecycle stage:** `quality-security`
- **Failure category:** `policy-gate`
- **Symptoms:** Gate fails on reliability, security rating or hotspots reviewed.
- **Log or event signatures (illustrative):** Condition `new_security_rating` `GT` `1`; `new_blocker_violations` > 0.
- **Evidence to collect:**
  - Failing condition.
  - Issue keys and rules (sanitized).
- **What-changed checks:** Commits introducing the issues.
- **Possible cause:** Newly introduced issues violate the gate.
- **Safe diagnostic checks:**
  - List new issues by severity.
- **Developer-performed fix:** Fix the issues; if a finding is believed wrong, follow the team's review process (TRIAGE-X does not mark issues).
- **L1 escalation conditions:** Rule appears misconfigured for the whole organization.
- **Prod-team conditions:** None.
- **Expected classification:** Self-fix (`policy-gate`).

## Pattern SQ-03: Duplication on new code above threshold

- **Lifecycle stage:** `quality-security`
- **Failure category:** `policy-gate`
- **Symptoms:** Gate fails on duplicated lines.
- **Log or event signatures (illustrative):** Condition `new_duplicated_lines_density` `GT` `3`.
- **Evidence to collect:**
  - Condition values.
  - Files with duplication.
- **What-changed checks:** Copied code or generated files newly included.
- **Possible cause:** Duplicated code, or generated code not excluded from analysis.
- **Safe diagnostic checks:**
  - Read measure and duplicated files.
- **Developer-performed fix:** Refactor duplicates or exclude generated code per team convention.
- **L1 escalation conditions:** Exclusions are managed centrally and the developer cannot change them.
- **Prod-team conditions:** None.
- **Expected classification:** Self-fix (`policy-gate`).

## Pattern SQ-04: Analysis did not complete; gate status unavailable

- **Lifecycle stage:** `quality-security`
- **Failure category:** `platform-infra`
- **Symptoms:** Jenkins waits for gate and times out, or gate status NONE.
- **Log or event signatures (illustrative):** `Timeout waiting for quality gate`, CE task status `FAILED` or `PENDING` for long; `status: NONE`.
- **Evidence to collect:**
  - CE task status and error message.
  - Jenkins wait message.
- **What-changed checks:** Scanner version or server changes (`TODO(owner)`).
- **Possible cause:** Background task failed, queue backlog, or webhook to Jenkins missing.
- **Safe diagnostic checks:**
  - Read CE task.
  - Check whether other projects' tasks are pending (if authorized).
- **Developer-performed fix:** If the CE error points to the project's own scanner config (e.g. wrong project key), correct it.
- **L1 escalation conditions:** CE task failed with a server-side error, or webhook missing for the project.
- **Prod-team conditions:** Many projects' tasks failing or pending (server degraded).
- **Expected classification:** L1 (`platform-infra`); Prod team if multi-app; Self-fix if project scanner config is wrong.

## Pattern SQ-05: Coverage report not imported

- **Lifecycle stage:** `quality-security`
- **Failure category:** `configuration`
- **Symptoms:** Coverage shows 0% or missing although tests ran.
- **Log or event signatures (illustrative):** Scanner log `No coverage report can be found`, `Coverage report doesn't exist`.
- **Evidence to collect:**
  - Scanner log line from Jenkins console.
  - Test stage result.
- **What-changed checks:** Changes to report paths, build tool plugin, or test task.
- **Possible cause:** Coverage report path misconfigured.
- **Safe diagnostic checks:**
  - Search console for coverage import messages.
  - Compare scanner properties with last good build.
- **Developer-performed fix:** Fix coverage report path property in the build configuration.
- **L1 escalation conditions:** Path is correct and the scanner still cannot read it.
- **Prod-team conditions:** None.
- **Expected classification:** Self-fix (`configuration`), Medium-High.

## Pattern SQ-06: Scanner authentication failure

- **Lifecycle stage:** `quality-security`
- **Failure category:** `credentials-access`
- **Symptoms:** Analysis step fails before upload.
- **Log or event signatures (illustrative):** `Not authorized. Please check the property sonar.login`, `401`, `Insufficient privileges`.
- **Evidence to collect:**
  - Error excerpt (no token values).
  - When it last worked.
- **What-changed checks:** Token rotation; project permission changes.
- **Possible cause:** Token expired, revoked or lacks Execute Analysis permission.
- **Safe diagnostic checks:**
  - Confirm error type from console; never read the token.
- **Developer-performed fix:** None unless the team owns the token configuration.
- **L1 escalation conditions:** Token or permission must be renewed by tool admins.
- **Prod-team conditions:** Many projects fail auth at once.
- **Expected classification:** L1 (`credentials-access`).
