---
name: secure-api-surface
description: >
  Product-oriented HTTP API security review (object/function authz, oversharing,
  mass assignment). Use for public or authenticated APIs, "/api-secure", "BOLA",
  "BFLA", "IDOR", "API security review", or in Chinese
  "接口安全", "越权", "水平越权", "垂直越权", "过量数据暴露". Defensive findings only -
  not red-team exploits or binary audit workflows.
---

# Secure API Surface

> UUIDs are not authorization. Specs are not proof.

## Overview

Catch API abuse cases product engineers ship by accident. Stay on object-level authz, exposure, mass assignment, injection surfaces, and basic abuse controls.

## Scope

| In | Out |
|----|-----|
| Authn/z on resources | Reverse engineering, exploit PoCs |
| Oversharing / DTO leaks | Full org AppSec programs |
| Rate limit / pagination caps | Network pentests |
| Token/session misuse on APIs | Physical security |

## Steps

1. **Inventory** endpoints (OpenAPI or routes).
2. **Per authenticated resource op**
   - Object-level (BOLA/IDOR): user A + user B id?
   - Function-level (BFLA): non-admin -> admin op?
   - Tenant isolation?
3. **Exposure** - internal fields, tokens, PII on list/detail; chatty errors.
4. **Mass assignment** - client sets `role`, `isAdmin`, `price`, `ownerId`?
5. **Auth gaps** - missing auth; token footguns visible in code.
6. **Injection / SSRF** - query/body/file; user-supplied fetch URLs.
7. **Abuse** - rate limits on auth/expensive routes; max page size; unbounded bulk.
8. **Findings** - severity + concrete fix (code or gateway).

## Exit criteria

- [ ] Endpoint inventory
- [ ] Object- and function-level checks (or N/A + why)
- [ ] Exposure + mass assignment reviewed
- [ ] Findings table with severity + fixes
- [ ] Residual risk noted
- [ ] No exploit payload chains

## Anti-patterns

- Generic OWASP essay with no endpoint table
- Only finding: "use HTTPS"
- Dropping working exploits into the repo
- "We use UUIDs so IDOR is fine"

## Output template

```markdown
## Secure API surface review

### Scope
- Spec/routes: ...
- Auth model: ...

### Findings
| id | severity | endpoint | issue | fix |
|----|----------|----------|-------|-----|

### Checks
- [ ] Object-level authz
- [ ] Function-level authz
- [ ] Excessive data exposure
- [ ] Mass assignment
- [ ] Injection surfaces
- [ ] Rate / pagination limits

### Residual risk
- ...

### Verdict
- **block-merge** | **fix-then-merge** | **acceptable-with-followups**
```
