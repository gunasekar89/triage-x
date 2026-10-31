# Evidence and confidence

## 1. Three kinds of statement

| Kind | Definition | Example (synthetic) | How it appears |
|---|---|---|---|
| **Observed fact** | Directly seen in a tool response, log line or configuration value you retrieved or the developer supplied | Jenkins console: `QUALITY GATE STATUS: FAILED` | `[Fact] jenkins — <excerpt>` / `kind: fact` |
| **Likely cause** | The best explanation that the facts support | Coverage on new code is below the gate threshold | `Likely cause:` line, with confidence |
| **Unverified hypothesis** | A plausible explanation not yet supported by direct evidence | The registry credential may have been rotated | `[Hypothesis] <statement> — <what would confirm it>` / `kind: hypothesis` with `confirm_by` |

Never present a hypothesis as a confirmed root cause.

## 2. Citation rules

- Every important conclusion cites at least one fact: the source (tool), a sanitized reference (build number, process id, event reason, config key) and a short excerpt or value.
- Excerpts are **sanitized** and **short** (normally one to three lines). Never paste raw log dumps.
- If a fact came from the developer rather than a tool, say so: `source: developer-supplied`.
- Never invent a log line, API response, ticket key or result. If you did not retrieve it, it is not a fact.

## 3. "What changed?"

Before concluding, look for authorized evidence of recent changes in:

- code (commits, merged PRs since the last successful run);
- pipeline definition (Jenkinsfile, Concord flow, workflow files);
- KITT or deployment configuration;
- base image or image tag;
- dependency versions;
- credentials (rotation, expiry);
- platform notices or maintenance announcements (`TODO(owner)`: source of platform notices).

Record findings in `change_evidence`. If none is available, write "no change evidence available"; do not imply there was no change.

## 4. Blast radius

When authorized data allows, check whether the symptom affects:

- **one application** (`single-app`);
- **several applications** on the same cluster, tool instance or shared dependency (`multi-app`), a strong platform signal;
- **unknown**, when you cannot see beyond the developer's application.

State how you determined it (e.g. "same `FailedScheduling` events in 6 other namespaces on `<cluster-name>`").

## 5. Confidence

Confidence is a **qualitative label** with a one-line reason. It is not a calibrated probability; do not report percentages unless they were measured.

| Level | Use when | Example reason |
|---|---|---|
| **High** | A direct fact from the failing tool explains the failure, the first failing stage is verified, and no conflicting evidence exists | "Gate condition reported directly by SonarQube" |
| **Medium** | Facts support the cause but one link is inferred (e.g. upstream stage not fully visible, blast radius unknown, change evidence missing) | "Scheduling events confirm CPU shortage; cluster-wide view partial" |
| **Low** | Cause is inferred from indirect or partial evidence, or evidence conflicts | "Only a truncated console log; failing step not visible" |

Rules:
- Low confidence never produces a Self-fix or a Prod-team classification.
- Downgrade confidence when evidence is incomplete, conflicting or from the developer only.
- Upgrade only on new direct evidence, never on the developer's insistence alone.

## 6. Staying bounded

- Run the checks defined for the matched failure patterns. Do not loop through unrelated checks.
- Stop as soon as evidence is sufficient to classify.
- If after the matched checks you still cannot classify, conclude with `needs-input` or `blocked-access` and the next safe check.
