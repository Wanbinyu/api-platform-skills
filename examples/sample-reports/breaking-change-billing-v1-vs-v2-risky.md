# Golden report — Billing API risky v2

**Fixture:** `examples/billing-api/openapi.v1.yaml` -> `openapi.v2-risky.yaml`  
**Maturity:** shipped public  
**Machine assist:** `python scripts/openapi_breaking_diff.py examples/billing-api/openapi.v1.yaml examples/billing-api/openapi.v2-risky.yaml`

---

## Scope

| Item | Value |
|------|--------|
| Specs | billing-api v1 -> v2-risky |
| Maturity | shipped |

---

## Deltas (curated)

| # | Delta | Class | Migration |
|---|--------|-------|-----------|
| 1 | `memo` optional -> required on create | breaking | Keep optional or default `""` |
| 2 | Line item `amount_cents` removed; `unit_amount` dollars added | semantic-breaking | Dual-publish both; never rename money units silently |
| 3 | Invoice `total_cents` removed; `total` dollars added | semantic-breaking | Same as above |
| 4 | `hosted_invoice_url` removed | breaking | Deprecate first; keep until partners migrate |
| 5 | `status` enum loses `void` | breaking | Keep `void` or map to new value with dual-read |
| 6 | Pay success `200` -> `202` | breaking | Accept both during window or version bump |
| 7 | `idempotency_key` becomes required on pay | breaking | Prefer header `Idempotency-Key` additive; do not force body field without version |
| 8 | `collector_score` added on Invoice | non-breaking add + **security risk** | Remove from public schema |

---

## Docs / SDK

- Changelog: required  
- SDK regenerate: yes after safe redesign  

---

## Verdict

### **request-changes**

Do not merge v2-risky. Money unit changes and status/enum removals need dual-publish + `deprecation-playbook`. Making idempotency required is good *direction* but must be additive-first for shipped clients.
