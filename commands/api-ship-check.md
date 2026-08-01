---
description: Full pre-merge API platform gate
---

Load `using-api-platform-skills` and run the **ship-check sequence**:
1. contract-first-openapi
2. breaking-change-review
3. secure-api-surface
4. idempotency-and-retries if mutations/retries
5. webhook-design if outbound events

Stop on hard blockers. End with a single go/no-go summary table.
