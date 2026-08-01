---
name: idempotency-and-retries
description: >
  Design idempotent mutations and safe retry policies. Use for create/payment/order
  endpoints, client timeouts, double-submit, Idempotency-Key, "/api-idempotent",
  "retry-safe", "exactly-once", or in Chinese "幂等", "重试", "重复下单", "防重复提交".
  Reliability design - not REST resource naming.
---

# Idempotency and Retries

> Networks retry. Users double-click. Design for replays.

## Overview

Aim for at-least-once delivery + idempotent handlers. Specify keys, storage, conflicts, timeouts, and tests.

## Steps

1. **Classify operations**

   | Kind | Examples | Need |
   |------|----------|------|
   | Safe read | GET | Natural |
   | Intrinsic idempotent | PUT replace, DELETE by id | Resource key |
   | Unsafe create | POST payment/order | Key or natural key |
   | Side-effect RPC | POST send-email | Key / dedupe store |

2. **Choose mechanism**
   - Natural: `PUT /orders/{clientOrderId}`
   - Header: `Idempotency-Key` (or project standard) on POST
   - Dedupe row: key -> outcome, TTL
   - Same key + different body -> `409` (recommended) or documented error

3. **Storage semantics** - body hash, status, resource id, TTL, uniqueness/lock.
4. **Retry policy** - upstream timeouts shorter than downstream; backoff + jitter; never blind-retry unkeyed POST; propagate trace ids.
5. **Failure modes** - response lost after commit; partial downstream success; key reuse mismatch.
6. **Tests** - sequential double POST; concurrent double; body mismatch; post-TTL behavior.

## Exit criteria

- [ ] Mutations classified
- [ ] Mechanism named (header / natural key)
- [ ] Storage + TTL + conflict defined
- [ ] Client/worker retry policy written
- [ ] Test list present
- [ ] Docs/OpenAPI note on checklist

## Anti-patterns

- "Just retry POST" without keys
- Accepting keys but not persisting them
- Infinite retries on non-idempotent calls
- Identical timeouts on every hop
- Different bodies returned for the same key

## Output template

```markdown
## Idempotency design

### Operations
| operation | class | mechanism | conflict | TTL |
|-----------|-------|-----------|----------|-----|

### Storage
- ...

### Retry policy
- Client: ...
- Worker: ...
- Do not retry: ...

### Tests
- [ ] ...

### Docs
- Header/param: ...
- Example: ...
```

## References

- [idempotency-patterns.md](references/idempotency-patterns.md)
