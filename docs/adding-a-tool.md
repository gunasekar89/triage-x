# Adding a tool

Adding a tool must not require changes to unrelated modules.

## Steps

1. **Pick the stage(s).** Map the tool to one or more stages in `core/lifecycle-stages.md`. If it does not fit any stage, raise that as a design question before continuing.
2. **Copy the template.**
   ```bash
   cp -r tools/_template tools/<tool>
   ```
3. **Fill `context.md`.** Role, context to collect, identifiers, connector (`TODO(owner)` until known), relationships, pilot status.
4. **Fill `checks.md`.** Read-only checks only; mark every command or API path as illustrative; include what-changed and blast-radius checks and a "Never do" list.
5. **Write 5–8 patterns in `runbooks.md`.** Each pattern needs every field in the template. Use only categories from the taxonomy.
6. **Register the tool id.**
   - Add it to the `tool` enum in `schemas/triage-result.schema.json` (additive change; note it in `CHANGELOG.md`).
   - Add it to `TOOLS` in `tests/validate.py`.
7. **Add routing hints** to `core/router.md` (keywords and illustrative signatures) and any multi-tool relationships.
8. **Add examples.** One synthetic input in `examples/inputs/` and its expected output in `examples/expected-outputs/`.
9. **Add at least four evaluation cases** in `tests/cases/<tool>.yaml`.
10. **Update** the tool-scope table in `README.md` and `CODEOWNERS`.
11. **Run** `python3 tests/validate.py`.

## What you should not need to change

- `core/classification.md`, `core/evidence-and-confidence.md`, `core/security-and-privacy.md`.
- Other tool modules (except to add a cross-reference if the tools interact).
- Integration contracts.

If you find you must change one of these, the change is probably a core design change: open it as a separate PR.
