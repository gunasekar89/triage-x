# Kubernetes: context

Kubernetes runs application workloads. TRIAGE-X reads workload, pod, event and rollout status through authorized read-only access.

## Role in the lifecycle

Stage 6 (`deploy`) and stage 7 (`run-operate`). Cluster-specific checks require a **confirmed target** (cluster and namespace).

## Context to collect

- Deployment/StatefulSet status, desired vs ready replicas, rollout condition.
- Pod phase, container state and reason (`CrashLoopBackOff`, `OOMKilled`, `ImagePullBackOff`).
- Recent events in the namespace (`FailedScheduling`, `FailedMount`, `BackOff`).
- Resource requests/limits and namespace quota usage.
- Last container log lines (sanitized) for crashing containers.

## Identifiers and target resolution

- Cluster `<cluster-name>`, namespace `<namespace>`, workload `example-app`.
- Target must be confirmed via CD Orchestration tools (AKS, GKE, EKS) target resolution before any check.

## Connector and access

- Connector: `TODO(owner)` (read-only RBAC: get/list/watch on pods, events, deployments, replicasets, resourcequotas in the developer's namespaces).
- Cluster-wide reads (nodes, other namespaces) only if granted; otherwise blast radius is `unknown`.

## Relationships to other tools

- Often invoked from the CD Orchestration tools (AKS, GKE, EKS) module, which supplies the confirmed target.
- Image pull failures → Artifactory / Docker.

## Pilot status

Post-pilot as a primary module; during the pilot Kubernetes checks run as part of CD Orchestration tools (AKS, GKE, EKS) triage (module `tools/cd-orchestration/`).
