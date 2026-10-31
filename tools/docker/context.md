# Docker: context

Docker covers image builds (Dockerfile, build context, base images) and registry operations (push, pull, tags).

## Role in the lifecycle

Stage 2 (`ci-build`, image build) and stage 4 (`package-publish`, registry). Registry errors overlap with Artifactory when Artifactory hosts the registry.

## Context to collect

- Dockerfile path and the failing instruction (as reported).
- Base image reference and tag/digest.
- Image reference being pushed or pulled, as a placeholder.
- Builder in use (`docker build`, BuildKit, Kaniko, etc.: `TODO(owner)`).

## Identifiers and target resolution

- Image `<registry-host>/example-app:<tag>`; never record the real registry host.

## Connector and access

- Connector: none expected directly; evidence comes from Jenkins console and registry (Artifactory) checks. `TODO(owner)`.

## Relationships to other tools

- Build failures appear in Jenkins console.
- Registry pull failures appear in Kubernetes events; check Artifactory.

## Pilot status

Post-pilot. Image build errors in Jenkins logs are handled as Jenkins evidence during the pilot.
