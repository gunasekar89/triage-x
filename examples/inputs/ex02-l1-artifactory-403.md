# Example 2 — L1 issue (access)

> Synthetic.

**Developer input**

> Pipeline can't pull com.example:example-lib:2.3.1.

**Evidence available (synthetic)**

- Jenkins `example-app` build #77, stage `Build`:
  ```text
  [ERROR] Failed to execute goal on project example-app: Could not resolve dependencies:
  Could not transfer artifact com.example:example-lib:jar:2.3.1 from/to libs-release (<internal-url>):
  status code: 403, reason phrase: Forbidden (403)
  ```
- Artifactory existence check: `com.example:example-lib:2.3.1` exists in `libs-release`; other consumers' builds resolved it in the last 24 h (authorized read).
- No dependency version change in this build; last green build used 2.3.0 from a different repository path.
