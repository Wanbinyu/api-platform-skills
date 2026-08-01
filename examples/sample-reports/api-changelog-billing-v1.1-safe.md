# Sample — API Changelog (billing v1.1 safe)

Generated style target for skill `api-changelog` on:

- before: `examples/billing-api/openapi.v1.yaml`
- after: `examples/billing-api/openapi.v1.1-safe.yaml`

---

# API Changelog

## [1.1.0] - 2026-08-01

### Summary

Additive-only release for the Billing API. Existing clients keep working with no code changes. New optional purchase-order fields and a PDF download endpoint.

- Maturity: shipped
- Compatibility: **additive-only**

### Breaking changes

_None._

### Semantic changes

_None._

### Deprecated (still work)

_None._

### Added

- `GET /invoices/{invoiceId}/pdf` - download invoice PDF (auth required)
- Optional `purchase_order` on `POST /invoices` request body
- Optional `purchase_order` on `Invoice` responses
- Optional query `customer_id` on `GET /invoices` to filter by customer

### Fixed (contract-visible only)

_None._

### Security

_No auth changes._

### Migration checklist

- [ ] (Optional) Call `GET /invoices/{id}/pdf` if you need PDFs
- [ ] (Optional) Send `purchase_order` on create if your ERP needs it
- [ ] Regenerate SDK only if you want typed access to new fields

### Support

- Docs: Billing API guide
- Contact: api-support@example.com

### Publish?

- [x] Yes - consumer-ready

---

### Short blurb

**API 1.1.0** (2026-08-01)

- Breaks: none  
- Adds: invoice PDF endpoint, optional purchase_order, list filter by customer  
- Action: none required for existing integrations  
