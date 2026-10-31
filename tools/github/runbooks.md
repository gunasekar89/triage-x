# GitHub: runbooks

Failure patterns for GitHub. Signatures and commands are **illustrative** and must be checked against real tool output. Every fix is a **manual action** performed by the developer under the normal change and approval process; TRIAGE-X never performs it.

## Pattern index

| ID | Pattern | Stage | Category | Expected classification |
|---|---|---|---|---|
| GH-01 | Required status check failing | `source-change` | `code-change` | Self-fix in most cases (classify by the upstream tool's finding) |
| GH-02 | Merge conflict blocks PR | `source-change` | `code-change` | Self-fix |
| GH-03 | Branch protection requires reviews or checks not met | `source-change` | `policy-gate` | Self-fix (`policy-gate`) |
| GH-04 | Workflow file invalid or failing to start | `source-change` | `configuration` | Self-fix |
| GH-05 | Repository access denied to pipeline | `source-change` | `credentials-access` | L1 (`credentials-access`) |
| GH-06 | KITT file change introduced bad deploy config | `source-change` | `configuration` | Self-fix, Medium-High confidence when the changed key matches the error |

## Pattern GH-01: Required status check failing

- **Lifecycle stage:** `source-change`
- **Failure category:** `code-change`
- **Symptoms:** PR cannot merge; a required check is red.
- **Log or event signatures (illustrative):** `Required status check "<check-name>" is failing`; check conclusion `failure`.
- **Evidence to collect:**
  - Check name, conclusion and target (build or analysis ref).
  - Head SHA and the commits in the PR.
- **What-changed checks:** Commits in the PR; any edits to build or test files.
- **Possible cause:** The underlying build or analysis failed; GitHub is only reporting it.
- **Safe diagnostic checks:**
  - List check runs for the head SHA.
  - Follow the check to its Jenkins build or SonarQube analysis and route there.
- **Developer-performed fix:** Fix per the upstream tool's runbook, push a new commit, let the check re-run.
- **L1 escalation conditions:** Check points to a tool the developer cannot open, or the check never reports a result for over `TODO(owner)` minutes.
- **Prod-team conditions:** Not usually. Only if the reporting integration is failing for many repositories.
- **Expected classification:** Self-fix in most cases (classify by the upstream tool's finding). L1 if the check is stuck with no upstream result.

## Pattern GH-02: Merge conflict blocks PR

- **Lifecycle stage:** `source-change`
- **Failure category:** `code-change`
- **Symptoms:** PR shows 'This branch has conflicts that must be resolved'.
- **Log or event signatures (illustrative):** `mergeable: false`, `mergeable_state: dirty`; `CONFLICT (content): Merge conflict in <file>`.
- **Evidence to collect:**
  - PR mergeable state.
  - Conflicting files if exposed.
- **What-changed checks:** Recent merges to the base branch touching the same files.
- **Possible cause:** Base branch changed the same lines.
- **Safe diagnostic checks:**
  - Read PR mergeable state.
  - Compare base and head for overlapping files.
- **Developer-performed fix:**
  - Update the branch from base locally.
  - Resolve conflicts, run tests, push.
- **L1 escalation conditions:** Never for a plain conflict.
- **Prod-team conditions:** None.
- **Expected classification:** Self-fix. High confidence when mergeable_state is `dirty`.

## Pattern GH-03: Branch protection requires reviews or checks not met

- **Lifecycle stage:** `source-change`
- **Failure category:** `policy-gate`
- **Symptoms:** Merge button disabled though checks are green.
- **Log or event signatures (illustrative):** `Review required`, `At least <n> approving review is required`, `Required check is expected`.
- **Evidence to collect:**
  - Protection summary.
  - Review state on the PR.
- **What-changed checks:** Recent change to branch protection or CODEOWNERS (if visible).
- **Possible cause:** A policy correctly requires approval or a check that has not run.
- **Safe diagnostic checks:**
  - Read PR reviews and requested reviewers.
  - Read required checks list and compare to reported checks.
- **Developer-performed fix:** Request review from the required owners; ensure the required check name matches the pipeline's reported name.
- **L1 escalation conditions:** A required check name no longer exists in any pipeline (stale protection rule) and the developer cannot change protection.
- **Prod-team conditions:** None.
- **Expected classification:** Self-fix (`policy-gate`). L1 with category `configuration` if the rule references a check that can never report.

## Pattern GH-04: Workflow file invalid or failing to start

- **Lifecycle stage:** `source-change`
- **Failure category:** `configuration`
- **Symptoms:** Workflow does not run or fails immediately.
- **Log or event signatures (illustrative):** `Invalid workflow file`, `The workflow is not valid`, `Unexpected value`.
- **Evidence to collect:**
  - Workflow run annotation.
  - Diff of the workflow file.
- **What-changed checks:** Recent edits to workflow files.
- **Possible cause:** Syntax or schema error in the workflow definition.
- **Safe diagnostic checks:**
  - Read latest run annotations.
  - Compare workflow file with last working version.
- **Developer-performed fix:** Correct the workflow file and push.
- **L1 escalation conditions:** Workflow uses an organization runner group or shared action the developer cannot access.
- **Prod-team conditions:** None.
- **Expected classification:** Self-fix. L1 if the failure is a runner or permission the developer cannot change.

## Pattern GH-05: Repository access denied to pipeline

- **Lifecycle stage:** `source-change`
- **Failure category:** `credentials-access`
- **Symptoms:** Jenkins or Concord cannot clone or fetch the repository.
- **Log or event signatures (illustrative):** `remote: Repository not found.`, `fatal: Authentication failed`, `403` on clone.
- **Evidence to collect:**
  - Sanitized error from the cloning tool.
  - Whether the repo was renamed, moved or made private recently.
- **What-changed checks:** Repository rename or transfer; credential rotation; team access change.
- **Possible cause:** The pipeline's credential lacks access, or the repository path changed.
- **Safe diagnostic checks:**
  - Confirm repository exists at the referenced path (as the developer).
  - Check recent rename/transfer events if visible.
- **Developer-performed fix:** If the repository was renamed by the team, update the pipeline's repository reference.
- **L1 escalation conditions:** Pipeline service credential needs access granted or rotated.
- **Prod-team conditions:** Many pipelines fail to clone at once (shared credential or SCM outage).
- **Expected classification:** L1 (`credentials-access`). Self-fix only if the developer's own rename caused it. Prod team if multi-app.

## Pattern GH-06: KITT file change introduced bad deploy config

- **Lifecycle stage:** `source-change`
- **Failure category:** `configuration`
- **Symptoms:** Deploy fails right after a PR that edited the KITT file.
- **Log or event signatures (illustrative):** Deploy error naming a KITT key; schema or validation error in Concord or WCNP.
- **Evidence to collect:**
  - Diff of the KITT file in the last merge.
  - Deploy error referencing the changed key.
- **What-changed checks:** KITT file commits between last good and failing deploy.
- **Possible cause:** Typo, wrong cluster or namespace, invalid value in the KITT change.
- **Safe diagnostic checks:**
  - Diff KITT file at last good and failing refs.
  - Match changed keys to the deploy error.
- **Developer-performed fix:** Revert or correct the KITT change through a new PR.
- **L1 escalation conditions:** Deploy error references a platform-side setting the developer cannot see.
- **Prod-team conditions:** None, unless the platform rejects valid config for many apps.
- **Expected classification:** Self-fix, Medium-High confidence when the changed key matches the error.
