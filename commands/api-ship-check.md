---
description: Full pre-merge API platform gate (contract, breaks, security, reliability)
---

Load `using-api-platform-skills` and run the **ship-check** sequence in order:

1. `contract-first-openapi` - reviewable contract
2. `breaking-change-review` - no silent breaks
3. `secure-api-surface` - authz / exposure
4. `idempotency-and-retries` if mutations or retries
5. `webhook-design` if outbound events

Stop on the first hard blocker. Finish with a single go/no-go summary table of which gates passed or failed.
