# Golden report — Deprecation plan for money field rename

**Scenario:** Team wants `total_cents` / `amount_cents` -> major-unit floats.  
**Skill:** `deprecation-playbook` (+ `breaking-change-review` forbids silent rename)

---

## Surface

| Deprecated | Replacement |
|------------|-------------|
| `Invoice.total_cents` (integer) | `Invoice.total_cents` kept + new `Invoice.total_minor` clear name, OR keep cents forever |
| `LineItemInput.amount_cents` | keep cents; add optional `description` only |

**Recommendation:** Prefer **keeping integer minor units** (cents). If product insists on major units, dual-publish:

- Keep `total_cents` required through sunset  
- Add optional `total_decimal` string (avoid binary float)  
- Never replace in place  

---

## Usage

- Traffic: unknown in fixture (treat as **high risk** public)  
- Measure: gateway counts on `GET/POST /invoices` by SDK user-agent for 14 days  

---

## Strategy

**Additive dual-track** for 90 days public.

---

## Timeline

| Milestone | Date (example) | Criteria |
|-----------|----------------|----------|
| Announce | T+0 | Changelog + email partners |
| Soft deprecation | T+7 | Response header `Deprecation: true` on legacy-only clients if detectable |
| Dual fields live | T+7 | Both cents + new field present |
| Default docs switch | T+60 | Docs show new field first; cents still returned |
| Hard sunset | T+90+ | Only if metrics near zero; else extend |

---

## Engineering

- [x] Dual fields in OpenAPI  
- [ ] Metrics dashboard  
- [ ] SDK examples updated  
- [ ] No removal of `total_cents` in this PR  

---

## Rollback

Feature flag `billing.money_dual_fields` reverts response shape to v1-only.

---

## Verdict vs v2-risky

Silent rename in `openapi.v2-risky.yaml` **fails** this playbook. Correct path is dual-publish, not delete-and-replace.
