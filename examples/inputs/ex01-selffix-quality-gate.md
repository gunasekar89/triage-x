# Example 1 — Self-fix (policy gate, not a tool fault)

> Synthetic. All names, numbers and log lines are invented.

**Developer input**

> Build #142 for example-app failed at Quality Gate.

**Evidence available to TRIAGE-X (synthetic tool responses)**

- Jenkins `example-app` build #142, stage `Quality Gate`:
  ```text
  [INFO] SonarQube task <ce-task-id> completed
  QUALITY GATE STATUS: FAILED - View details on <internal-url>
  ERROR: Pipeline aborted due to quality gate failure: ERROR
  ```
- SonarQube project `example-app`, gate status `ERROR`, failing condition: `new_coverage` LT 80.0, actual 61.2.
- Commits since last green build: 3, adding `OrderExportService` without tests.
