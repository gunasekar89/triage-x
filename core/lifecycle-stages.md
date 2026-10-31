# Lifecycle stages

TRIAGE-X reasons **by lifecycle stage first, tool second**.

## 1. Stage map

| # | Stage id | Name | Tools | Typical failure categories |
|---|---|---|---|---|
| 1 | `source-change` | Source & change | GitHub | Branch protection, required checks, merge conflicts, workflow or config errors |
| 2 | `ci-build` | CI build | Jenkins, Docker (build) | Compilation, dependency resolution, build agent, Dockerfile, test failures |
| 3 | `quality-security` | Quality & security | SonarQube, Gates | Quality gate conditions, scan failures, policy violations |
| 4 | `package-publish` | Package & publish | Artifactory, Docker (registry) | Artifact or image publish/pull, version, permission, storage errors |
| 5 | `orchestrate-deliver` | Orchestrate & deliver | Concord | Pipeline flow, task failures, target resolution, approvals |
| 6 | `deploy` | Deploy | Kubernetes, WCNP | Manifest/config errors, image pull, rollout, quota, admission policy |
| 7 | `run-operate` | Run & operate | Kubernetes, WCNP | CrashLoop, OOM, probes, scheduling, node or platform health |

Stage 5 (Concord) orchestrates other stages, so a Concord failure frequently has its first failing stage at 2, 3, 4 or 6.

## 2. Failure category taxonomy

Every result has exactly **one** primary category.

| Category | Meaning | Typical owner (default, `TODO(owner)` confirm) |
|---|---|---|
| `code-change` | Application code or tests changed and broke the build, tests or runtime | Developer |
| `configuration` | Application, pipeline, KITT, manifest or Dockerfile configuration is wrong | Developer (if they own the file) or L1 |
| `dependency` | A library, base image or upstream artifact version is missing, incompatible or changed | Developer (version choice) or L1 (repository issue) |
| `credentials-access` | Authentication or authorization denied, expired token, missing permission | L1 |
| `policy-gate` | A quality gate, security scan or policy check **correctly** blocked the change | Developer |
| `capacity-quota` | Resource quota, scheduling capacity, storage limit | Developer (own quota request) / L1 / Prod team (cluster-wide) |
| `platform-infra` | Shared tool, node, control plane, network or registry fault | Prod team or L1 |
| `transient-flaky` | Timeouts or intermittent errors with no related change | Developer retry once, then L1 |
| `unknown` | Evidence insufficient to categorize | n/a; status usually `needs-input` or `blocked-access` |

## 3. Upstream walk: finding the first failing stage

The first tool reporting an error is often a downstream symptom. For every triage:

1. Note the **reported stage** and **reported tool**.
2. Ask: does the error message reference another tool, job, artifact, image or check? If yes, move to that stage's module and collect evidence there.
3. Repeat until you reach a stage whose failure is **self-contained** (its own evidence explains the failure) or you run out of authorized evidence.
4. The earliest stage with direct failure evidence is `first_failing`. If you could not reach it, record the last stage you could verify and add "upstream stage not verified" to `unknowns`.
5. Never claim a root cause in a stage you could not observe.

### Examples (synthetic)

| Reported | Walk | First failing |
|---|---|---|
| Concord: task `build` failed | → Jenkins build #142 stage "Quality Gate" ERROR → SonarQube: coverage on new code 61% < 80% | `quality-security` (SonarQube), category `policy-gate` |
| WCNP: deploy timed out | → pods `ImagePullBackOff` → registry: tag `1.4.2` not found → Jenkins publish stage skipped | `package-publish` or `ci-build`, depending on evidence |
| GitHub: required check failing | → Jenkins build failed: `cannot find symbol` | `ci-build`, category `code-change` |

## 4. "What changed?" checks by stage

| Stage | Change evidence to look for |
|---|---|
| source-change | Recent merges, branch protection or required-check changes, workflow file edits |
| ci-build | Commits since last green build, build script or Jenkinsfile edits, dependency bumps, agent image changes |
| quality-security | Quality profile or gate changes, new rules, new-code baseline changes |
| package-publish | Version bumps, repository or permission changes, credential rotation |
| orchestrate-deliver | Concord flow changes, new approval steps, changed target definitions |
| deploy | KITT or manifest edits, image tag changes, quota or policy changes |
| run-operate | New image, config or secret changes, resource limit changes, platform notices |

If no change evidence is available, write "no change evidence available" and keep confidence proportionate.
