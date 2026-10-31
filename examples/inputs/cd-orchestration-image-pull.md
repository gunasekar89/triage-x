# CD Orchestration tools (AKS, GKE, EKS) — image pull access denied

> Synthetic.

**Developer input**

> example-app stage deploy failed with ImagePullBackOff.

**Evidence available (synthetic)**

- Target confirmed: one `stage` KITT entry (`<cluster-a>`, `example-app-stage`) matching Concord log.
- Event: `Failed to pull image "<registry-host>/example-app:3.1.0": unauthorized: authentication required`.
- Tag `3.1.0` exists in the registry (authorized check).
- No KITT change to image or pull secret; platform notice (synthetic) mentions pull-secret rotation yesterday.
