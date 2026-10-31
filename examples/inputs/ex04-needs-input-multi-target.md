# Example 4 — Needs input (multiple WCNP targets)

> Synthetic.

**Developer input**

> Deployment failed for example-app.

**Evidence available (synthetic)**

- No Concord run reference supplied; none found unambiguously for the last hour.
- KITT file: see `kitt-multi-target.example.yml`, three candidate targets:
  1. `stage` · `<cluster-a>` · `example-app-stage`
  2. `prod` · `<cluster-b>` · `example-app-prod`
  3. `prod` · `<cluster-c>` · `example-app-prod`
