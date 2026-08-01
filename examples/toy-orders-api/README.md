# Toy Orders API

Deliberate teaching fixture for **API Platform Skills**.

| File | Role |
|------|------|
| [`openapi.v1.yaml`](openapi.v1.yaml) | Shipped baseline |
| [`openapi.v2-bad.yaml`](openapi.v2-bad.yaml) | Upgrade full of **silent breaks** |
| [../sample-reports/breaking-change-v1-vs-v2-bad.md](../sample-reports/breaking-change-v1-vs-v2-bad.md) | Golden review |

```bash
python scripts/openapi_breaking_diff.py \
  examples/toy-orders-api/openapi.v1.yaml \
  examples/toy-orders-api/openapi.v2-bad.yaml
```

Also see [`../billing-api/`](../billing-api/) for a money/idempotency-oriented fixture pair.

## Try these prompts

**Breaking change**

```text
Compare openapi.v1.yaml with openapi.v2-bad.yaml.
Follow breaking-change-review. Merge verdict required.
```

**Compatibility**

```text
Build a compatibility-matrix. Consumers: web-checkout, mobile-app, partner-erp (unknown traffic).
```

**Deprecation (how v2 should have been done)**

```text
Using deprecation-playbook, plan a safe path from v1 status strings to a new enum.
```

**Idempotency**

```text
v1 POST /orders has no idempotency. Design an additive fix with idempotency-and-retries.
```

**Security surface**

```text
Review GET /orders/{orderId} with secure-api-surface. List what code must enforce beyond the spec.
```
