# Golden report — Billing API safe additive v1.1

**Fixture:** `examples/billing-api/openapi.v1.yaml` -> `openapi.v1.1-safe.yaml`  
**Maturity:** shipped public  
**Machine assist:** `python scripts/openapi_breaking_diff.py examples/billing-api/openapi.v1.yaml examples/billing-api/openapi.v1.1-safe.yaml`  
**Tool exit code:** `0` (no hard breaks)

---

## Scope

| Item | Value |
|------|--------|
| Specs | billing-api v1 -> v1.1-safe |
| Maturity | shipped |

---

## Deltas

| # | Delta | Class | Notes |
|---|--------|-------|-------|
| 1 | `GET /invoices/{id}/pdf` added | non-breaking | New surface |
| 2 | Optional `purchase_order` on create request | non-breaking | Server ignores if absent |
| 3 | Optional `purchase_order` on Invoice response | non-breaking | Old clients ignore |
| 4 | Optional `customer_id` query on list | non-breaking | Filter additive |

---

## Docs / SDK

- Changelog: yes (minor feature)  
- SDK: optional regenerate for new endpoint  

---

## Verdict

### **approve**

Additive-only evolution. No migration notes required for existing clients. Good template for "how to ship without a version bump."
