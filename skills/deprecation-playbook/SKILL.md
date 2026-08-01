---
name: deprecation-playbook
description: >
  Plan and execute API deprecation without surprising consumers. Use when sunsetting
  endpoints or fields, migrating from v1 to v2, dual-running versions, or when the user
  says "/api-deprecate", "sunset", "deprecation plan".
---

# Deprecation Playbook

## Overview

Deprecation is a **communication + dual-track + measurement** problem, not a delete PR. This skill produces a dated plan with signals (headers, docs, metrics) and a hard sunset criteria.

## Steps

1. **Define what is deprecated**
   - Endpoints, fields, auth modes, base URLs.
   - Replacement contract (links to new operationIds / version).

2. **Measure current usage** (or document how to)
   - Logs/metrics: request counts by path, user/agent, partner id.
   - If no metrics: treat as **high risk**; require longer window or forced inventory.

3. **Choose strategy**

   | Strategy | When |
   |----------|------|
   | Additive dual-track | Default for public APIs |
   | Header-only warning | Low traffic internal |
   | Big-bang cutover | Single consumer, coordinated deploy only |
   | Emulation adapter | Old shape served from new internals |

4. **Timeline**
   - Announce date
   - Soft deprecation (warnings)
   - Default switch (if any)
   - Hard sunset (fail closed)
   - Minimum windows (suggested defaults — adjust for audience):
     - Internal single-team: days–2 weeks
     - Multi-team internal: 30+ days
     - Public/partner: 90+ days or contractual

5. **Signals to implement**
   - `Deprecation` / `Sunset` headers (RFC 8594 style where applicable)
   - Warning in response body or docs portal
   - Changelog + migration guide
   - Optional: sunset date in error body after deadline

6. **Consumer checklist**
   - Per known consumer: contact, migration task, done criteria.

7. **Rollback**
   - How to re-enable old path if sunset fails.

## Exit criteria

- [ ] Deprecated surface + replacement listed
- [ ] Usage measurement plan or explicit high-risk waiver
- [ ] Strategy chosen with rationale
- [ ] Dated timeline with announce / soft / hard milestones
- [ ] Header/docs/changelog signals specified
- [ ] Consumer checklist (or unknown-consumer risk accepted in writing)
- [ ] Rollback path documented

## Anti-patterns

- Deleting endpoints in the same PR as "deprecation"
- No sunset date ("someday")
- No metrics and short window for public APIs
- Silent dual-write without documenting which source of truth wins

## Output template

```markdown
## Deprecation plan

### Surface
- Deprecated: ...
- Replacement: ...

### Usage
- Current traffic: ... | unknown (risk: high)
- How measured: ...

### Strategy
- ...

### Timeline
| milestone | date | criteria |
|-----------|------|----------|
| Announce | | |
| Soft deprecation | | headers live |
| Hard sunset | | old path returns ... |

### Engineering tasks
- [ ] Headers
- [ ] Docs/changelog
- [ ] Metrics dashboard
- [ ] Adapter/dual-track code
- [ ] Sunset fail-closed behavior

### Consumers
| consumer | contact | status |
|----------|---------|--------|

### Rollback
- ...
```
