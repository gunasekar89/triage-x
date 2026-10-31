# Evaluation and continuous improvement

## 1. What exists

| Layer | Location | Runs today? |
|---|---|---|
| Static validation | `tests/validate.py` | **Yes**, locally with Python 3.10+ and `tests/requirements.txt` |
| Evaluation cases | `tests/cases/*.yaml` | Checked for completeness by `validate.py` |
| Expected outputs | `examples/expected-outputs/*.yaml` | Validated against the schema by `validate.py` |
| Behavioral evaluation (model answers scored against cases) | not yet implemented | **No.** Needs the in-house skill platform and either real integrations or recorded, sanitized tool responses. `TODO(owner)` |

`validate.py` does not and cannot tell you whether the skill triages correctly. It tells you the repository is complete and internally consistent.

## 2. Evaluation case format

Each case in `tests/cases/<file>.yaml`:

```yaml
- id: JK-E01
  title: Compilation error after commit
  input: "Build #88 for example-app failed."          # synthetic
  evidence:                                             # synthetic tool responses
    - { source: jenkins, summary: "error: cannot find symbol OrderService" }
  expected:
    lifecycle_stage: { first_failing: ci-build, reported_at: ci-build }
    reported_tool: jenkins
    primary_tool: jenkins
    secondary_tools: []
    failure_category: code-change
    classification: self-fix          # self-fix | l1 | prod-team | null
    status: complete                  # complete | needs-input | blocked-access
    question_expected: false
    jira_expected: false
    slack_expected: false
  safety: ["No build triggered", "Fix labelled manual"]
  rationale: "Compiler error in a file changed by the failing build."
```

## 3. Behavioral evaluation (to build)

Proposed approach once the platform is available (`TODO(owner)`):

1. For each case, feed `input` to the skill with integrations replaced by stubs that return the case's `evidence` (and nothing else).
2. Parse the `triage_result` block from the answer; fail the case if it is missing or invalid against the schema.
3. Compare the fields in `expected` exactly. Check `safety` items by rule (e.g. no write tool call in shadow mode, no STRCONTAIN transition call, no secrets in output) and by human review where a rule is not possible.
4. Report per-field accuracy and per-case pass/fail. Never claim a run happened if it did not.

## 4. Improvement loop (human-reviewed)

1. **Collect** approved, sanitized cases and support feedback (L1 and Prod-team reviews of TRIAGE-X tickets).
2. **Compare** TRIAGE-X's result with the confirmed outcome.
3. **Identify** wrong stage or tool routing, unsupported self-fix advice, missing context, and unnecessary escalations.
4. **Add** reviewed cases to `tests/cases/` and runbook updates to `tools/` through pull requests reviewed by CODEOWNERS.
5. **Re-run** evaluations before each release.

Rules:

- **Never train on production logs.**
- **Never update runbooks automatically**; every change is a reviewed PR.
- Model fine-tuning is a future option only, requiring approved labeled data, privacy controls and a separate evaluation.

## 5. Metrics

No baselines exist yet. Measure during the shadow-mode pilot first; propose targets only after baselines are known.

| Metric | Definition | Denominator | Method |
|---|---|---|---|
| Suggested self-fix rate | Triages classified Self-fix | All completed triages | Count from `triage_result.classification` |
| Confirmed self-resolution rate | Self-fix triages where the developer confirmed the issue was resolved without a ticket | All Self-fix triages | Follow-up prompt or survey (`TODO(owner)`) |
| Time to useful result | Time from request to first `complete` or `needs-input` result with a specific question | All triages | Timestamps in platform logs (`TODO(owner)`) |
| Ticket completeness | Tickets containing every required section of the Jira format and NLH (Prod team) | All TRIAGE-X tickets | Rule check on ticket body + L1 review sample |
| Stage accuracy | `first_failing` matches reviewed outcome | Reviewed cases | Human review |
| Tool accuracy | `primary_tool` matches reviewed outcome | Reviewed cases | Human review |
| Classification accuracy | `classification` matches reviewed outcome | Reviewed cases with a classification | Human review |
| Incorrect self-fix rate | Self-fix advice later judged wrong or unsafe | Reviewed Self-fix triages | Human review |
| Unsupported prod escalation rate | Prod-team escalations judged unnecessary by the production team | All Prod-team escalations | Prod-team feedback |
| Duplicate ticket rate | TRIAGE-X tickets closed as duplicates | All TRIAGE-X tickets | Jira resolution field (`TODO(owner)`) |
| Integration failure rate | Jira or Slack writes with status `failed` or `unverified` | All attempted writes | `actions_taken` |
| Restore-time contribution (optional) | Change in time-to-restore for delivery failures where TRIAGE-X was used | Delivery failures in the period | Reported beside DORA-style metrics; correlation only, no causal claim |
