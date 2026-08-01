---
name: using-api-platform-skills
description: >
  Meta-router for API Platform Skills (contract evolution pack). Use when the user
  mentions APIs, OpenAPI, versioning, breaking changes, deprecation, webhooks,
  idempotency, contract tests, or API security but the specialized skill is unclear;
  or says "api platform skills", "which API skill", "/api-ship-check", "ship-check".
  Do not use for pure REST naming/style questions (shape layer belongs to other packs).
---

# Using API Platform Skills

> **Router only.** Pick the smallest skill. Never load all nine.

## Overview

This pack owns the **evolution layer** (compat, breaks, deprecation, CDC, idempotency, webhooks, API surface security). Route there. For plural-noun / status-code style guides, say so and stay out of scope.

## Routing table

| User intent / signals | Primary | Optional second |
|----------------------|---------|-----------------|
| New API / write OpenAPI first | `contract-first-openapi` | `secure-api-surface` |
| Who breaks if we change X? | `compatibility-matrix` | `breaking-change-review` |
| PR: removed field, type change, status rename | `breaking-change-review` | `deprecation-playbook` |
| Sunset v1, dual-track, migrate clients | `deprecation-playbook` | `compatibility-matrix` |
| Pact / consumer expectations | `consumer-driven-contract` | `contract-first-openapi` |
| Double charge, Idempotency-Key, retries | `idempotency-and-retries` | — |
| Callbacks, signed events | `webhook-design` | `idempotency-and-retries` |
| BOLA/BFLA, excess data, mass assignment | `secure-api-surface` | — |
| Pre-merge “can we ship?” | **Ship-check** below | — |
| Only “is plural nouns correct?” | *Out of scope* — point to shape packs | — |

## Ship-check sequence

Run in order; stop at first hard gate failure:

1. `contract-first-openapi` — reviewable contract exists  
2. `breaking-change-review` — no silent breaks  
3. `secure-api-surface` — critical authz / exposure  
4. Mutations/retries → `idempotency-and-retries`  
5. Outbound events → `webhook-design`  

## Steps

1. Restate the goal in one sentence.  
2. Choose primary skill (or ship-check / out-of-scope).  
3. Tell the user which skill is active.  
4. Execute that skill to its exit criteria.  
5. Summarize with any report paths.

## Exit criteria

- [ ] Primary skill chosen (or explicit ship-check / out-of-scope)
- [ ] User informed of active skill
- [ ] Specialized exit criteria satisfied (if in pack)

## Anti-patterns

- Loading every skill “just in case”
- Answering evolution questions with generic REST folklore
- Skipping break review because “it’s a small rename”
- Rewriting a full api-design tutorial inside this pack

## Output template

```markdown
## Skill routing
- Goal: …
- Primary: `…`
- Secondary: `…` | none
- Mode: single | ship-check | out-of-scope
- Note: …
```
