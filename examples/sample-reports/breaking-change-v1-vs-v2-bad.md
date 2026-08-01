# Sample: Breaking change review (v1 → v2-bad)

Golden answer for demos. Agents should surface similar findings.

## Scope

- Spec/code: `examples/toy-orders-api/openapi.v1.yaml` → `openapi.v2-bad.yaml`
- API maturity: **shipped** (assumed)

## Deltas

| # | delta | class | client impact | migration |
|---|-------|-------|---------------|-----------|
| 1 | `listOrders` security removed | breaking | unauthenticated list; security regression | restore bearerAuth; treat as critical |
| 2 | `createOrder` success `201` → `200` | breaking | clients checking 201 fail | keep 201 or version bump + docs |
| 3 | `CreateOrderRequest.note` optional → required | breaking | old clients omit note → 400 | keep optional or default `""` + deprecate later |
| 4 | `Order.total_cents` removed; `amount` dollars added | semantic-breaking | wrong money if clients assume cents | dual-publish both fields; migrate; then deprecate cents |
| 5 | `Order.status` free string → enum OPEN/COMPLETE/VOID | breaking | pending/paid/… rejected or misunderstood | map old values; dual-read; long deprecation |
| 6 | `Order.note` removed | breaking | UI/clients reading note break | deprecate field first |
| 7 | `Order.customer_email` removed | breaking / product | may be intentional privacy | changelog + consumer notice |
| 8 | `Order.internal_score` added | non-breaking add but **security risk** | excess data exposure | remove from public schema |

## Verdict

**request-changes**

Do not merge v2-bad. Re-introduce additive evolution: keep v1 fields, add new fields optionally, use `deprecation-playbook` for removals, restore auth on listOrders, keep 201 for creates.
