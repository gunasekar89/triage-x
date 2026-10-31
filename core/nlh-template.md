# Next Level Handover (NLH) template

Used only for **Prod team needed**. TRIAGE-X drafts the NLH; the developer confirms; it is included in the Jira ticket body. TRIAGE-X never claims the production team accepted it and never moves the ticket to another queue.

```text
NEXT LEVEL HANDOVER · <triage-id> · <Jira key or "draft">

1. Business / service impact
   <confirmed impact, or "unknown — not confirmed by evidence">

2. Application and target
   App: <app>   Env: <env>   Cluster: <cluster-name>   Namespace: <namespace>
   Target source: <evidence that confirmed the target>

3. Failure summary and lifecycle stage
   <one or two sentences>
   First failing stage: <stage>   Reported at: <stage> by <tool>

4. Blast radius
   <single-app | multi-app | unknown> — <how determined>

5. Evidence (sanitized)
   [Fact] <source> — <excerpt>
   [Fact] ...
   [Hypothesis] <statement> — <what would confirm it>

6. Investigation timeline (UTC)
   <time> — <what was observed or checked>
   <time> — ...

7. Checks completed
   - <check> — <result>

8. Why L1 cannot resolve this
   <specific reason: shared component, missing authority, multi-app impact, etc.>

9. Requested production-team action
   <the specific validation or action requested>

10. Remaining unknowns
   - <unknown>

Note: Moving this ticket to L3 or another queue is a manual support decision. TRIAGE-X has not moved it.
```

## Completeness checklist

An NLH draft is complete only when every numbered section is filled or explicitly marked `unknown`. Section 8 and section 9 must never be empty: if you cannot state why L1 cannot resolve it and what you are asking for, the case is not Prod team needed.
