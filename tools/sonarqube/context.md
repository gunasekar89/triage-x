# SonarQube: context

SonarQube analyses code quality, coverage and security hotspots and evaluates a quality gate per project.

## Role in the lifecycle

Stage 3 (`quality-security`). Usually **reported** by Jenkins (`Quality Gate` stage) or Concord.

## Context to collect

- Project key, branch or PR, analysis ID / CE task ID.
- Quality gate status and each condition: metric, operator, threshold, actual value.
- New-code period definition (as configured).
- Top new issues (rule, severity, file) where relevant.

## Identifiers and target resolution

- Project key `example-app`; SonarQube URL is `<internal-url>` in all results.
- Jenkins console usually prints the CE task ID and project key.

## Connector and access

- Connector: `TODO(owner)` (SonarQube API token with Browse permission on the developer's projects).

## Relationships to other tools

- Jenkins `Quality Gate` stage reports SonarQube gate status.
- Gate status unavailable often means analysis never finished or the webhook is missing.

## Pilot status

**Primary** in `v0.1.0-pilot`.
