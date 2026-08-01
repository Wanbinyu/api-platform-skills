---
name: deprecation-playbook
description: >
  Dated API deprecation plan with dual-track and consumer communication. Use when
  sunsetting endpoints or fields, migrating v1 to v2, or when the user says
  "/api-deprecate", "sunset", "deprecation plan", or in Chinese
  "弃用计划", "下线接口", "平滑迁移", "双轨运行". Not a same-PR delete checklist.
---

# Deprecation Playbook

> Deprecation is a release train, not a red delete button.

## Overview

Deliver a dated plan: measure usage -> choose strategy -> signals (headers/docs) -> consumer checklist -> rollback.

## Steps

1. **Name the surface** - what dies, what replaces it (operationIds / version links).
2. **Measure or escalate risk** - path counts, partner ids, user-agents. No metrics => high risk, longer window or forced inventory.
3. **Pick a strategy**

   | Strategy | When |
   |----------|------|
   | Additive dual-track | Default public APIs |
   | Header warnings only | Low-traffic internal |
   | Big-bang cutover | Single consumer, same deploy train |
   | Emulation adapter | Old shape over new internals |

4. **Timeline** - announce, soft (warnings), optional default switch, hard sunset.
   Suggested floors: internal single-team days-2w; multi-team 30d+; public/partner 90d+ or contract.
5. **Signals** - Deprecation/Sunset headers, portal/changelog, migration guide, post-deadline error body optional.
6. **Per-consumer checklist** - owner, task, done criteria.
7. **Rollback** - how to re-enable the old path.

## Exit criteria

- [ ] Deprecated surface + replacement listed
- [ ] Usage plan or high-risk waiver
- [ ] Strategy + rationale
- [ ] Dated milestones
- [ ] Headers/docs/changelog tasks listed
- [ ] Consumers or accepted unknown risk
- [ ] Rollback path

## Anti-patterns

- Delete and "deprecate" in the same PR
- Sunset date = "someday"
- Public API + no metrics + short window
- Silent dual-write with unclear source of truth

## Output template

```markdown
## Deprecation plan

### Surface
- Deprecated: ...
- Replacement: ...

### Usage
- Traffic: ... | unknown (risk: high)
- Measured by: ...

### Strategy
- ...

### Timeline
| milestone | date | criteria |
|-----------|------|----------|
| Announce | | |
| Soft deprecation | | headers live |
| Hard sunset | | old path returns ... |

### Engineering
- [ ] Headers
- [ ] Docs / changelog
- [ ] Metrics
- [ ] Dual-track / adapter
- [ ] Fail-closed sunset behavior

### Consumers
| consumer | contact | status |
|----------|---------|--------|

### Rollback
- ...
```
