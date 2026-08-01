# Toy Orders API (demo)

Intentionally simple OpenAPI pair for practicing skills:

| File | Role |
|------|------|
| `openapi.v1.yaml` | Shipped contract (baseline) |
| `openapi.v2-bad.yaml` | Proposed change with **deliberate breaks** |

## Exercises

1. **breaking-change-review**  
   Compare v1 vs v2-bad. Expect findings: removed field, renames, auth change, status change.

2. **compatibility-matrix**  
   Assume consumers: `web-checkout`, `mobile-app`, `partner-erp` (unknown usage on partner).

3. **deprecation-playbook**  
   Plan how v1 `status` string → v2 enum should have been done safely.

4. **secure-api-surface**  
   Review `GET /orders/{id}` for object-level auth notes (spec alone cannot prove IDOR — list what code must enforce).

5. **idempotency-and-retries**  
   Design keys for `POST /orders` (v1 has no idempotency — propose additive change).
