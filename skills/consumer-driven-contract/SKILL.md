---
name: consumer-driven-contract
description: >
  Capture consumer expectations and turn them into contract tests. Use when multiple
  clients depend on an API, when introducing Pact-style tests, when provider changes
  must not break consumers, or when the user says "/api-cdc", "consumer contract",
  or "Pact".
---

# Consumer-Driven Contract

## Overview

Provider-only OpenAPI is necessary but not sufficient. CDC captures **what consumers actually assert** (status, required fields, content-types) as executable checks the provider must pass.

## Steps

1. **Identify consumers in scope**
   - Name each consumer app/service and owner.

2. **Elicit expectations** (from code, not wishful thinking)
   - Grep client code for paths, required JSON keys, status handling.
   - For each interaction: given provider state → request → expected response minimum.

3. **Write consumer contracts** (framework-agnostic shape)
   - Prefer existing stack: Pact, Spring Cloud Contract, schemathesis against OpenAPI, custom schema tests.
   - Each interaction must be minimal (only fields consumer needs).

4. **Provider verification plan**
   - How CI runs provider tests against contracts
   - Can-i-deploy / gate before release

5. **Map to OpenAPI**
   - Ensure OpenAPI documents at least the consumer-required fields
   - Flag provider fields never consumed (candidates for future deprecation — do not delete yet)

6. **Change process**
   - Consumer changes contract first (or paired PR)
   - Provider implements / verifies
   - No breaking provider change without consumer contract update

## Exit criteria

- [ ] ≥1 consumer interaction documented with request/response minimum
- [ ] Test approach chosen and file paths proposed
- [ ] Provider CI verification step described
- [ ] OpenAPI alignment notes written
- [ ] Ownership: who updates contracts when clients change

## Anti-patterns

- Giant contracts that mirror entire OpenAPI (brittle, not consumer-driven)
- Contracts only on provider repo with no consumer input
- Asserting full exact body equality when only a few fields matter
- Skipping provider states for authenticated/list endpoints

## Output template

```markdown
## CDC plan

### Consumers
| name | repo/path | owner |
|------|-----------|-------|

### Interactions
| id | consumer | request | min response | provider state |
|----|----------|---------|--------------|----------------|

### Tooling
- Framework: Pact | OpenAPI tests | other: ...
- Consumer tests path: ...
- Provider verify path: ...
- CI gate: ...

### OpenAPI gaps
- ...

### Process
- ...
```
