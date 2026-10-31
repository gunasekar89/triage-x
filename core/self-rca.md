# Self-service RCA

TRIAGE-X ends every **complete** triage with a short, developer-facing root cause analysis (RCA). It turns the evidence already collected into a reusable record: what broke, why, why it was not caught earlier, and what would prevent it next time.

The Self-RCA is **not** a formal incident postmortem. For production incidents, the organization's incident and postmortem process applies (`TODO(owner)`: name that process); the Self-RCA can be attached to it as input.

## 1. When to produce it

| Triage outcome | Self-RCA |
|---|---|
| Status `complete`, any classification | Produce it (`rca.status: draft`) |
| Status `needs-input` or `blocked-access` | Do not produce it (`rca.status: not-applicable`); there is no supported cause yet |
| Developer later confirms the fix worked | May be updated to `rca.status: confirmed-by-developer` |

TRIAGE-X never marks an RCA as confirmed on its own. Only the developer's explicit confirmation that the fix resolved the problem (or a reviewed support outcome) moves it from `draft` to `confirmed-by-developer`.

## 2. Template

```text
Self-RCA · <triage-id> · <draft | confirmed-by-developer>
Problem:              <what failed, for whom, in which environment>
Impact:               <confirmed impact, or "unknown">
Timeline (UTC):       <time> — <event>   (from evidence only)
First failing stage:  <stage> · <tool>   (reported at: <stage> · <tool>)
Trigger:              <what changed, or "no change evidence available">
Root cause:           <statement>   [basis: fact | likely | hypothesis]
Contributing factors: <list, or "none identified">
Why not caught earlier: <which earlier check could have caught it, or "unknown">
Resolution:           <proposed manual fix, or the fix the developer confirmed>
Prevention (manual, for the team to decide):
  1. <action> — suggested owner: <developer | team | TODO(owner)>
Evidence references:  <evidence items from the triage result>
```

## 3. Rules

- **Evidence only.** Every line comes from the triage evidence. Do not add new facts, logs or timestamps that were not retrieved.
- **State the basis of the root cause.**
  - `fact`: a direct observation explains the failure (e.g. a gate condition with its actual value).
  - `likely`: facts support it but one link is inferred.
  - `hypothesis`: not yet supported directly; say what would confirm it. A hypothesis-based RCA must be phrased as "suspected".
- The root-cause basis may not be stronger than the triage confidence: High confidence may use `fact` or `likely`; Medium uses `likely` or `hypothesis`; Low uses `hypothesis` only.
- **Policy blocks.** When a gate correctly blocked a change (`policy-gate`), the root cause is the change that violated the policy, not the gate. "Why not caught earlier" usually points at local checks (tests, scans) the developer can run before pushing.
- **Platform causes.** For L1 or Prod-team cases, the Self-RCA records what the developer saw and why it is not developer-fixable. Do not speculate about platform internals; leave those to the owning team.
- **Prevention items are suggestions**, labelled manual, with a suggested owner. TRIAGE-X never creates follow-up tickets for them unless that is configured and confirmed (`TODO(owner)`).
- **Sanitize** like every other output (`security-and-privacy.md`). No hostnames, URLs, credentials or names.
- Keep it short: normally under 20 lines.

## 4. Where it goes

- Part 1 of the result: the Self-RCA block, after the main result.
- Part 2: the `rca` object in `triage_result` (optional field, schema version `1.0`).
- Jira tickets (L1 and Prod team): included in the body after "Requested action".
