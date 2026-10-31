# Unified Support Agent integration

> **Decision pending: `TODO(owner)`.** TRIAGE-X may later be integrated into a Unified Support Agent (USA). Nothing in this repository assumes it will be.

## What TRIAGE-X offers a USA

- A **single entry point** (`SKILL.md`) that accepts a developer request about a delivery failure.
- A **stable result**: `triage_result` (schema version `1.0`), validated by `schemas/triage-result.schema.json`.
- **Explicit status** (`complete`, `needs-input`, `blocked-access`) and at most one open question, so a USA can continue the conversation.
- **Declared side effects**: `actions_taken`, `jira`, and `slack` blocks say exactly what was written.

## Proposed boundary

| Concern | Owner if integrated |
|---|---|
| Conversation, identity, channel | USA |
| Choosing TRIAGE-X for a delivery failure | USA router |
| Stage/tool routing, evidence, classification | TRIAGE-X |
| Developer confirmation before writes | Whoever presents the draft, under the same rules |
| Jira/Slack execution | `TODO(owner)`: TRIAGE-X or USA; contracts in `integrations/` apply either way |
| Metrics collection from `triage_result` | `TODO(owner)` |

## Open questions

- Does USA call TRIAGE-X as a skill, a sub-agent, or a tool? `TODO(owner)`
- Does USA pass prior conversation context, and how is it sanitized? `TODO(owner)`
- Who owns the Jira write permission in an integrated setup? `TODO(owner)`
