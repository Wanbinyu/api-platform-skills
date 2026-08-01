---
name: compatibility-matrix
description: >
  Build a consumer blast-radius matrix for an API change. Use when asking who breaks
  if a field, endpoint, status code, or auth changes; planning migrations; or
  "/api-compat", "blast radius", "consumer impact", or in Chinese
  "谁会挂", "影响面", "兼容矩阵", "调用方影响". This is impact analysis, not API style design.
---

# Compatibility Matrix

> Rows are deltas. Columns are consumers. Empty cells are failures.

## Overview

Map what changes -> who consumes it -> severity -> mitigation. Document unknowns; do not invent traffic you cannot evidence.

## Steps

1. **Freeze the change set**
   Atomic deltas only: add/remove/rename/retype, path, status, header, auth, semantic change (same JSON, new meaning).

2. **Inventory consumers** (best effort)
   First-party web/mobile, internal services, partners, SDKs, jobs/webhooks, unknown.
   Evidence: grep paths/operationIds, gateway notes, README, user-stated owners.

3. **Classify each delta**

   | Class | Examples |
   |-------|----------|
   | Safe additive | New optional field, new endpoint |
   | Soft risk | New required request field; tighter validation |
   | Hard break | Remove/rename/retype; remove endpoint |
   | Semantic break | Same shape, different meaning (e.g. cents -> dollars) |

4. **Fill the matrix**
   Cells: `none | low | high | unknown` + one-line reason.

5. **Mitigations for every high/unknown**
   Dual-write/read, deprecation window, version bump, adapter, feature flag, research task.

6. **Decision**
   `ship-additive` | `version-bump` | `block` | `research`.

## Exit criteria

- [ ] Discrete deltas listed
- [ ] Consumer inventory attempted (unknowns explicit)
- [ ] Matrix complete for delta x consumer
- [ ] Every high/unknown has mitigation or research task
- [ ] Go/no-go stated

## Anti-patterns

- "Only mobile uses this" with no evidence
- Treating semantic breaks as safe because JSON Schema still validates
- Empty matrix + "LGTM"
- Ignoring machine consumers (cron, webhooks, generated SDKs)

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

### Mitigations
| delta | plan | owner | ETA |
|-------|------|-------|-----|

### Decision
- Recommendation: ship-additive | version-bump | block | research
- Rationale: ...
```

## References

- [compatibility-rules.md](references/compatibility-rules.md)
