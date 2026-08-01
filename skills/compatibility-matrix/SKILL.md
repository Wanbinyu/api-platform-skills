---
name: compatibility-matrix
description: >
  Build a compatibility impact matrix for an API change. Use when asking who breaks if
  a field, endpoint, status code, or auth behavior changes; when planning migrations;
  or when the user says "/api-compat", "blast radius", or "consumer impact".
---

# Compatibility Matrix

## Overview

Before changing a shipped contract, map **what changes** → **who consumes it** → **impact severity** → **required mitigation**. Guessing is not allowed; document unknowns explicitly.

## Steps

1. **Define the change set**
   - List each delta: add/remove/rename/retype field, path change, status change, header change, auth change, semantic change (same shape, different meaning).

2. **Inventory consumers** (best effort)
   - First-party web/mobile
   - Internal services
   - External partners / public docs
   - Generated SDKs
   - Jobs/cron/webhooks
   - Unknown (mark explicitly)

   Sources: repo grep for paths/operationIds, API gateway logs notes, README, SDK packages, OpenAPI `x-consumers` if present, team knowledge stated by user.

3. **Classify each delta**

   | Class | Examples |
   |-------|----------|
   | Safe additive | New optional field, new endpoint, new optional query param |
   | Soft risk | New required field on request without default; tighter validation |
   | Hard break | Remove/rename field; change type; change status meaning; remove endpoint |
   | Semantic break | Same JSON, different meaning (e.g. amount now cents) |

4. **Build matrix**

   Rows = deltas, columns = consumers, cells = impact: `none | low | high | unknown` + note.

5. **Mitigations**
   - For each `high` or `unknown`: dual-write, dual-read, deprecation window, version bump, feature flag, adapter layer.
   - Prefer additive + deprecate over hard break.

6. **Decision**
   - Ship additive / ship with version / block pending consumer work / needs research (list how to resolve unknowns).

## Exit criteria

- [ ] Change set enumerated as discrete deltas
- [ ] At least one consumer inventory attempt documented (even if all unknown)
- [ ] Matrix filled with severity per delta × consumer
- [ ] Every high/unknown has a mitigation or explicit research task
- [ ] Go / no-go recommendation stated

## Anti-patterns

- "Only mobile uses this" without evidence
- Treating semantic changes as non-breaking because JSON schema still validates
- Empty matrix with "LGTM"
- Ignoring machine consumers (jobs, webhooks, SDKs)

## Output template

```markdown
## Compatibility matrix

### Change set
1. ...

### Consumers
| id | type | evidence | owner |
|----|------|----------|-------|

### Matrix
| delta | consumer A | consumer B | unknown |
|-------|------------|------------|---------|
| ... | high: reason | none | unknown |

### Mitigations
| delta | plan | owner | ETA |
|-------|------|-------|-----|

### Decision
- Recommendation: ship-additive | version-bump | block | research
- Rationale: ...
```
