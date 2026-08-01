---
name: contract-first-openapi
description: >
  Contract-first OpenAPI workflow with a hard review gate before writing handlers.
  Use when designing new HTTP APIs, adding endpoints, writing or reviewing openapi.yaml,
  swagger, or API specs, or when the user says "/api-contract", "spec before code",
  "OpenAPI first", or in Chinese "先写契约", "先写 OpenAPI", "接口规范", "契约优先".
  Focus on complete operations, errors, auth, ready/blocked - not REST naming essays.
---

# Contract-First OpenAPI

> Spec is the product surface. Code implements the gate that passed.

## Overview

Produce a minimal-but-complete contract review and an implementation checklist. Lock request/response/error/auth so evolution skills have a baseline.

## Steps

1. **Find the source of truth**
   Search `openapi.yaml|yml`, `swagger.json`, `openapi.json`, annotated routes. Note hand-written vs generated.

2. **Classify the surface**
   - Visibility: public | partner | internal | unreleased
   - Auth: none | API key | session | OAuth2/JWT | mTLS
   - Style: REST resources | RPC-over-HTTP | mixed

3. **Complete each in-scope operation**
   - `operationId`, method, path
   - Request params/body + required fields
   - Success schema (not bare `200 OK`)
   - Error model (problem+json or project standard)
   - Per-operation security
   - List pagination shape if applicable
   - Document idempotency headers when mutations are retry-safe by design

4. **Review gate (must pass before handlers)**

   | Check | Pass? |
   |-------|-------|
   | No anonymous free-form objects on public fields without justification | |
   | New fields optional by default on shipped APIs | |
   | Stable error shape documented | |
   | Happy-path + one validation error example | |
   | Versioning strategy stated (path / header / none + why) | |

5. **Implementation checklist**
   Map operation -> handler file, validations that must match schema, contract tests to add.

6. Emit the report template.

## Exit criteria

- [ ] Spec path identified or created
- [ ] Every in-scope operation has request + success + error shape
- [ ] Review gate filled (pass/fail + notes)
- [ ] Implementation checklist written
- [ ] Explicit **ready** or **blocked** (with why)

## Anti-patterns

- Prose endpoints with no schemas
- `additionalProperties: true` everywhere "for flexibility"
- Only documenting 200 responses
- Reverse-engineering OpenAPI after ship without calling out drift
- Padding the report with REST naming lectures (out of scope)

## Output template

```markdown
## Contract-first report

### Surface
- Visibility: public | partner | internal | unreleased
- Auth: ...
- Spec path: `...`
- Versioning: ...

### Operations
| operationId | method path | request | responses | auth | notes |
|-------------|-------------|---------|-----------|------|-------|

### Review gate
| check | result | notes |
|-------|--------|-------|

### Implementation checklist
- [ ] ...

### Ready?
- [ ] Yes - implement against this contract
- [ ] No - blockers: ...
```

## References

- [compatibility-rules.md](references/compatibility-rules.md) - what becomes a break later
- Pair with `breaking-change-review` when editing a shipped spec
