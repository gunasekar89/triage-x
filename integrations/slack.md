# Slack integration contract

## 1. Destination

| Item | Value |
|---|---|
| Channel name | `#triage-x-alerts` |
| Channel ID | `TODO(owner)` |
| Integration (app/bot/MCP) | `TODO(owner)` |
| Permission scope | Post to this one channel only (`TODO(owner)`: enforce in the integration) |

## 2. When to notify

- **Only** for classification **Prod team needed**.
- **Only after** the Jira issue exists (`jira.created: true` with a key).
- **Only after** the developer confirmed the Slack summary.
- Never in shadow mode.

## 3. Message format

```text
:rotating_light: TRIAGE-X · Prod validation requested
App/Env:      <app> · <env>
Stage/Tool:   <stage> · <tool>
Impact:       <confirmed impact or "unknown">
Blast radius: <single-app | multi-app | unknown>
Ask:          <specific validation requested>
Ticket:       <Jira key>
```

Never include secrets, raw log dumps, real internal URLs, hostnames or employee names.

## 4. Failure handling

| Situation | Behavior |
|---|---|
| Jira creation failed or unverified | Do not post. Report `slack.posted: false`, provide the Slack draft for manual posting once a ticket exists. |
| Slack post failed | Report `actions_taken: {action: slack-post, status: failed}`; give the draft. The Jira ticket stays as created. |
| Slack result ambiguous | Report `unverified`; do not repost blindly; ask the developer to check the channel. |
| Channel ID not configured | Do not post; provide the draft; note `TODO(owner)`. |

Never claim a message was posted unless the integration confirms success.
