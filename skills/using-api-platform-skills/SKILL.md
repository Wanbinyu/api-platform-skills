---
name: using-api-platform-skills
description: >
  Route API work to the right API Platform skill. Use when the user mentions APIs,
  OpenAPI, versioning, breaking changes, deprecation, webhooks, idempotency, contract
  tests, ship-check, or is unsure which skill to load. Also when they say
  "/api-ship-check", "which API skill", "api platform", or in Chinese
  "接口审查", "兼容性", "破坏性变更", "弃用", "幂等", "Webhook", "变更日志",
  "该用哪个 skill". Do NOT use for pure REST naming/style (plural nouns only).
---

# Using API Platform Skills

> Router only. Load the smallest skill. Never load the whole pack.

## Overview

This pack owns the **evolution layer** (compat, breaks, deprecation, CDC, idempotency, webhooks, API surface security, consumer changelogs). For pure REST style guides, say out-of-scope.

## Routing table

| User intent | Primary | Optional second |
|-------------|---------|-----------------|
| New API / OpenAPI first | `contract-first-openapi` | `secure-api-surface` |
| Who breaks if we change X? | `compatibility-matrix` | `breaking-change-review` |
| PR: remove field, type change, status rename | `breaking-change-review` | `deprecation-playbook` |
| Sunset v1, dual-track, migrate clients | `deprecation-playbook` | `compatibility-matrix` |
| Pact / consumer expectations | `consumer-driven-contract` | `contract-first-openapi` |
| Double charge, Idempotency-Key, retries | `idempotency-and-retries` | - |
| Callbacks, signed events | `webhook-design` | `idempotency-and-retries` |
| BOLA/BFLA, excess data, mass assignment | `secure-api-surface` | - |
| Release notes / partner changelog | `api-changelog` | `breaking-change-review` |
| Pre-merge can we ship? | Ship-check below | - |
| Only "is plural nouns correct?" | Out of scope (shape packs) | - |

## Ship-check sequence

Run in order; stop at first hard gate failure:

1. `contract-first-openapi` - reviewable contract exists
2. `breaking-change-review` - no silent breaks
3. `secure-api-surface` - critical authz / exposure
4. Mutations/retries -> `idempotency-and-retries`
5. Outbound events -> `webhook-design`
6. After merge decision -> `api-changelog` for consumer notes

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

- Loading every skill "just in case"
- Answering evolution questions with generic REST folklore
- Skipping break review because "it is a small rename"
- Rewriting a full api-design tutorial inside this pack

## Output template

```markdown
## Skill routing
- Goal: ...
- Primary: `...`
- Secondary: `...` | none
- Mode: single | ship-check | out-of-scope
- Note: ...
```
