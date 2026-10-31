# Onboarding and go-live checklists

## A. Team onboarding (each team, about 30 minutes)

- [ ] Copy `config/triage-x.config.example.yaml` to `config/triage-x.config.yaml` (kept out of git) or to your platform's config store.
- [ ] Set `team`, `environments` (your naming) and `mode: shadow`.
- [ ] List the tools your team uses under `tools:` and mark `enabled: true` only for connectors you actually have (read-only).
- [ ] For CD Orchestration, set `platform:` to `aks`, `gke` or `eks`.
- [ ] Decide the ticket destination: Jira project key and issue types (or leave `jira.enabled: false` for drafts only).
- [ ] Decide the alerts channel for Prod-team cases (or leave `slack.enabled: false`).
- [ ] Share `docs/process/quick-start.md` with developers.
- [ ] Agree where the feedback log lives (`docs/process/operating-process.md` §5).

## B. Pilot go-live (shadow mode)

- [ ] Skill platform chosen and header adapted in `SKILL.md` (`TODO(owner)`).
- [ ] Bundle built: `python3 scripts/bundle.py` → `dist/triage-x-skill.md`, and loaded.
- [ ] `python3 tests/validate.py` passes on the deployed commit.
- [ ] Pilot tool owners (Jenkins, SonarQube, CD Orchestration) reviewed their runbooks and replaced illustrative signatures with real, sanitized ones.
- [ ] 5–10 recent real failures (sanitized) replayed in paste mode; results reviewed by L1.
- [ ] Feedback log created and owners named.
- [ ] Developers in the pilot teams briefed.

## C. Turning on writes (after the shadow pilot)

- [ ] Jira MCP connected with **create-only** permission in the configured project; no transition, assign or edit rights.
- [ ] Test ticket created and verified end to end, then closed by L1.
- [ ] Duplicate search works (or is documented as unavailable).
- [ ] Slack integration limited to the one configured channel; test message verified.
- [ ] Audit logging of writes confirmed (`TODO(owner)`).
- [ ] Config switched to `mode: writes`, `jira.enabled: true` (and `slack.enabled: true` if used).
- [ ] Developer confirmation before every write left on (`jira.confirmation_required: true`).

## D. Before v1.0 (all tools)

- [ ] Each tool owner reviewed their module.
- [ ] Behavioral evaluation harness built and passing on `tests/cases/`.
- [ ] Pilot metrics reviewed and initial targets proposed.
