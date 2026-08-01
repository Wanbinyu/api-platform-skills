# Idempotency patterns

## A — Natural key

```http
PUT /v1/orders/{clientOrderId}
```

Client-allocated id ⇒ same key, same resource.

## B — Idempotency-Key header

```http
POST /v1/payments
Idempotency-Key: 8e03978e-40d5-43e8-bc93-6894a57f9324
```

| Same key + same body | Replay original outcome |
| Same key + different body | Prefer `409 Conflict` |

### Storage (conceptual)

| key | body_hash | status | resource_id | response_code | expires_at |
|-----|-----------|--------|-------------|---------------|------------|

## C — Business fingerprint

e.g. hash(user + cart + amount + day) — weaker; last resort.

## Retry cheat sheet

| Operation | Retry without key? |
|-----------|--------------------|
| GET | Yes |
| PUT/DELETE by id | Usually yes |
| POST without key | **No** |
| POST with same key | Yes |

## Minimum tests

1. Sequential double submit  
2. Concurrent double submit  
3. Body mismatch on same key  
4. Expired key behavior  
