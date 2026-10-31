# Concord: runbooks

Failure patterns for Concord. Signatures and commands are **illustrative** and must be checked against real tool output. Every fix is a **manual action** performed by the developer under the normal change and approval process; TRIAGE-X never performs it.

## Pattern index

| ID | Pattern | Stage | Category | Expected classification |
|---|---|---|---|---|
| CC-01 | Task failed because an upstream Jenkins build failed | `ci-build` | `code-change` | Classify from upstream evidence |
| CC-02 | Flow definition error | `orchestrate-deliver` | `configuration` | Self-fix (`configuration`) |
| CC-03 | Deploy target resolution conflict | `orchestrate-deliver` | `configuration` | Status `needs-input` (classification null) until the developer confirms the target |
| CC-04 | Approval step pending or rejected | `orchestrate-deliver` | `policy-gate` | Self-fix (`policy-gate`) |
| CC-05 | Concord secret or credential not accessible | `orchestrate-deliver` | `credentials-access` | L1 (`credentials-access`) |
| CC-06 | Concord server degraded or processes stuck in queue | `orchestrate-deliver` | `platform-infra` | L1 if blast radius single or unknown; Prod team if multi-app is evidenced |

## Pattern CC-01: Task failed because an upstream Jenkins build failed

- **Lifecycle stage:** `ci-build`
- **Failure category:** `code-change`
- **Symptoms:** Concord process FAILED at a build task.
- **Log or event signatures (illustrative):** `Process finished with status FAILED`; task error naming a Jenkins job/build.
- **Evidence to collect:**
  - Concord failed task and referenced build.
  - Jenkins evidence (walk upstream).
- **What-changed checks:** Per Jenkins module.
- **Possible cause:** Concord is the reporter; Jenkins (or further upstream) holds the cause.
- **Safe diagnostic checks:**
  - Extract build reference from Concord log.
  - Apply Jenkins runbook.
- **Developer-performed fix:** Per Jenkins/SonarQube runbook.
- **L1 escalation conditions:** Jenkins reference missing or not accessible.
- **Prod-team conditions:** None from Concord alone.
- **Expected classification:** Classify from upstream evidence. reported_tool concord. Category follows upstream (shown here as code-change for illustration).

## Pattern CC-02: Flow definition error

- **Lifecycle stage:** `orchestrate-deliver`
- **Failure category:** `configuration`
- **Symptoms:** Process fails at start or at a step with a syntax or variable error.
- **Log or event signatures (illustrative):** `Error while loading the project`, `Variable '<name>' not found`, `Invalid flow`.
- **Evidence to collect:**
  - Error excerpt.
  - Diff of flow file.
- **What-changed checks:** Recent edits to the Concord flow file.
- **Possible cause:** Flow file typo, missing variable, wrong task parameter.
- **Safe diagnostic checks:**
  - Read error excerpt.
  - Diff flow file with last good revision.
- **Developer-performed fix:** Correct the flow file through a PR.
- **L1 escalation conditions:** Error references a shared plugin or task version the developer cannot change.
- **Prod-team conditions:** None.
- **Expected classification:** Self-fix (`configuration`).

## Pattern CC-03: Deploy target resolution conflict

- **Lifecycle stage:** `orchestrate-deliver`
- **Failure category:** `configuration`
- **Symptoms:** Deploy task targets an unexpected cluster or namespace, or fails to resolve one.
- **Log or event signatures (illustrative):** Target values in log differ from the KITT file; `target not found`.
- **Evidence to collect:**
  - Target values from Concord log.
  - Candidate targets from KITT.
- **What-changed checks:** KITT edits; flow parameter changes.
- **Possible cause:** Mismatch between flow parameters and KITT configuration.
- **Safe diagnostic checks:**
  - List both target sets with sources.
  - Do **not** run cluster checks.
- **Developer-performed fix:** Developer confirms intended target and aligns flow parameters or KITT.
- **L1 escalation conditions:** The developer cannot determine which is authoritative.
- **Prod-team conditions:** None.
- **Expected classification:** Status `needs-input` (classification null) until the developer confirms the target.

## Pattern CC-04: Approval step pending or rejected

- **Lifecycle stage:** `orchestrate-deliver`
- **Failure category:** `policy-gate`
- **Symptoms:** Process suspended or failed at an approval step.
- **Log or event signatures (illustrative):** `SUSPENDED` waiting for form/approval; `approval rejected`.
- **Evidence to collect:**
  - Approval step name and state.
- **What-changed checks:** New approval requirement added to the flow.
- **Possible cause:** Approval correctly required or rejected.
- **Safe diagnostic checks:**
  - Read process status and event at the approval step.
- **Developer-performed fix:** Request approval through the normal process.
- **L1 escalation conditions:** Approver group misconfigured and the developer cannot change it.
- **Prod-team conditions:** None.
- **Expected classification:** Self-fix (`policy-gate`).

## Pattern CC-05: Concord secret or credential not accessible

- **Lifecycle stage:** `orchestrate-deliver`
- **Failure category:** `credentials-access`
- **Symptoms:** Task fails reading a secret.
- **Log or event signatures (illustrative):** `Secret not found`, `Access denied to secret '<name>'`.
- **Evidence to collect:**
  - Secret name (never value).
  - Task name.
- **What-changed checks:** Secret renamed or rotated; org/team change.
- **Possible cause:** Secret missing or the project lacks access.
- **Safe diagnostic checks:**
  - Compare secret name with last good run.
- **Developer-performed fix:** If the name was changed by the team, restore it.
- **L1 escalation conditions:** Secret access must be granted or the secret recreated.
- **Prod-team conditions:** None unless many projects lose secret access at once.
- **Expected classification:** L1 (`credentials-access`).

## Pattern CC-06: Concord server degraded or processes stuck in queue

- **Lifecycle stage:** `orchestrate-deliver`
- **Failure category:** `platform-infra`
- **Symptoms:** Processes stay ENQUEUED or time out; no task error.
- **Log or event signatures (illustrative):** Status `ENQUEUED` for an unusually long time; `Process timed out` with no task error.
- **Evidence to collect:**
  - Process status timeline.
  - Same state across other projects (if visible).
- **What-changed checks:** Platform notices (`TODO(owner)`).
- **Possible cause:** Concord agents or server capacity problem.
- **Safe diagnostic checks:**
  - Read events and timestamps.
  - Check other projects' recent processes if authorized.
- **Developer-performed fix:** None for the developer beyond waiting or one retry later.
- **L1 escalation conditions:** Single project affected or blast radius unknown.
- **Prod-team conditions:** Many projects stuck at the same time.
- **Expected classification:** L1 if blast radius single or unknown; Prod team if multi-app is evidenced.
