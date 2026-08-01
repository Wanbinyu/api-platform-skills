---
name: webhook-design
description: >
  Design reliable, secure webhooks and outbound event delivery. Use when adding
  callbacks, Stripe-like event posts, partner notifications, or when the user says
  "/api-webhook", "event delivery", or "signed webhooks".
---

# Webhook Design

## Overview

Webhooks are **asynchronous public APIs you call on customers**. Assume at-least-once delivery, hostile receivers, and replay attacks. Design signing, retries, and event identity up front.

## Steps

1. **Event model**
   - Event types (stable strings)
   - Event id (unique, for consumer dedupe)
   - Payload versioning (`api_version` or schema version)
   - Thin vs thick payloads (id-only + fetch vs full snapshot) — pick and document

2. **Delivery semantics**
   - At-least-once (default)
   - Ordering: per-resource best-effort vs none (document clearly)
   - Retry schedule with exponential backoff + give-up + dead-letter/manual replay

3. **Security**
   - HMAC signature header (algorithm, which bytes signed, timestamp)
   - Timestamp tolerance to limit replay
   - Optional mTLS or IP allowlist for enterprise
   - Secrets rotation process
   - Never send secrets in query strings

4. **Receiver contract**
   - Expected success status codes (2xx)
   - Timeout budget (e.g. 5s) — slow receivers get retries
   - Consumer idempotency on `event.id`

5. **Observability**
   - Delivery attempts log: event id, URL host, status, latency
   - Dashboard: failure rate, oldest unacknowledged

6. **API surface for management** (if productized)
   - Register URL, rotate secret, list event types, test ping endpoint

7. **Docs checklist**
   - Signature verification sample
   - Retry policy
   - Event catalog

## Exit criteria

- [ ] Event types + event id scheme defined
- [ ] Delivery/retry/give-up policy written
- [ ] Signature scheme specified (headers + algorithm + rotation)
- [ ] Receiver timeout and success codes documented
- [ ] Consumer dedupe guidance included
- [ ] Ops/replay path mentioned

## Anti-patterns

- Unsigned webhooks to the public internet
- Infinite retries with no backoff
- Assuming exactly-once delivery
- Changing event payload shape without versioning
- Logging full payloads with PII at info level

## Output template

```markdown
## Webhook design

### Events
| type | payload | versioning |
|------|---------|------------|

### Delivery
- Semantics: at-least-once
- Retry: ...
- Give-up: ...
- Replay: ...

### Security
- Signature: ...
- Timestamp window: ...
- Rotation: ...

### Receiver requirements
- ...

### Observability
- ...

### Open items
- ...
```
