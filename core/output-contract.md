# Output contract

Every triage returns the same **two-part** result. Schema: `schemas/triage-result.schema.json` (version `1.0`).

## Part 1: Human-readable result

```text
TRIAGE-X Result · <triage-id>
Summary:          <one sentence>
Lifecycle stage:  <first failing stage>   (reported at: <stage>)
Reported by:      <tool / step>
Likely failing:   <tool or dependency>
Category:         <failure category>
Target:           <app> · <env> · <cluster> · <namespace>   (source: <evidence>)
Blast radius:     <single app | multiple apps | unknown>

Evidence
  [Fact]        <source> — <sanitized excerpt or value>
  [Fact]        ...
  [Hypothesis]  <statement> — <what would confirm it>

What changed:     <change evidence, or "no change evidence available">
Likely cause:     <statement>
Confidence:       <High | Medium | Low> — <reason>

Classification:   <Self-fix | L1 issue | Prod team needed>
Status:           <complete | needs-input | blocked-access>

Actions taken (confirmed):
  - <action> — <succeeded | failed | unverified> — <reference>
Proposed manual actions (not performed):
  1. ...
Verify by:        <how the developer confirms resolution>
Escalate if:      <condition>
Open questions:   <one focused question, if any>
Unknowns:         <list>

Self-RCA · <triage-id> · <draft | confirmed-by-developer>      (complete triages only; see core/self-rca.md)
Problem:              ...
Trigger:              ...
Root cause:           ...   [basis: fact | likely | hypothesis]
Why not caught earlier: ...
Prevention (manual):  1. ...
```

Rules:
- Use `—` or `none` for empty fields; never omit a line.
- When classification is not yet possible, write `Classification: not yet determined`.
- "Actions taken" lists only actions an integration actually performed or attempted, with the real result. Read-only checks may be listed; writes must be.
- "Proposed manual actions" are always labelled as not performed and subject to normal change and approval processes.

## Part 2: Machine-readable result

```yaml
triage_result:
  schema_version: "1.0"
  triage_id: "TX-20261031-0001"
  request_ref: "<sanitized input reference>"
  lifecycle_stage: { first_failing: "quality-security", reported_at: "ci-build" }
  reported_tool: "jenkins"
  primary_tool: "sonarqube"
  secondary_tools: ["jenkins"]
  failure_category: "policy-gate"
  target: { app: "example-app", environment: "dev", cluster: null, namespace: null, source: "jenkins-console" }
  blast_radius: "single-app"            # single-app | multi-app | unknown
  classification: "self-fix"            # self-fix | l1 | prod-team | null
  status: "complete"                    # complete | needs-input | blocked-access
  confidence: { level: "high", reason: "Gate condition reported directly by SonarQube" }
  evidence:
    - { kind: "fact", source: "jenkins", ref: "<build-ref>", summary: "Quality gate status ERROR" }
  change_evidence: []
  actions_taken: []                     # { action, status: succeeded|failed|unverified, ref }
  proposed_manual_actions: []
  open_questions: []
  unknowns: []
  jira:  { expected: false, created: false, key: null, draft_provided: false }
  slack: { expected: false, posted: false }
  rca:                                  # optional; see core/self-rca.md
    status: "draft"                     # not-applicable | draft | confirmed-by-developer
    problem: "Build #142 blocked by the quality gate"
    trigger: "OrderExportService added without tests"
    root_cause: "New code lacks tests, so coverage on new code is 61.2% (< 80%)"
    root_cause_basis: "fact"            # fact | likely | hypothesis
    contributing_factors: []
    why_not_caught_earlier: "Coverage was not checked locally before pushing"
    resolution: "Add tests and re-run (proposed, not performed)"
    prevention: ["Run tests with coverage locally before pushing"]
```

## Field reference

| Field | Type | Notes |
|---|---|---|
| `schema_version` | `"1.0"` | Bump on breaking changes; record in CHANGELOG. |
| `triage_id` | `TX-YYYYMMDD-NNNN` | Generated per triage. |
| `request_ref` | string | Sanitized reference to the input (never raw logs). |
| `lifecycle_stage.first_failing` | stage id or null | Null only when it cannot be determined. |
| `lifecycle_stage.reported_at` | stage id or null | Where the developer saw the failure. |
| `reported_tool` / `primary_tool` | tool id or null | Reporting tool vs most likely failing tool. |
| `secondary_tools` | tool ids | Other modules that contributed evidence. |
| `failure_category` | category | Exactly one. `unknown` allowed. |
| `target` | object | `confirmed: true` only when evidence or the developer settled a single target. |
| `blast_radius` | enum | `unknown` when not determinable. |
| `classification` | enum or null | Null when status is not `complete` and no classification can be claimed. |
| `status` | enum | `complete` requires a classification. |
| `confidence` | object | Qualitative; reason required. Low forbids self-fix and prod-team. |
| `evidence[]` | objects | `kind: fact` or `hypothesis`; hypotheses need `confirm_by`. |
| `change_evidence[]` | objects | Empty list means no change evidence available. |
| `actions_taken[]` | objects | Real integration actions only. |
| `proposed_manual_actions[]` | strings | Never performed by TRIAGE-X. |
| `open_questions[]` | max 1 | One question at a time. |
| `jira` | object | `expected` = classification calls for a ticket; `created` only on confirmed success; `key` null unless created. |
| `slack` | object | Only `prod-team` may set `expected`; `posted` requires `jira.created`. |
| `rca` | object (optional) | Self-RCA (`core/self-rca.md`). `status: not-applicable` unless the triage is `complete`; `confirmed-by-developer` only after the developer confirms the fix. |
| `strcontain_transition` | `false` (optional) | Explicit assertion; can never be true. |

## Expected Jira ticket format

```text
Title:   [TRIAGE-X][<tool>] <short failure summary> — <app> (<env>)
Labels:  triage-x, triage-x-<tool>
Body:    Summary · Lifecycle stage · Target · Evidence (sanitized) ·
         What changed · Checks completed · Likely cause + confidence ·
         Unknowns · Requested action · Self-RCA ·
         NLH (prod-team cases only)
Fields:  TODO(owner) — issue type, components, priority mapping
```

## Expected Slack message format (Prod team needed only)

```text
:rotating_light: TRIAGE-X · Prod validation requested
App/Env:      <app> · <env>
Stage/Tool:   <stage> · <tool>
Impact:       <confirmed impact or "unknown">
Blast radius: <single-app | multi-app | unknown>
Ask:          <specific validation requested>
Ticket:       <PGPTOOLS key>
```

## Compatibility

The machine-readable block is the integration surface for metrics, evaluation and a possible Unified Support Agent (`docs/usa-integration.md`). Add fields in a backwards-compatible way; never repurpose an existing field.
