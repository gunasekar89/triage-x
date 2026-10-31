# Docker: runbooks

Failure patterns for Docker. Signatures and commands are **illustrative** and must be checked against real tool output. Every fix is a **manual action** performed by the developer under the normal change and approval process; TRIAGE-X never performs it.

## Pattern index

| ID | Pattern | Stage | Category | Expected classification |
|---|---|---|---|---|
| DK-01 | Dockerfile instruction fails | `ci-build` | `code-change` | Self-fix |
| DK-02 | Base image not found or pull denied | `ci-build` | `dependency` | Self-fix for missing tag; L1 for access; Prod team if multi-app |
| DK-03 | Push denied to registry | `package-publish` | `credentials-access` | L1 (`credentials-access`); Self-fix if the path typo is the cause |
| DK-04 | Image pulled at deploy does not exist (wrong tag) | `package-publish` | `configuration` | Self-fix (`configuration`) |
| DK-05 | Build runs out of disk or memory on builder | `ci-build` | `capacity-quota` | Self-fix if the build grew; L1 (`capacity-quota`) otherwise |

## Pattern DK-01: Dockerfile instruction fails

- **Lifecycle stage:** `ci-build`
- **Failure category:** `code-change`
- **Symptoms:** Image build fails at a RUN/COPY step.
- **Log or event signatures (illustrative):** `failed to solve: process "/bin/sh -c <cmd>" did not complete successfully: exit code: 1`, `COPY failed: file not found in build context`.
- **Evidence to collect:**
  - Failing instruction and exit code.
  - Dockerfile diff.
- **What-changed checks:** Dockerfile or build context changes.
- **Possible cause:** Command error or missing file in context (e.g. `.dockerignore`).
- **Safe diagnostic checks:**
  - Read console around the failing step.
  - Compare Dockerfile with last good.
- **Developer-performed fix:** Fix the Dockerfile or build context and rebuild locally first.
- **L1 escalation conditions:** Builder environment lacks a capability the Dockerfile legitimately needs.
- **Prod-team conditions:** None.
- **Expected classification:** Self-fix.

## Pattern DK-02: Base image not found or pull denied

- **Lifecycle stage:** `ci-build`
- **Failure category:** `dependency`
- **Symptoms:** Build fails at `FROM`.
- **Log or event signatures (illustrative):** `pull access denied for <image>`, `manifest unknown`, `not found`.
- **Evidence to collect:**
  - Base image reference.
  - Error type (404 vs 401/403).
- **What-changed checks:** Base image tag change; upstream image retired.
- **Possible cause:** Tag removed/renamed, or credential lacks access.
- **Safe diagnostic checks:**
  - Check base image existence.
  - Distinguish 404 from auth error.
- **Developer-performed fix:** Use an approved existing base image tag.
- **L1 escalation conditions:** Image exists but pull is denied (access).
- **Prod-team conditions:** Shared base image unavailable for many teams.
- **Expected classification:** Self-fix for missing tag; L1 for access; Prod team if multi-app.

## Pattern DK-03: Push denied to registry

- **Lifecycle stage:** `package-publish`
- **Failure category:** `credentials-access`
- **Symptoms:** Publish stage fails on `docker push`.
- **Log or event signatures (illustrative):** `denied: requested access to the resource is denied`, `unauthorized: authentication required`.
- **Evidence to collect:**
  - Error excerpt.
  - Target repository path (placeholder).
- **What-changed checks:** Repository path change; credential rotation.
- **Possible cause:** Pipeline credential lacks push permission or wrong repository path.
- **Safe diagnostic checks:**
  - Compare push target with last good build.
- **Developer-performed fix:** If the path was changed by the team, correct it.
- **L1 escalation conditions:** Permission must be granted.
- **Prod-team conditions:** None unless widespread.
- **Expected classification:** L1 (`credentials-access`); Self-fix if the path typo is the cause.

## Pattern DK-04: Image pulled at deploy does not exist (wrong tag)

- **Lifecycle stage:** `package-publish`
- **Failure category:** `configuration`
- **Symptoms:** `ErrImagePull` / `ImagePullBackOff` at deploy.
- **Log or event signatures (illustrative):** `Failed to pull image "<registry-host>/example-app:1.4.3": ... not found`.
- **Evidence to collect:**
  - Kubernetes event.
  - Tag existence.
  - Tag in KITT vs tags produced by the build.
- **What-changed checks:** KITT tag edit; build publishes a different tag scheme.
- **Possible cause:** Mismatch between published and referenced tag.
- **Safe diagnostic checks:**
  - Compare KITT tag with build-produced tags.
- **Developer-performed fix:** Correct the tag reference.
- **L1 escalation conditions:** Tag exists but cannot be pulled by the cluster (pull secret) → KB-03.
- **Prod-team conditions:** None.
- **Expected classification:** Self-fix (`configuration`).

## Pattern DK-05: Build runs out of disk or memory on builder

- **Lifecycle stage:** `ci-build`
- **Failure category:** `capacity-quota`
- **Symptoms:** Build killed or `no space left on device`.
- **Log or event signatures (illustrative):** `no space left on device`, `signal: killed`, exit code 137.
- **Evidence to collect:**
  - Error and step.
  - Image or context size trend.
- **What-changed checks:** Large files added to context; multi-stage build removed.
- **Possible cause:** Build context or layers too large, or builder capacity exhausted.
- **Safe diagnostic checks:**
  - Compare context size with last good if printed.
- **Developer-performed fix:** Reduce context with `.dockerignore`, use multi-stage builds.
- **L1 escalation conditions:** Builder disk full regardless of image size.
- **Prod-team conditions:** Builder pool exhausted for many teams.
- **Expected classification:** Self-fix if the build grew; L1 (`capacity-quota`) otherwise.
