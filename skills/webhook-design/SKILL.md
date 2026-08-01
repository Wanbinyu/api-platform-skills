---
name: webhook-design
description: >
  Design signed, retry-safe outbound webhooks. Use for callbacks, partner event posts,
  "/api-webhook", "event delivery", "signed webhooks". Focus on event identity, HMAC,
  at-least-once delivery — not generic REST CRUD style.
---

# Webhook Design

> You are the client now. Receivers are hostile and slow.

## Overview

Assume **at-least-once** delivery, replay attacks, and flaky receivers. Lock event ids, signatures, retries, and consumer dedupe.

## Steps

1. **Event model** — stable type strings · unique event id · payload version · thin vs thick body (document choice).  
2. **Delivery** — retry schedule + give-up + dead-letter/manual replay · ordering guarantees (per-resource best-effort vs none).  
3. **Security** — HMAC (algorithm, signed bytes, header names) · timestamp skew window · secret rotation · no secrets in query strings · optional mTLS/allowlist.  
4. **Receiver contract** — 2xx success · timeout budget · consumer must dedupe on `event.id`.  
5. **Observability** — attempts log · failure rate · oldest unacked.  
6. **Management API** (if productized) — register URL, rotate secret, test ping.  
7. **Docs** — verify sample · retry policy · event catalog.

## Exit criteria

- [ ] Event types + id scheme  
- [ ] Retry / give-up / replay  
- [ ] Signature + rotation  
- [ ] Receiver timeout + success codes  
- [ ] Consumer dedupe guidance  
- [ ] Ops/replay path  

## Anti-patterns

- Unsigned public webhooks  
- Infinite retries, no backoff  
- Claiming exactly-once  
- Payload shape changes without versioning  
- Info-logging full PII payloads  

## Output template

```markdown
## Webhook design

### Events
| type | payload | versioning |
|------|---------|------------|

### Delivery
- Semantics: at-least-once
- Retry: …
- Give-up: …
- Replay: …

### Security
- Signature: …
- Timestamp window: …
- Rotation: …

### Receiver requirements
- …

### Observability
- …

### Open items
- …
```
