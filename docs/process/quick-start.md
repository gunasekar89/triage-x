# Quick start: use TRIAGE-X today

This gets a developer from "my pipeline failed" to a triage result **without any integrations**. TRIAGE-X runs in **paste mode**: you paste the evidence, it triages, and it drafts any ticket for you to raise by hand. This is the pilot's shadow mode.

## 1. Load the skill (once per team)

**Option A: one file.** Build the bundle and load it as the skill or as the system/project instructions of your AI assistant:

```bash
python3 scripts/bundle.py          # writes dist/triage-x-skill.md
```

**Option B: folder skill.** If your platform supports multi-file skills (for example a `SKILL.md` folder), load `SKILL.md` with the `core/`, `tools/` and `integrations/` folders.

Platform-specific header and packaging: `TODO(owner)`.

## 2. Ask for a triage

Paste one request. More context gives a better result, but TRIAGE-X will ask for what it needs, one question at a time.

```text
TRIAGE-X: <one line: what failed>
App:          <app name>
Environment:  <dev | stage | prod>
Reference:    <build #, pipeline/process id, PR, or "none">
Where seen:   <GitHub | Jenkins | Concord | SonarQube | Artifactory | deploy | running app>
What changed: <recent commits, config or version changes, or "not sure">
Evidence:
<paste the 20–50 log lines around the FIRST error, plus any status/event output>
```

Before pasting, remove anything you would not put in a ticket. TRIAGE-X also redacts secrets, internal URLs and names, and tells you when it did.

## 3. Read the result

| You get | What to do |
|---|---|
| **Self-fix** | Follow the numbered manual steps, then check "Verify by". If it still fails, reply with the new evidence. |
| **L1 issue** | Review the ticket draft. Raise it in your team's Jira project (or confirm, once Jira is connected). |
| **Prod team needed** | Review the ticket draft and the Next Level Handover. Raise it, then post the Slack summary in your alerts channel. |
| **Needs input** | Answer the single question (for example, which cluster). |

Every completed triage ends with a **Self-RCA**. Keep it with the ticket or your team notes. When your fix works, tell TRIAGE-X so it can mark the RCA as confirmed.

## 4. Tell us how it went

After each triage, record the outcome in your team's feedback log (`docs/process/operating-process.md` §5). This is how runbooks improve.

## Tips

- Paste the **first** error, not just the last line. The last line is usually a downstream symptom.
- For deploy problems, include the cluster and namespace if you know them; otherwise TRIAGE-X will offer the candidates from your CI/CD config.
- Never paste tokens, passwords or private keys.
