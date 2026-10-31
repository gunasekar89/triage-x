# Jenkins: context

Jenkins runs CI builds: compile, test, package, and often invokes quality gates and publishing.

## Role in the lifecycle

Stage 2 (`ci-build`). Jenkins frequently **reports** failures whose first failing stage is 3 (SonarQube gate) or 4 (publish).

## Context to collect

- Job name and build number (`example-app #142`), result, duration.
- Failed stage name and the sanitized console excerpt around the first error.
- Agent label and node the build ran on (as a placeholder).
- Previous build result and the commits between the last green and the failing build.
- Test report summary (failed test names, counts).
- Downstream references printed in the console: SonarQube task ID, artifact coordinates, image tag.

## Identifiers and target resolution

- Job path and build number. Jenkins instance URL is `<internal-url>` in all results.
- Multibranch jobs: branch or PR number is part of the job path.

## Connector and access

- Connector: `TODO(owner)` (Jenkins MCP or API user with read-only Overall/Read and Job/Read).
- Console logs may be large: fetch the tail and the region around the first `ERROR`/`FAILURE`.
- Job configuration (Jenkinsfile) is read from the repository, not from Jenkins, where possible.

## Relationships to other tools

- Quality Gate stage → SonarQube module.
- Publish / push stage → Artifactory or Docker module.
- Called by Concord → Concord shows the symptom; Jenkins (or further upstream) holds the cause.

## Pilot status

**Primary** in `v0.1.0-pilot`.
