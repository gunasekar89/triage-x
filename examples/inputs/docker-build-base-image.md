# Docker — base image tag not found

> Synthetic.

**Developer input**

> example-app image build fails at FROM.

**Evidence available (synthetic)**

- Jenkins console: `failed to solve: <registry-host>/base/java-runtime:17.0.3: not found`.
- Dockerfile diff: `FROM` changed from `java-runtime:17.0.2` to `java-runtime:17.0.3` in the last commit.
- Registry existence check: tags `17.0.1`, `17.0.2`, `17.0.4` exist; `17.0.3` does not.
