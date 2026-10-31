# Jenkins: runbooks

Failure patterns for Jenkins. Signatures and commands are **illustrative** and must be checked against real tool output. Every fix is a **manual action** performed by the developer under the normal change and approval process; TRIAGE-X never performs it.

## Pattern index

| ID | Pattern | Stage | Category | Expected classification |
|---|---|---|---|---|
| JK-01 | Compilation error after code change | `ci-build` | `code-change` | Self-fix |
| JK-02 | Unit or integration tests failing | `ci-build` | `code-change` | Self-fix |
| JK-03 | Dependency resolution failure | `ci-build` | `dependency` | Self-fix for wrong versions (404 and recent bump) |
| JK-04 | Build agent unavailable or lost | `ci-build` | `platform-infra` | L1 (`platform-infra`) |
| JK-05 | Quality Gate stage failed (reported by Jenkins) | `quality-security` | `policy-gate` | Classify from SonarQube evidence; usually Self-fix (`policy-gate`) |
| JK-06 | Transient network timeout during build | `ci-build` | `transient-flaky` | First occurrence: Self-fix (retry once), Medium confidence |
| JK-07 | Pipeline credential missing or expired | `ci-build` | `credentials-access` | L1 (`credentials-access`) unless the ID typo is the developer's change |

## Pattern JK-01: Compilation error after code change

- **Lifecycle stage:** `ci-build`
- **Failure category:** `code-change`
- **Symptoms:** Build fails in compile stage.
- **Log or event signatures (illustrative):** `cannot find symbol`, `error: incompatible types`, `TS2304`, `SyntaxError`, `BUILD FAILURE`.
- **Evidence to collect:**
  - First compiler error line and file (sanitized).
  - Commits since last green build.
- **What-changed checks:** Commits touching the failing file.
- **Possible cause:** A code change introduced a compile error.
- **Safe diagnostic checks:**
  - Read console around first `error:`.
  - List changeSets since last green.
- **Developer-performed fix:**
  - Reproduce locally with the same build command.
  - Fix the error, push, let CI re-run.
- **L1 escalation conditions:** Same code compiles locally but fails on agent due to tool version mismatch the developer cannot change.
- **Prod-team conditions:** None.
- **Expected classification:** Self-fix. High confidence when the error points to a file changed in the build.

## Pattern JK-02: Unit or integration tests failing

- **Lifecycle stage:** `ci-build`
- **Failure category:** `code-change`
- **Symptoms:** Test stage red; build result UNSTABLE or FAILURE.
- **Log or event signatures (illustrative):** `Tests run: <n>, Failures: <f>`, `AssertionError`, `FAILED <test>`.
- **Evidence to collect:**
  - Failed test names and first assertion message.
  - Whether the same tests passed on the previous build.
- **What-changed checks:** Commits touching code under test or the tests.
- **Possible cause:** Regression or outdated test.
- **Safe diagnostic checks:**
  - Read test report.
  - Compare with previous build's test report.
- **Developer-performed fix:** Fix the code or test, run locally, push.
- **L1 escalation conditions:** Tests fail only due to a shared test environment or service the developer cannot reach.
- **Prod-team conditions:** None.
- **Expected classification:** Self-fix. If failure looks flaky (passes on retry, no change), see JK-06.

## Pattern JK-03: Dependency resolution failure

- **Lifecycle stage:** `ci-build`
- **Failure category:** `dependency`
- **Symptoms:** Build fails resolving a library.
- **Log or event signatures (illustrative):** `Could not resolve dependencies`, `Could not find artifact <g:a:v>`, `npm ERR! 404`, `No matching distribution`.
- **Evidence to collect:**
  - Artifact coordinates and HTTP status.
  - Whether the version was bumped recently.
- **What-changed checks:** Dependency version changes in build files.
- **Possible cause:** Version does not exist, was never published, or repository access is denied.
- **Safe diagnostic checks:**
  - Extract coordinates and status from console.
  - Route to Artifactory module for availability and access.
- **Developer-performed fix:** If the version is wrong or unpublished, correct the version.
- **L1 escalation conditions:** HTTP 401/403 for an artifact that exists (access) → Artifactory AF-02.
- **Prod-team conditions:** Repository manager unavailable for many builds.
- **Expected classification:** Self-fix for wrong versions (404 and recent bump). L1 for access (401/403). Prod team if multi-app outage.

## Pattern JK-04: Build agent unavailable or lost

