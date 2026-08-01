---
name: idempotency-and-retries
description: >
  Design idempotent APIs and safe retry behavior. Use for create/payment/order
  endpoints, client timeouts, double-submit, Idempotency-Key headers, or when the
  user says "/api-idempotent", "retry-safe", or "exactly-once".
---

# Idempotency and Retries

## Overview

Networks retry. Users double-click. Clients time out after the server succeeded. Design mutations so **replays do not corrupt state**. True exactly-once is rare; aim for **at-least-once + idempotent handlers**.

## Steps

1. **Classify operations**

   | Kind | Examples | Idempotency need |
   |------|----------|------------------|
   | Safe read | GET | Natural |
   | Intrinsic idempotent | PUT full replace, DELETE | Usually by resource key |
   | Unsafe create | POST payment, POST order | **Requires key or natural key** |
   | Side-effecting RPC | POST /send-email | Key or dedupe store |

2. **Choose idempotency mechanism**
   - Natural key: `PUT /orders/{clientOrderId}`
   - Header: `Idempotency-Key` (or project standard) on POST
   - Dedupe table: key → response snapshot / resource id, with TTL
   - Document conflict behavior: same key + same body → same result; same key + different body → `409` or documented error

3. **Specify storage semantics**
   - What is stored: status, response body hash, resource id
   - TTL and replay window
   - Concurrency: first writer wins; lock or unique constraint

4. **Timeouts and retries (client + server + dependency)**
   - Timeouts must be **shorter upstream than downstream** (avoid retry storms)
   - Retry only idempotent or keyed operations
   - Backoff + jitter; cap attempts
   - Propagate correlation/trace ids

5. **Failure modes to design explicitly**
   - Server committed, response lost
   - Partial downstream success (payment ok, DB fail) — saga/compensation note
   - Key reuse with different payload

6. **Tests**
   - Double POST same key → one resource
   - Parallel double POST → one resource
   - Different body same key → conflict
   - After TTL → define behavior

## Exit criteria

- [ ] Each in-scope mutation classified
- [ ] Mechanism chosen and documented (header name / natural key)
- [ ] Storage + TTL + conflict semantics specified
- [ ] Retry policy for clients and workers specified
- [ ] Test cases listed
- [ ] OpenAPI/docs note for clients added to checklist

## Anti-patterns

- "Just retry POST" without keys
- Idempotency key accepted but not stored (theater)
- Infinite retries on non-idempotent calls
- Same timeout on every hop
- Returning different bodies for the same key on replay

## Output template

```markdown
## Idempotency design

### Operations
| operation | class | mechanism | conflict | TTL |
|-----------|-------|-----------|----------|-----|

### Storage
- Store: ...
- Uniqueness: ...

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

- `references/idempotency-patterns.md`
