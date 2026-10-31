# Gates — vulnerability threshold exceeded

> Synthetic.

**Developer input**

> Release gate blocked example-app 2.8.0 promotion to stage.

**Evidence available (synthetic)**

- Gate evaluation `<gate-eval-id>`: `FAILED: critical vulnerabilities 1 > 0` for component `example-json-parser 1.2.0`.
- Dependency diff since 2.7.0: `example-json-parser` bumped 1.1.4 → 1.2.0.