- **Lifecycle stage:** `ci-build`
- **Failure category:** `platform-infra`
- **Symptoms:** Build waits forever or fails mid-run with agent disconnect.
- **Log or event signatures (illustrative):** `Waiting for next available executor on <label>`, `ChannelClosedException`, `Agent went offline during the build`.
- **Evidence to collect:**
  - Queue reason or disconnect message.
  - Agent label.
  - Other jobs on same label.
- **What-changed checks:** Recent changes to agent label in Jenkinsfile.
- **Possible cause:** Agent pool exhausted, label misspelled, or agent crashed.
- **Safe diagnostic checks:**
  - Read queue item reason.
  - Read node status for the label (if authorized).
  - Check other builds on same label.
- **Developer-performed fix:** If the label was changed by the team and is wrong, correct it in the Jenkinsfile.
- **L1 escalation conditions:** Label is correct and agents are offline or saturated for this team.
- **Prod-team conditions:** Agent pool or controller down for many teams.
- **Expected classification:** L1 (`platform-infra`). Self-fix if the label typo is the cause. Prod team if multi-app.

## Pattern JK-05: Quality Gate stage failed (reported by Jenkins)

- **Lifecycle stage:** `quality-security`
- **Failure category:** `policy-gate`
- **Symptoms:** Jenkins stage 'Quality Gate' fails.
- **Log or event signatures (illustrative):** `QUALITY GATE STATUS: FAILED`, `Pipeline aborted due to quality gate failure: ERROR`.
- **Evidence to collect:**
  - Jenkins gate line.
  - SonarQube task ID or project key from console.
- **What-changed checks:** Code changes in the build; gate or profile changes (see SonarQube).
- **Possible cause:** Usually a SonarQube condition correctly failing. Jenkins is only the reporter.
- **Safe diagnostic checks:**
  - Extract project key and task ID.
  - Walk upstream to SonarQube SQ-01/SQ-02.
- **Developer-performed fix:** Per SonarQube runbook.
- **L1 escalation conditions:** Gate status cannot be retrieved (timeout, webhook missing) → SonarQube SQ-04.
- **Prod-team conditions:** None from Jenkins alone.
- **Expected classification:** Classify from SonarQube evidence; usually Self-fix (`policy-gate`). reported_tool jenkins, primary_tool sonarqube.

## Pattern JK-06: Transient network timeout during build

- **Lifecycle stage:** `ci-build`
- **Failure category:** `transient-flaky`
- **Symptoms:** Build fails on a download or remote call; no related code change.
- **Log or event signatures (illustrative):** `Read timed out`, `Connection reset`, `ETIMEDOUT`, `Temporary failure in name resolution`.
- **Evidence to collect:**
  - Timeout line.
  - Absence of related changes.
  - Previous runs of the same job.
- **What-changed checks:** None found (state explicitly).
- **Possible cause:** Intermittent network or remote service issue.
- **Safe diagnostic checks:**
  - Confirm no related change.
  - Check if previous build had the same error.
- **Developer-performed fix:** Retry the build **once** (developer action).
- **L1 escalation conditions:** Same error recurs after one retry; include both occurrences.
- **Prod-team conditions:** Same timeout across many jobs at the same time.
- **Expected classification:** First occurrence: Self-fix (retry once), Medium confidence. Recurrence: L1 (`transient-flaky`).

## Pattern JK-07: Pipeline credential missing or expired

- **Lifecycle stage:** `ci-build`
- **Failure category:** `credentials-access`
- **Symptoms:** Step fails reading a credential.
- **Log or event signatures (illustrative):** `ERROR: Could not find credentials entry with ID '<id>'`, `401 Unauthorized` in a step using a stored credential.
- **Evidence to collect:**
  - Credential ID (not value).
  - Step that used it.
  - When it last worked.
- **What-changed checks:** Jenkinsfile credential ID edits; credential rotation notices.
- **Possible cause:** Credential ID wrong, removed, or expired.
- **Safe diagnostic checks:**
  - Compare credential ID in Jenkinsfile with last green build.
  - Never read the credential value.
- **Developer-performed fix:** If the ID was changed by the team, restore the correct ID.
- **L1 escalation conditions:** Credential must be created, rotated or scoped by tool admins.
- **Prod-team conditions:** Shared credential expired for many teams.
- **Expected classification:** L1 (`credentials-access`) unless the ID typo is the developer's change.
