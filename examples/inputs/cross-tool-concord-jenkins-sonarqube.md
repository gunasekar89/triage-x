# Cross-tool — Concord → Jenkins → SonarQube

> Synthetic.

**Developer input**

> Concord pipeline for example-app failed at the build task.

**Evidence available (synthetic)**

- Concord process `<process-id>`: task `ciBuild` FAILED, `Jenkins job example-app build #305 finished with result FAILURE`.
- Jenkins build #305, stage `Quality Gate`: `Pipeline aborted due to quality gate failure: ERROR`.
- SonarQube `example-app`: condition `new_security_rating` GT 1, actual 3 (one new vulnerability, rule `<rule-id>`, SQL built from string concatenation).
