# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses semantic versioning.

## [Unreleased] — v0.1.0-pilot

### Changed
- Replaced WCNP with CD Orchestration tools (AKS, GKE, EKS); the tool id is now `cd-orchestration` (module, schema enum, examples and evaluation cases renamed; pattern IDs CO-xx).

### Added
- Self-service RCA: `core/self-rca.md`, optional `rca` object in `triage_result` (additive, schema stays 1.0), Self-RCA block in results and Jira tickets.
- Initial scaffold: `SKILL.md`, core reasoning documents, output contract and `triage_result` schema v1.0.
- Tool modules for GitHub, Jenkins, Concord, Gates, SonarQube, Artifactory, Docker, Kubernetes and CD Orchestration tools (AKS, GKE, EKS), each with 5–8 failure patterns, plus a module template.
- Jira MCP and Slack integration contracts (organization details as `TODO(owner)`).
- Synthetic example inputs and schema-validated expected outputs, including the four worked examples and a cross-tool case.
- Evaluation cases (four or more per tool, plus cross-cutting safety cases) and `tests/validate.py`.
- Architecture, extension, evaluation and USA-integration docs.
