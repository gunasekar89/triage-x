# Kubernetes — CrashLoopBackOff after release

> Synthetic.

**Developer input**

> example-app pods keep restarting in dev after today's deploy.

**Evidence available (synthetic)**

- Target confirmed: KITT has one `dev` entry (`<cluster-d>`, `example-app-dev`), matching Concord log.
- Pod state `CrashLoopBackOff`, restarts 9, exit code 1.
- Previous container log tail: `IllegalStateException: required property 'ORDERS_DB_POOL_SIZE' is not set`.
- KITT diff: env var `ORDERS_DB_POOL_SIZE` removed in the release.
