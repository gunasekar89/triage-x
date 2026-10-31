# Artifactory: context

Artifactory stores build artifacts, dependencies and container images.

## Role in the lifecycle

Stage 4 (`package-publish`). Failures are often **reported** in Jenkins (stage 2) or Kubernetes/CD Orchestration tools (AKS, GKE, EKS) (stage 6, image pull).

## Context to collect

- Repository key, artifact coordinates or image reference (as placeholders).
- HTTP status of the failing request and operation (pull, push, resolve).
- Whether the artifact or tag exists (if authorized to check).
- Whether other consumers can retrieve the same artifact.

## Identifiers and target resolution

- Maven-style `com.example:example-lib:2.3.1`, npm `@example/lib@2.3.1`, image `<registry-host>/example-app:1.4.2`.
- Artifactory URL is `<internal-url>` in all results.

## Connector and access

- Connector: `TODO(owner)` (Artifactory API with read-only access to relevant repositories).
- TRIAGE-X must not create, delete, move or re-permission artifacts.

## Relationships to other tools

- Jenkins dependency resolution → AF-01/AF-02.
- Kubernetes `ImagePullBackOff` → AF-03/AF-02 and Docker DK-04.

## Pilot status

Post-pilot. During the pilot, Artifactory evidence printed in Jenkins logs or Kubernetes events is used as supporting context.
