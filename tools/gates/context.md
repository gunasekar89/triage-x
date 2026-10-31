# Gates: context

Gates are release or quality checkpoints (for example security scan thresholds, change-record checks, test-evidence checks) that must pass before promotion. The exact gate product and its rules are `TODO(owner)`.

## Role in the lifecycle

Stage 3 (`quality-security`). A gate that **correctly blocks** a change is a `policy-gate` Self-fix, not a tool fault.

## Context to collect

- Gate name, result (pass/fail/error), evaluation time.
- Failed conditions and their thresholds (e.g. critical vulnerabilities > 0).
- Evidence the gate evaluated (scan report reference, test report reference, change record reference).
- Whether an exception or waiver process exists (`TODO(owner)`).

## Identifiers and target resolution

- Gate evaluation ID `<gate-eval-id>`; application and version under evaluation.

## Connector and access

- Connector: `TODO(owner)` (gate service API or results exported into Concord/Jenkins logs).
- If no direct connector exists, read gate results from the Concord or Jenkins log that invoked the gate.

## Relationships to other tools

- Invoked by Concord or Jenkins → those tools are reporters.
- Security scan findings may originate in SonarQube or a scanner (`TODO(owner)`: scanner list).

## Pilot status

Post-pilot. During the pilot, gate failures surfaced in Jenkins or Concord logs are read as supporting evidence.
