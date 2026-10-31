# Jenkins — build agent unavailable

> Synthetic.

**Developer input**

> example-app build #210 has been waiting for 40 minutes.

**Evidence available (synthetic)**

- Jenkins queue: `Waiting for next available executor on 'linux-docker-large'`.
- Jenkinsfile label unchanged for 3 months.
- Node status for label (authorized): 4 of 4 agents offline since 40 minutes ago.
- Other teams' visibility: not authorized (blast radius unknown).
