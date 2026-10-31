# Kubernetes: runbooks

Failure patterns for Kubernetes. Signatures and commands are **illustrative** and must be checked against real tool output. Every fix is a **manual action** performed by the developer under the normal change and approval process; TRIAGE-X never performs it.

## Pattern index

| ID | Pattern | Stage | Category | Expected classification |
|---|---|---|---|---|
| KB-01 | CrashLoopBackOff after new release | `run-operate` | `code-change` | Self-fix, High when logs show the error |
| KB-02 | OOMKilled | `run-operate` | `capacity-quota` | Self-fix (`capacity-quota`) |
| KB-03 | ImagePullBackOff | `deploy` | `configuration` | Self-fix (wrong tag) or L1 (`credentials-access`); first_failing usually `package-publish` |
| KB-04 | Pods Pending: insufficient resources | `deploy` | `capacity-quota` | Self-fix if own requests grew; Prod team (`capacity-quota`/`platform-infra`) when multi-app; L1 when unknown |
| KB-05 | Namespace quota exceeded | `deploy` | `capacity-quota` | Self-fix or L1 (`capacity-quota`) |
| KB-06 | Readiness/liveness probe failures | `run-operate` | `configuration` | Self-fix (`configuration`) |
| KB-07 | Admission policy denied | `deploy` | `policy-gate` | Self-fix (`policy-gate`); Prod team if the webhook itself is failing cluster-wide |
| KB-08 | Node NotReady affecting workloads | `run-operate` | `platform-infra` | Prod team (`platform-infra`) when evidenced; else L1 with blast radius unknown |

## Pattern KB-01: CrashLoopBackOff after new release

- **Lifecycle stage:** `run-operate`
- **Failure category:** `code-change`
- **Symptoms:** Pods restart repeatedly after deploy.
- **Log or event signatures (illustrative):** `Back-off restarting failed container`, state `CrashLoopBackOff`, exit code 1.
- **Evidence to collect:**
  - Pod status and restart count.
  - Last log lines (sanitized).
  - New image tag.
- **What-changed checks:** New image or config in this rollout.
- **Possible cause:** Application error at startup (bad config, missing env var, code bug).
- **Safe diagnostic checks:**
  - Describe pod.
  - Read previous logs tail.
- **Developer-performed fix:** Fix the application or config; roll forward or ask for a rollback through the normal process (developer action).
- **L1 escalation conditions:** Crash caused by a platform-provided dependency the developer cannot change.
- **Prod-team conditions:** Many apps crash-looping on the same cluster at once.
- **Expected classification:** Self-fix, High when logs show the error.

## Pattern KB-02: OOMKilled

- **Lifecycle stage:** `run-operate`
- **Failure category:** `capacity-quota`
- **Symptoms:** Containers terminated with OOMKilled.
- **Log or event signatures (illustrative):** `Last State: Terminated, Reason: OOMKilled`, exit code 137.
- **Evidence to collect:**
  - Termination reason.
  - Memory limit.
  - Recent memory-related changes.
- **What-changed checks:** Limit change; new release with higher memory use.
- **Possible cause:** Memory limit too low or memory leak.
- **Safe diagnostic checks:**
  - Describe pod.
  - Compare limits with previous release.
- **Developer-performed fix:** Adjust memory limits in KITT/manifest or fix memory use.
- **L1 escalation conditions:** Limit increase blocked by quota the developer cannot raise.
- **Prod-team conditions:** Node-level memory pressure affecting many apps.
- **Expected classification:** Self-fix (`capacity-quota`).

## Pattern KB-03: ImagePullBackOff

- **Lifecycle stage:** `deploy`
- **Failure category:** `configuration`
- **Symptoms:** Pods cannot start; image pull fails.
- **Log or event signatures (illustrative):** `Failed to pull image`, `ErrImagePull`, `ImagePullBackOff`; sub-reason `not found` or `unauthorized`.
- **Evidence to collect:**
  - Event message.
  - Image reference.
  - Tag existence (Artifactory).
- **What-changed checks:** Image tag change; pull-secret change.
- **Possible cause:** Wrong tag (configuration) or pull credential problem (credentials-access).
- **Safe diagnostic checks:**
  - Read events.
  - Distinguish not-found vs unauthorized.
  - Walk upstream to Artifactory/Docker.
- **Developer-performed fix:** Correct the tag.
- **L1 escalation conditions:** Pull secret or registry permission problem.
- **Prod-team conditions:** Registry unreachable from the cluster for many apps.
- **Expected classification:** Self-fix (wrong tag) or L1 (`credentials-access`); first_failing usually `package-publish`.

## Pattern KB-04: Pods Pending: insufficient resources

