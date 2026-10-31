# GitHub: context

GitHub hosts application source, pull requests, required checks, workflow definitions and the repository's KITT deployment configuration.

## Role in the lifecycle

Stage 1 (`source-change`). Also the main source of **what-changed** evidence for every later stage, and of KITT files used for WCNP target resolution.

## Context to collect

- Repository (`example-org/example-app`), default branch, PR number and state.
- Required status checks and their state; the check name and the build or analysis it points to.
- Branch protection summary (required reviews, required checks), as far as readable.
- Commits and merged PRs since the last successful build or deploy.
- Workflow files and their recent edits, if GitHub Actions is used (`TODO(owner)`: confirm whether it is).
- KITT file(s) on the deployed branch and their recent history.

## Identifiers and target resolution

- PR reference `example-org/example-app#<n>` or a commit SHA.
- KITT file path: `TODO(owner)` (commonly at the repository root; treat any location as illustrative).
- A KITT file may define **several clusters or configurations**; never assume the first one is the target.

## Connector and access

- Connector: `TODO(owner)` (GitHub MCP, GitHub App or API token with read-only scope).
- Required permission: read access to code, pull requests, checks and commit history for the developer's repositories only.
- GitHub host (cloud or Enterprise): `TODO(owner)`. Never record the real host in results.

## Relationships to other tools

- Required check failing → usually route to Jenkins (`ci-build`) or SonarQube (`quality-security`).
- KITT file → WCNP and Kubernetes target resolution.
- Commit history → what-changed for every stage.

## Pilot status

Supporting context in `v0.1.0-pilot` (KITT files and change history). Primary GitHub triage is post-pilot.
