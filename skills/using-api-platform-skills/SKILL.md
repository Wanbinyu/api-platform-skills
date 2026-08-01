---
name: using-api-platform-skills
description: >
  Meta-router for the API Platform Skills pack. Use when the user asks about APIs,
  OpenAPI, versioning, breaking changes, deprecation, webhooks, idempotency, contract
  tests, or API security but it is unclear which specialized skill to load. Also use
  when the user says "api platform skills", "which API skill", or "/api-ship-check".
---

# Using API Platform Skills

## Overview

Route work to the smallest set of specialized skills. Do **not** load every skill. Prefer one primary skill; add a second only when exit criteria require it.

## Routing table

| User intent / signals | Primary skill | Optional second |
|----------------------|---------------|-----------------|
| New API / new endpoints / write OpenAPI first | `contract-first-openapi` | `secure-api-surface` |
| "Who breaks if we change X?" / field usage | `compatibility-matrix` | `breaking-change-review` |
| PR review, removed field, type change, status rename | `breaking-change-review` | `deprecation-playbook` |
| Sunset v1, migrate clients, dual-track | `deprecation-playbook` | `compatibility-matrix` |
| Pact / consumer expectations / contract tests | `consumer-driven-contract` | `contract-first-openapi` |
| Retries, double charge, Idempotency-Key | `idempotency-and-retries` | — |
| Webhooks, callbacks, signed events | `webhook-design` | `idempotency-and-retries` |
| BOLA/BFLA, excess data, authz on APIs | `secure-api-surface` | — |
| Pre-merge "can we ship this API change?" | Run **ship-check** sequence below | — |

## Ship-check sequence (`/api-ship-check`)

Run in order; stop and report blockers at first failed hard gate:

1. `contract-first-openapi` — spec present and reviewable  
2. `breaking-change-review` — no silent breaks  
3. `secure-api-surface` — critical authz issues  
4. If mutations/retries: `idempotency-and-retries`  
5. If events out: `webhook-design`  

## Steps

1. Restate the user's goal in one sentence.
2. Pick primary skill from the table (or ship-check).
3. Announce which skill(s) you will follow.
4. Execute that skill fully (its exit criteria).
5. Summarize with links to any reports produced.

## Exit criteria

- [ ] Exactly one primary skill chosen (or explicit ship-check)
- [ ] User told which skill is active
- [ ] Specialized skill exit criteria satisfied

## Anti-patterns

- Loading all nine skills into one prompt
- Answering API evolution questions from generic REST folklore without a skill workflow
- Skipping breaking-change-review because "it's a small field rename"

## Output template

```markdown
## Skill routing
- Goal: ...
- Primary: `...`
- Secondary: `...` | none
- Mode: single | ship-check
```
