# GitHub — required check failing (routes to Jenkins)

> Synthetic.

**Developer input**

> My PR example-org/example-app#57 can't merge, a required check is red.

**Evidence available (synthetic)**

- PR #57 mergeable_state `blocked`; required check `ci/jenkins/build` conclusion `failure`, target points to Jenkins `example-app/PR-57` build #3.
- Jenkins build #3 console: `[ERROR] OrderMapper.java:[42,17] cannot find symbol: method toDto()`.
- PR commit renamed `toDto()` to `toResponse()` in `Order.java`.
