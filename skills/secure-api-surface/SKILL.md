---
name: secure-api-surface
description: >
  Product-oriented API security review (OWASP API style). Use when reviewing public
  or authenticated HTTP APIs for object-level authz, excess data exposure, mass
  assignment, rate limits, or when the user says "/api-secure", "BOLA", "BFLA",
  or "API security review". Defensive only — not penetration-tooling guidance.
---

# Secure API Surface

## Overview

Focus on **API abuse cases product engineers ship by accident**, not binary exploitation. Primary targets: broken object/function level authorization, excessive data exposure, weak auth, injection via parameters, and unrestricted flows.

## Scope boundary

| In scope | Out of scope (point elsewhere) |
|----------|--------------------------------|
| Authn/z on resources | Reverse engineering, exploit PoCs |
| Schema exposure / oversharing | Full org AppSec program |
| Rate limit / abuse basics | Network pentest |
| Token/session misuse on APIs | Physical security |

## Steps

1. **Inventory endpoints** under review (from OpenAPI or routes).

2. **For each authenticated resource operation, ask**
   - **Object-level (BOLA/IDOR):** Can user A pass user B's id and succeed?
   - **Function-level (BFLA):** Can a non-admin hit admin-only operations?
   - **Tenant isolation:** Cross-tenant id access?

3. **Data exposure**
   - Response DTOs vs DB models — leaked internal fields, tokens, PII?
   - List endpoints returning full objects when summaries suffice?
   - Error messages leaking existence/stack details?

4. **Mass assignment / over-posting**
   - Can client set `role`, `isAdmin`, `price`, `ownerId`?

5. **Auth & session**
   - Missing auth on sensitive routes?
   - JWT algorithm/acceptance footguns (if visible in code)?
   - Logout/revocation story for tokens if relevant?

6. **Injection & parsing**
   - SQL/NoSQL/command from query/body
   - File/path params
   - SSRF via user-supplied URLs (webhooks, importers)

7. **Abuse & availability**
   - Rate limiting on auth and expensive endpoints?
   - Pagination max limits?
   - Bulk endpoints unbounded?

8. **Severity & fix**
   - Rate each finding: critical/high/medium/low
   - Concrete fix (code or gateway), not vague "add security"

## Exit criteria

- [ ] Endpoint inventory listed
- [ ] Object-level and function-level checks performed (or N/A with reason)
- [ ] Exposure + mass assignment reviewed
- [ ] Findings table with severity and fixes
- [ ] Residual risks / testing gaps noted
- [ ] No exploit payload chains (defensive report only)

## Anti-patterns

- Generic OWASP essay without inspecting this API
- "Use HTTPS" as the only finding
- Dropping working exploit scripts into the repo
- Ignoring IDOR because "we use UUIDs" (UUIDs are not authz)

## Output template

```markdown
## Secure API surface review

### Scope
- Spec/routes: ...
- Auth model: ...

### Findings
| id | severity | endpoint | issue | fix |
|----|----------|----------|-------|-----|

### Checks performed
- [ ] Object-level authz
- [ ] Function-level authz
- [ ] Excessive data exposure
- [ ] Mass assignment
- [ ] Injection surfaces
- [ ] Rate/pagination limits

### Residual risk
- ...

### Verdict
- **block-merge** | **fix-then-merge** | **acceptable-with-followups**
```
