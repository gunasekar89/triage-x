# Concord: context

Concord orchestrates delivery flows: it calls builds, gates, publishing and deployments and records task history.

## Role in the lifecycle

Stage 5 (`orchestrate-deliver`). Concord is very often the **reporting** tool for failures whose first failing stage is earlier (2, 3, 4) or later (6). Its logs are also a key source for WCNP target resolution.

## Context to collect

- Process ID, project/org, flow name, status, start and end time.
- Failed task name and sanitized error excerpt.
- Deployment target values printed in the log (environment, cluster, namespace) as placeholders.
- Upstream references: Jenkins build, image tag, artifact version.
- Approval steps and their state.

## Identifiers and target resolution

- Process ID `<process-id>`; Concord instance URL is `<internal-url>`.
- Target values from the log are evidence for WCNP target resolution; compare them with the KITT file.

## Connector and access

- Connector: `TODO(owner)` (Concord API with read-only role).
- Read process status, events and logs for the developer's organization only.

## Relationships to other tools

- Task wraps Jenkins → walk to Jenkins.
- Task waits on Gates → Gates module.
- Deploy task → WCNP / Kubernetes.
- Concord target vs KITT target disagreement → `needs-input` (cross-cutting rule).

## Pilot status

Supporting read-only context in `v0.1.0-pilot`; primary Concord triage is post-pilot.
