# WCNP: runbooks

Failure patterns for WCNP. Signatures and commands are **illustrative** and must be checked against real tool output. Every fix is a **manual action** performed by the developer under the normal change and approval process; TRIAGE-X never performs it.

## Pattern index

| ID | Pattern | Stage | Category | Expected classification |
|---|---|---|---|---|
| WC-01 | Multiple candidate targets in KITT | `deploy` | `unknown` | Status `needs-input`, classification null; ask one question listing the candidates |
| WC-02 | Concord target conflicts with KITT | `deploy` | `configuration` | Status `needs-input`; becomes Self-fix (`configuration`) once the developer confirms |
| WC-03 | Deploy stuck: pods Pending for capacity (multi-app) | `deploy` | `capacity-quota` | Prod team needed; NLH, Jira and Slack after confirmation |
| WC-04 | Rollout progress deadline exceeded | `deploy` | `configuration` | Classify from the underlying pod evidence; usually Self-fix |
| WC-05 | Image pull failure on deploy | `deploy` | `configuration` | Self-fix (wrong tag) or L1 (access); reported_tool wcnp, primary_tool artifactory |
| WC-06 | Platform-wide incident on cluster | `run-operate` | `platform-infra` | Prod team needed (link to existing incident instead if one is found) |

## Pattern WC-01: Multiple candidate targets in KITT

- **Lifecycle stage:** `deploy`
- **Failure category:** `unknown`
- **Symptoms:** "Deployment failed" with no run reference; KITT lists several clusters.
- **Log or event signatures (illustrative):** KITT file with more than one cluster/namespace entry for the app.
- **Evidence to collect:**
  - List of candidate targets from KITT.
  - Absence of a Concord run reference.
- **What-changed checks:** n/a until a target is chosen.
- **Possible cause:** Not yet determinable.
- **Safe diagnostic checks:**
  - List candidates.
  - Do **not** run cluster checks.
- **Developer-performed fix:** n/a.
- **L1 escalation conditions:** n/a.
- **Prod-team conditions:** n/a.
- **Expected classification:** Status `needs-input`, classification null; ask one question listing the candidates.

## Pattern WC-02: Concord target conflicts with KITT

- **Lifecycle stage:** `deploy`
- **Failure category:** `configuration`
- **Symptoms:** Concord log shows a cluster or namespace not in KITT, or different from it.
- **Log or event signatures (illustrative):** Target values in Concord log ≠ KITT entries.
- **Evidence to collect:**
  - Both values with sources.
- **What-changed checks:** KITT edits; flow parameter edits.
- **Possible cause:** Configuration drift between flow and KITT.
- **Safe diagnostic checks:**
  - Show both; no cluster checks.
- **Developer-performed fix:** Developer aligns flow parameters and KITT after confirming intent.
- **L1 escalation conditions:** Neither the developer nor the evidence can determine which is authoritative.
- **Prod-team conditions:** None.
- **Expected classification:** Status `needs-input`; becomes Self-fix (`configuration`) once the developer confirms.

## Pattern WC-03: Deploy stuck: pods Pending for capacity (multi-app)

- **Lifecycle stage:** `deploy`
- **Failure category:** `capacity-quota`
- **Symptoms:** Prod deploy stuck; rollout not progressing.
- **Log or event signatures (illustrative):** `FailedScheduling ... Insufficient cpu` in own namespace and others.
- **Evidence to collect:**
  - Confirmed target (KITT single match + Concord log).
  - Scheduling events.
  - Same events in other namespaces.
- **What-changed checks:** No request increase in this release (if verified).
- **Possible cause:** Cluster capacity exhausted.
- **Safe diagnostic checks:**
  - Kubernetes KB-04 checks on the confirmed target.
  - Blast-radius scan if authorized.
- **Developer-performed fix:** None for the developer.
- **L1 escalation conditions:** Blast radius unknown and only own namespace affected.
- **Prod-team conditions:** Multi-app scheduling failure on the same cluster.
- **Expected classification:** Prod team needed; NLH, Jira and Slack after confirmation.

## Pattern WC-04: Rollout progress deadline exceeded

- **Lifecycle stage:** `deploy`
- **Failure category:** `configuration`
- **Symptoms:** Deploy step times out.
- **Log or event signatures (illustrative):** `ProgressDeadlineExceeded`, `deployment exceeded its progress deadline`.
- **Evidence to collect:**
  - Rollout condition.
  - Pod states (often probe failures or crash loops).
- **What-changed checks:** New release config.
- **Possible cause:** Pods never became ready (see KB-01, KB-06).
- **Safe diagnostic checks:**
  - Kubernetes pod and event checks on confirmed target.
- **Developer-performed fix:** Fix the underlying pod failure.
- **L1 escalation conditions:** Pods healthy but platform reports failure.
- **Prod-team conditions:** Same timeout across many apps on the cluster.
- **Expected classification:** Classify from the underlying pod evidence; usually Self-fix.

## Pattern WC-05: Image pull failure on deploy

- **Lifecycle stage:** `deploy`
- **Failure category:** `configuration`
- **Symptoms:** WCNP deploy fails; pods `ImagePullBackOff`.
- **Log or event signatures (illustrative):** `Failed to pull image ... not found` or `unauthorized`.
- **Evidence to collect:**
  - Event.
  - KITT image tag.
  - Tag existence.
- **What-changed checks:** Image tag change in KITT.
- **Possible cause:** Wrong tag or pull permission.
- **Safe diagnostic checks:**
  - Kubernetes KB-03; walk upstream to Artifactory/Docker.
- **Developer-performed fix:** Correct the tag in KITT.
- **L1 escalation conditions:** Pull permission or pull secret problem.
- **Prod-team conditions:** Registry unreachable from cluster for many apps.
- **Expected classification:** Self-fix (wrong tag) or L1 (access); reported_tool wcnp, primary_tool artifactory.

## Pattern WC-06: Platform-wide incident on cluster

- **Lifecycle stage:** `run-operate`
- **Failure category:** `platform-infra`
- **Symptoms:** App degraded together with other apps on the cluster.
- **Log or event signatures (illustrative):** Node or control-plane events; many namespaces with errors at the same time.
- **Evidence to collect:**
  - Multi-namespace evidence.
  - Platform notice if available.
- **What-changed checks:** No app change correlates.
- **Possible cause:** Platform fault.
- **Safe diagnostic checks:**
  - Blast-radius scan; check for an existing incident before raising a new ticket.
- **Developer-performed fix:** None for the developer.
- **L1 escalation conditions:** Blast radius cannot be verified.
- **Prod-team conditions:** Multi-app impact evidenced and no existing incident ticket covers it.
- **Expected classification:** Prod team needed (link to existing incident instead if one is found).
