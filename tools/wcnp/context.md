# WCNP: context

WCNP is the internal container platform that deploys and runs applications on Kubernetes clusters, driven by Concord flows and the repository's KITT configuration. Platform internals and APIs are `TODO(owner)`.

## Role in the lifecycle

Stage 6 (`deploy`) and stage 7 (`run-operate`). WCNP triage owns **target resolution**: derive environment, cluster and namespace before any cluster-specific check.

## Context to collect

- KITT file(s) from GitHub: candidate environments, clusters, namespaces (illustrative structure only).
- Concord deploy process log: target values actually used.
- Deployment status and Kubernetes evidence for the confirmed target.
- Platform notices for the cluster (`TODO(owner)`).

## Identifiers and target resolution

- App `example-app`, environment `dev|stage|prod` (`TODO(owner)` naming), cluster `<cluster-name>`, namespace `<namespace>`.

## Connector and access

- Connector: `TODO(owner)` (WCNP API, or Kubernetes read-only access plus Concord and GitHub reads).

## Relationships to other tools

- Target resolution uses GitHub (KITT) and Concord (log).
- Runtime checks use the Kubernetes module.
- Image issues → Artifactory/Docker.

## Pilot status

**Primary** in `v0.1.0-pilot`.

## Target resolution rules

1. Read the repository's KITT file(s). A KITT file may contain **multiple clusters or configurations**; list every candidate `(environment, cluster, namespace)`.
2. Read the Concord deploy process log, if a run reference is available, and extract the target values it used.
3. Reconcile:
   - **Exactly one** candidate supported by evidence (e.g. a single KITT entry for the environment that matches the Concord log) → target confirmed; record the evidence in `target.source` and set `target.confirmed: true`.
   - **Several** plausible candidates → present them as a numbered list and ask the developer to select one (`status: needs-input`).
   - **Sources disagree** (Concord used a cluster not in KITT, or a different namespace) → state the conflict with both sources and ask for clarification or more evidence (`status: needs-input`).
4. **Never run cluster-specific checks against an unconfirmed target.**
5. KITT examples in this repository (`examples/inputs/kitt-multi-target.example.yml`) are illustrative. Do not assume undocumented internal schema details are authoritative; the real KITT schema is `TODO(owner)`.