- **Lifecycle stage:** `deploy`
- **Failure category:** `capacity-quota`
- **Symptoms:** Rollout stuck; pods Pending.
- **Log or event signatures (illustrative):** `FailedScheduling: 0/<n> nodes are available: <n> Insufficient cpu`.
- **Evidence to collect:**
  - Scheduling events.
  - Requests per pod.
  - Same events in other namespaces (if authorized).
- **What-changed checks:** Request increase; replica increase.
- **Possible cause:** Requests too large for nodes, or cluster capacity exhausted.
- **Safe diagnostic checks:**
  - Read events.
  - Compare requests with previous release.
  - Cluster-wide scan if authorized.
- **Developer-performed fix:** If requests grew unintentionally, reduce them.
- **L1 escalation conditions:** Single app affected and requests are reasonable.
- **Prod-team conditions:** Same FailedScheduling across multiple namespaces/apps on the cluster.
- **Expected classification:** Self-fix if own requests grew; Prod team (`capacity-quota`/`platform-infra`) when multi-app; L1 when unknown.

## Pattern KB-05: Namespace quota exceeded

- **Lifecycle stage:** `deploy`
- **Failure category:** `capacity-quota`
- **Symptoms:** ReplicaSet cannot create pods.
- **Log or event signatures (illustrative):** `exceeded quota: <quota-name>, requested: ..., used: ..., limited: ...`.
- **Evidence to collect:**
  - Quota event.
  - Quota usage.
- **What-changed checks:** Replica or resource increase.
- **Possible cause:** Namespace quota reached.
- **Safe diagnostic checks:**
  - Read resourcequota usage.
- **Developer-performed fix:** Reduce requests/replicas or clean up unused workloads in the namespace.
- **L1 escalation conditions:** Quota increase needed.
- **Prod-team conditions:** None.
- **Expected classification:** Self-fix or L1 (`capacity-quota`).

## Pattern KB-06: Readiness/liveness probe failures

- **Lifecycle stage:** `run-operate`
- **Failure category:** `configuration`
- **Symptoms:** Pods running but not ready, or restarted by liveness probe.
- **Log or event signatures (illustrative):** `Readiness probe failed: HTTP probe failed with statuscode: 503`, `Liveness probe failed`.
- **Evidence to collect:**
  - Probe events.
  - Probe config.
  - App startup time.
- **What-changed checks:** Probe path/port change; slower startup in new release.
- **Possible cause:** Probe misconfigured or app too slow to start.
- **Safe diagnostic checks:**
  - Describe pod.
  - Compare probe config.
- **Developer-performed fix:** Fix probe path/port or add startup delay.
- **L1 escalation conditions:** Probe fails due to a dependency the developer cannot reach.
- **Prod-team conditions:** None.
- **Expected classification:** Self-fix (`configuration`).

## Pattern KB-07: Admission policy denied

- **Lifecycle stage:** `deploy`
- **Failure category:** `policy-gate`
- **Symptoms:** Deploy rejected by admission controller.
- **Log or event signatures (illustrative):** `admission webhook "<name>" denied the request: <reason>`.
- **Evidence to collect:**
  - Denial message.
- **What-changed checks:** Manifest change that violates policy; new policy.
- **Possible cause:** Manifest violates a cluster policy (e.g. privileged container, missing labels).
- **Safe diagnostic checks:**
  - Read the denial reason.
- **Developer-performed fix:** Change the manifest to comply.
- **L1 escalation conditions:** Policy appears to reject compliant manifests.
- **Prod-team conditions:** Webhook failing (timeouts) for all deployments on cluster.
- **Expected classification:** Self-fix (`policy-gate`); Prod team if the webhook itself is failing cluster-wide.

## Pattern KB-08: Node NotReady affecting workloads

- **Lifecycle stage:** `run-operate`
- **Failure category:** `platform-infra`
- **Symptoms:** Pods evicted or unknown; several apps affected.
- **Log or event signatures (illustrative):** `NodeNotReady`, pod status `Unknown`, `Evicted` with node pressure.
- **Evidence to collect:**
  - Node conditions (if authorized).
  - Affected namespaces.
- **What-changed checks:** Platform notices.
- **Possible cause:** Node or infrastructure failure.
- **Safe diagnostic checks:**
  - Read events for node-related reasons.
  - Blast-radius scan if authorized.
- **Developer-performed fix:** None for the developer.
- **L1 escalation conditions:** Only own pods visible; cannot see node state.
- **Prod-team conditions:** Node issue confirmed or multi-app impact.
- **Expected classification:** Prod team (`platform-infra`) when evidenced; else L1 with blast radius unknown.
