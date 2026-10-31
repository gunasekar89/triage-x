# Example 3 — Prod team needed (platform capacity)

> Synthetic.

**Developer input**

> example-app prod deploy stuck.

**Evidence available (synthetic)**

- KITT file: exactly one `prod` entry → cluster `<cluster-name>`, namespace `example-app-prod`.
- Concord process `<process-id>` log: `deploying to cluster=<cluster-name> namespace=example-app-prod`.
- Kubernetes (read-only, confirmed target):
  ```text
  pod/example-app-7d9f-abcde   0/1   Pending
  Warning  FailedScheduling  0/12 nodes are available: 12 Insufficient cpu.
  ```
- Cluster-wide event scan (authorized): the same `Insufficient cpu` FailedScheduling events in 7 other namespaces in the last 30 minutes.
- Release did not change CPU requests (KITT diff).
