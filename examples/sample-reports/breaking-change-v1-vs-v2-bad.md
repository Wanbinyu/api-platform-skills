# Golden report — Breaking change review

**Fixture:** `openapi.v1.yaml` → `openapi.v2-bad.yaml`  
**Assumed maturity:** shipped public API  

Agents should surface the same classes of findings (wording may differ).

---

## Scope

| Item | Value |
|------|--------|
| Specs | `examples/toy-orders-api/openapi.v1.yaml` → `openapi.v2-bad.yaml` |
| Maturity | shipped |

---

## Deltas

| # | Delta | Class | Client impact | Migration |
|---|--------|-------|---------------|-----------|
| 1 | `listOrders` security removed | **breaking** | Unauthenticated list; security regression | Restore `bearerAuth`; treat as critical |
| 2 | `createOrder` success `201` → `200` | **breaking** | Clients branching on 201 fail | Keep 201 or version + docs |
| 3 | `note` optional → **required** on create | **breaking** | Old clients omit note → 400 | Keep optional or default `""` |
| 4 | `total_cents` removed; `amount` dollars added | **semantic-breaking** | Wrong money if clients assume cents | Dual-publish both fields; migrate; then deprecate cents |
| 5 | `status` free string → enum `OPEN/COMPLETE/VOID` | **breaking** | Old values misunderstood | Map old values; dual-read; long deprecation |
| 6 | `Order.note` removed | **breaking** | Readers of note break | Deprecate first |
| 7 | `customer_email` removed | **breaking** (may be intentional privacy) | Email consumers break | Changelog + notice |
| 8 | `internal_score` added | additive but **security risk** | Excess data exposure | Remove from public schema |

---

## Verdict

### **request-changes**

Do **not** merge `v2-bad`.

Safe path: additive evolution — keep v1 fields, add new fields as optional, use `deprecation-playbook` for removals, restore list auth, keep `201` for creates, never rename money units without dual-read.
