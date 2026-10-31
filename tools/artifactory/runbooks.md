# Artifactory: runbooks

Failure patterns for Artifactory. Signatures and commands are **illustrative** and must be checked against real tool output. Every fix is a **manual action** performed by the developer under the normal change and approval process; TRIAGE-X never performs it.

## Pattern index

| ID | Pattern | Stage | Category | Expected classification |
|---|---|---|---|---|
| AF-01 | Artifact version not found | `package-publish` | `dependency` | Self-fix (`dependency`) when the version does not exist |
| AF-02 | Access denied pulling an existing artifact | `package-publish` | `credentials-access` | L1 (`credentials-access`), labels `triage-x`, `triage-x-artifactory` |
| AF-03 | Image tag missing for deployment | `package-publish` | `configuration` | Self-fix (`configuration`) |
| AF-04 | Publish rejected: version already exists | `package-publish` | `configuration` | Self-fix (`configuration`) |
| AF-05 | Storage quota or size limit exceeded | `package-publish` | `capacity-quota` | Self-fix if artifact grew unexpectedly; otherwise L1 (`capacity-quota`) |
| AF-06 | Repository unavailable or slow | `package-publish` | `platform-infra` | First occurrence Self-fix (retry, `transient-flaky`); recurrence L1; multi-app Prod team (`platform-infra`) |

## Pattern AF-01: Artifact version not found

- **Lifecycle stage:** `package-publish`
- **Failure category:** `dependency`
- **Symptoms:** Build cannot resolve a dependency version.
- **Log or event signatures (illustrative):** `Could not find artifact com.example:example-lib:jar:2.3.1`, `404 Not Found`.
- **Evidence to collect:**
  - Coordinates and 404.
  - Existence check result.
- **What-changed checks:** Recent version bump.
- **Possible cause:** Version never published, typo, or wrong repository.
- **Safe diagnostic checks:**
  - Check existence of the exact version.
  - List available versions if authorized.
- **Developer-performed fix:** Correct the version or publish it from its owning build.
- **L1 escalation conditions:** Version exists in another repository but is not visible through the virtual repository.
- **Prod-team conditions:** None.
- **Expected classification:** Self-fix (`dependency`) when the version does not exist.

## Pattern AF-02: Access denied pulling an existing artifact

- **Lifecycle stage:** `package-publish`
- **Failure category:** `credentials-access`
- **Symptoms:** 403/401 for an artifact that others can resolve.
- **Log or event signatures (illustrative):** `status code: 403, reason phrase: Forbidden`, `401 Unauthorized`.
- **Evidence to collect:**
  - HTTP status and coordinates.
  - Existence for other consumers (if authorized).
- **What-changed checks:** Credential rotation; permission target changes.
- **Possible cause:** Pipeline credential lacks read permission on the repository.
- **Safe diagnostic checks:**
  - Confirm the artifact exists.
  - Confirm the status is auth-related, not 404.
- **Developer-performed fix:** None for the developer (cannot change repository permissions).
- **L1 escalation conditions:** Always: permission must be granted or credential fixed.
- **Prod-team conditions:** Many pipelines denied at once (shared credential or permission outage).
- **Expected classification:** L1 (`credentials-access`), labels `triage-x`, `triage-x-artifactory`.

## Pattern AF-03: Image tag missing for deployment

- **Lifecycle stage:** `package-publish`
- **Failure category:** `configuration`
- **Symptoms:** Deployment `ImagePullBackOff`; `manifest unknown`.
- **Log or event signatures (illustrative):** `manifest for <registry-host>/example-app:1.4.2 not found: manifest unknown`.
- **Evidence to collect:**
  - Kubernetes event.
  - Tag existence check.
  - KITT image tag.
- **What-changed checks:** KITT tag edit; publish stage skipped or failed.
- **Possible cause:** Tag never pushed or KITT references a wrong tag.
- **Safe diagnostic checks:**
  - Check tag existence.
  - Check the publish stage of the build that should have produced it.
- **Developer-performed fix:** Correct the tag in KITT or re-run the publish (developer action).
- **L1 escalation conditions:** Tag exists but cannot be pulled (see AF-02).
- **Prod-team conditions:** None.
- **Expected classification:** Self-fix (`configuration`).

## Pattern AF-04: Publish rejected: version already exists

- **Lifecycle stage:** `package-publish`
- **Failure category:** `configuration`
- **Symptoms:** Publish step fails on re-release.
- **Log or event signatures (illustrative):** `409 Conflict`, `Redeploy not allowed`.
- **Evidence to collect:**
  - Status and coordinates.
- **What-changed checks:** Version not bumped.
- **Possible cause:** Release repository forbids overwriting a version.
- **Safe diagnostic checks:**
  - Confirm version exists already.
- **Developer-performed fix:** Bump the version and publish again.
- **L1 escalation conditions:** Snapshot repository wrongly configured as immutable.
- **Prod-team conditions:** None.
- **Expected classification:** Self-fix (`configuration`).

## Pattern AF-05: Storage quota or size limit exceeded

- **Lifecycle stage:** `package-publish`
- **Failure category:** `capacity-quota`
- **Symptoms:** Publish fails with quota or size error.
- **Log or event signatures (illustrative):** `413 Request Entity Too Large`, `quota exceeded`.
- **Evidence to collect:**
  - Status and artifact size.
- **What-changed checks:** Artifact size growth; new large files included.
- **Possible cause:** Artifact too large or repository quota reached.
- **Safe diagnostic checks:**
  - Compare artifact size with previous builds.
- **Developer-performed fix:** Remove unintended large content from the artifact.
- **L1 escalation conditions:** Quota needs raising.
- **Prod-team conditions:** Repository-wide storage exhaustion affecting many apps.
- **Expected classification:** Self-fix if artifact grew unexpectedly; otherwise L1 (`capacity-quota`).

## Pattern AF-06: Repository unavailable or slow

- **Lifecycle stage:** `package-publish`
- **Failure category:** `platform-infra`
- **Symptoms:** 5xx errors or timeouts on resolve or push.
- **Log or event signatures (illustrative):** `502 Bad Gateway`, `503 Service Unavailable`, `Read timed out` against `<registry-host>`.
- **Evidence to collect:**
  - Errors and timestamps.
  - Other builds affected (if visible).
- **What-changed checks:** Platform notices.
- **Possible cause:** Artifactory or network issue.
- **Safe diagnostic checks:**
  - Check whether the error is consistent or intermittent.
  - Blast-radius check.
- **Developer-performed fix:** Retry once if transient.
- **L1 escalation conditions:** Recurs after one retry; blast radius unknown.
- **Prod-team conditions:** Multiple applications affected at the same time.
- **Expected classification:** First occurrence Self-fix (retry, `transient-flaky`); recurrence L1; multi-app Prod team (`platform-infra`).
