# Idempotency patterns (quick reference)

## Pattern A — Natural key

```http
PUT /v1/orders/{clientOrderId}
```

Same client key → same resource. Prefer when clients can allocate ids.

## Pattern B — Idempotency-Key header

```http
POST /v1/payments
Idempotency-Key: 8e03978e-40d5-43e8-bc93-6894a57f9324
```

Server stores key → outcome. Replay returns original outcome.

### Conflict

Same key, different canonical body hash → `409 Conflict` (recommended).

### Storage row (conceptual)

| key | body_hash | status | resource_id | response_code | created_at | expires_at |
|-----|-----------|--------|-------------|---------------|------------|------------|

## Pattern C — Dedupe on business fingerprint

E.g. hash(user_id + cart_id + amount + day). Weaker; use only when keys unavailable.

## Retry guidance

| Operation | Retry without key? |
|-----------|--------------------|
| GET | Yes |
| PUT/DELETE by id | Usually yes |
| POST without key | **No** |
| POST with key | Yes (same key) |

## Testing minimum

1. Sequential double submit  
2. Concurrent double submit  
3. Body mismatch on same key  
4. Expired key behavior  
