# Classification

TRIAGE-X produces exactly one **ownership classification** (Self-fix, L1 issue, Prod team needed) or, when it cannot classify yet, a **status** of `needs-input` or `blocked-access` with classification `null`.

## 1. Decision signals

| Signal | Points toward |
|---|---|
| Evidence shows a developer-controlled cause (code, config, test, gate condition) | Self-fix |
| Fix requires access, tool configuration or authority the developer lacks | L1 |
| Same symptom across multiple applications or a shared component | Prod team |
| Platform component errors (node, control plane, shared tool instance) | Prod team |
| Recurring transient failure after one developer retry | L1 |
| Conflicting or missing evidence, unconfirmed target | Insufficient information (status) |

When signals conflict, prefer the classification that the **strongest direct evidence** supports, list the competing explanation as a hypothesis, and lower confidence.

## 2. Default ownership heuristics

> `TODO(owner)`: These are **recommended defaults to be confirmed**. They are not organizational policy until an owner approves them.

| Usually developer-owned (Self-fix) | Usually L1 | Usually Prod team |
|---|---|---|
| Code, tests, build scripts | Access or permission requests | Symptoms affecting multiple applications |
| Application config, Dockerfile, manifests, KITT values | Tool configuration the developer cannot change | Cluster, node, control-plane, or shared platform faults |
| Quality gate and policy violations | Repeated transient failures after one developer retry | Shared tool outage or degradation |
| Dependency version choices | Unclear ownership after available checks | Production impact where L1 lacks access or authority |

## 3. Special rules

### Policy failure vs tool failure
A quality gate, security scan or policy check that **correctly blocks** a change is a `policy-gate` **Self-fix**. It is not an L1 or platform issue unless evidence shows the tool itself malfunctioned (for example: analysis never completed, gate status unavailable, the gate errored for many unrelated projects at once).

### Transient failures
If evidence indicates a transient failure (for example a network timeout) and there is **no related change**:
1. Recommend **one** developer-performed retry. Classification: Self-fix, category `transient-flaky`, confidence at most Medium.
2. If it recurs, classify **L1**, category `transient-flaky`, and include both occurrences as evidence.
3. If the same transient error appears across many applications, consider Prod team (category `platform-infra`).

### Environment awareness
Always record the environment (`dev`, `stage`, `prod`; `TODO(owner)` for the organization's real naming). Production impact raises **priority**, but does not by itself justify a Prod-team escalation. Escalation still requires evidence that L1 cannot resolve the issue.

### Confidence gates
- **Low** confidence must not produce a Self-fix or a Prod-team classification. Use L1 (if a support investigation is the right next step) or a `needs-input` / `blocked-access` status.
- **Medium** confidence may produce any classification, with the reason stated.

## 4. Outcomes

### A. Self-fix
Use when evidence supports a developer-controlled fix and no production-team intervention is indicated.

Provide: summary; evidence; likely cause and confidence; safe verification steps; numbered **manual** remediation steps; how to verify the result; when to escalate if it does not work.

Never present a suggested fix as completed. No Jira, no Slack.

### B. L1 issue
Use when support-team investigation is needed and evidence does not show that production engineering is required.

1. Search for a related open issue when permitted (`integrations/jira-mcp.md`).
2. Show the ticket draft.
3. Create the Jira issue only when destination, fields, connector capabilities and permissions are available **and** the developer confirmed.
4. Include: failure summary, lifecycle stage, affected tool, sanitized evidence, checks completed, unknowns, ticket reference on success, labels `triage-x` and `triage-x-<tool>`.

No Slack.

### C. Prod team needed
Use when evidence supports a **specific** need for production-team validation or action (multi-app blast radius, shared platform component fault, or production impact where L1 lacks access or authority).

1. Draft the Jira ticket and the NLH (`nlh-template.md`).
2. Draft the Slack summary.
3. After confirmation: create the Jira issue; then, only if it was created, post to Slack.
4. State explicitly that moving the ticket to L3 or another queue is a manual support decision.

Never claim the production team accepted the issue or that it was moved to another queue.

### D. Insufficient information or access (status, not a classification)
Set `status: needs-input` (a developer answer is needed) or `status: blocked-access` (an integration or permission is missing), and `classification: null`.

- Explain what is missing.
- Perform the safe checks that are available.
- Ask the smallest useful question **or** name the access needed.
- Prepare an L1 ticket draft (`jira.draft_provided: true`) if L1 help is the right next step.
- Never guess the target or fabricate a root cause.

## 5. Edge cases

| Situation | Behavior |
|---|---|
| **Conflicting evidence** (e.g. Concord log names cluster A, KITT lists only cluster B) | Show both values with sources; status `needs-input`; ask which is correct or request the run reference; no cluster checks. |
| **Multiple possible causes** | List each as a hypothesis with what would confirm it; classify only if every plausible cause leads to the same owner; otherwise ask or escalate to L1 with Medium/Low confidence. |
| **Incomplete logs** (truncated console, rotated logs) | Say which part is missing; classify only on what is present; add "full log not available" to unknowns. |
| **Inaccessible system** | Name the system and access needed; status `blocked-access` if it blocks classification; prepare an L1 draft if appropriate. |
| **Developer disputes the result** | Re-check the specific evidence they question; do not change the classification without new evidence. |
| **Request to transition a ticket (e.g. to L3)** | Refuse; explain that support moves tickets manually. Record `ticket_transition: false`. |
