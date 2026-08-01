---
name: contract-first-openapi
description: >
  Drive API work contract-first with OpenAPI (or equivalent). Use when designing a new
  HTTP API, adding endpoints, writing or reviewing openapi.yaml/swagger, establishing
  review gates before implementation, or when the user says "/api-contract" or
  "spec before code". Prefer this over free-form endpoint inventing.
---

# Contract-First OpenAPI

## Overview

Public HTTP APIs should have a reviewable contract **before** (or tightly coupled with) implementation. This skill produces a minimal-but-complete OpenAPI-oriented contract review and an implementation checklist — not a novel on REST naming.

## Steps

1. **Discover existing contract**
   - Search for `openapi.yaml`, `openapi.yml`, `swagger.json`, `openapi.json`, `api/**/*.yaml`, generated specs.
   - Note source of truth: hand-written vs codegen vs framework annotations.

2. **Classify API surface**
   - Public external / partner / internal-only / unreleased.
   - Auth model: none, API key, session, OAuth2/JWT, mTLS.
   - Consistency style: REST resources, RPC-over-HTTP, mixed.

3. **Author or update contract (minimal complete set)**
   For each operation ensure:
   - `operationId`, method, path
   - Request parameters/body schema with required fields
   - Success response schema (not just `200 OK`)
   - Error model (problem+json or project standard) for 4xx/5xx you will return
   - Auth security requirement per operation
   - Pagination shape if lists exist
   - Idempotency header documented if mutation is retry-safe by design

4. **Review gate (must pass before coding handlers)**
   - [ ] No anonymous `object` / unconstrained maps on public fields without justification
   - [ ] Breaking-risk fields marked; new fields optional by default
   - [ ] Error codes stable and documented
   - [ ] Examples for happy path + one validation error
   - [ ] Versioning strategy stated (path `/v1`, header, or none + rationale)

5. **Implementation checklist**
   - Map each operation → handler/file
   - List validation rules that must match schema
   - List tests: contract/snapshot or schema assertion tests

6. **Write report** using the output template.

## Exit criteria

- [ ] Contract file path identified or created
- [ ] Every in-scope operation has request + success + error shape
- [ ] Review gate checklist completed (pass/fail with notes)
- [ ] Implementation checklist produced
- [ ] Explicit statement: ready to implement / blocked (why)

## Anti-patterns

- Inventing endpoints only in prose without schemas
- `additionalProperties: true` everywhere "for flexibility"
- Documenting only 200 responses
- Changing implementation first and reverse-engineering OpenAPI later without calling out drift
- Copying ECC-style resource naming essays instead of locking the actual contract

## Output template

```markdown
## Contract-first report

### Surface
- Visibility: public | partner | internal | unreleased
- Auth: ...
- Spec path: `...`
- Versioning: ...

### Operations in scope
| operationId | method path | request | responses | auth | notes |
|-------------|-------------|---------|-----------|------|-------|

### Review gate
| check | result | notes |
|-------|--------|-------|

### Implementation checklist
- [ ] ...

### Ready?
- [ ] Yes — implement against this contract
- [ ] No — blockers: ...
```

## References

- See repo `references/compatibility-rules.md` for what counts as a later break.
- Pair with `breaking-change-review` when editing an already-shipped spec.
