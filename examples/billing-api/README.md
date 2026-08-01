# Toy Billing API fixtures

More realistic than Orders for money / idempotency / deprecation drills.

| File | Intent |
|------|--------|
| [`openapi.v1.yaml`](openapi.v1.yaml) | Shipped baseline |
| [`openapi.v1.1-safe.yaml`](openapi.v1.1-safe.yaml) | Additive only — expect **approve** |
| [`openapi.v2-risky.yaml`](openapi.v2-risky.yaml) | Cleanup PR with breaks — expect **request-changes** |

## Machine assist

```bash
# from repo root
python scripts/openapi_breaking_diff.py \
  examples/billing-api/openapi.v1.yaml \
  examples/billing-api/openapi.v2-risky.yaml

python scripts/openapi_breaking_diff.py \
  examples/billing-api/openapi.v1.yaml \
  examples/billing-api/openapi.v1.1-safe.yaml
```

## Golden reports

- [../sample-reports/breaking-change-billing-v1-vs-v2-risky.md](../sample-reports/breaking-change-billing-v1-vs-v2-risky.md)
- [../sample-reports/breaking-change-billing-v1-vs-v1.1-safe.md](../sample-reports/breaking-change-billing-v1-vs-v1.1-safe.md)
- [../sample-reports/deprecation-billing-money-fields.md](../sample-reports/deprecation-billing-money-fields.md)
