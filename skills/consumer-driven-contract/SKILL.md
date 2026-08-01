---
name: consumer-driven-contract
description: >
  Capture consumer expectations and turn them into provider CI gates (CDC / Pact-style).
  Use for multi-client APIs, contract tests, "/api-cdc", "consumer contract", "Pact".
  Focus on minimal consumer assertions — not cloning the entire OpenAPI into a test.
---

# Consumer-Driven Contract

> Providers don’t guess. Consumers assert. CI enforces.

## Overview

OpenAPI is necessary; CDC records **what each consumer actually requires** (status, required keys, content-type) as executable checks.

## Steps

1. **Name consumers** — app/service + owner.  
2. **Elicit from code** — grep clients for paths, required keys, status branches (not wish lists).  
3. **Write minimal interactions** — provider state → request → **minimum** response. Prefer existing stack: Pact, Spring Cloud Contract, OpenAPI/schema tests, custom.  
4. **Provider verification** — CI job, can-i-deploy / merge gate.  
5. **Align OpenAPI** — spec must cover consumer-required fields; unused fields are deprecation *candidates* only.  
6. **Process** — consumer updates contract (or paired PR) before provider breaks them.

## Exit criteria

- [ ] ≥1 interaction with request + min response  
- [ ] Tooling + file paths proposed  
- [ ] Provider CI verification described  
- [ ] OpenAPI gaps listed  
- [ ] Ownership of contract updates clear  

## Anti-patterns

- Contracts that mirror entire OpenAPI (brittle, not consumer-driven)  
- Provider-only contracts with no consumer input  
- Full-body exact equality when three fields matter  
- Skipping provider states for auth/list flows  

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
- Framework: Pact | OpenAPI tests | other: …
- Consumer tests: …
- Provider verify: …
- CI gate: …

### OpenAPI gaps
- …

### Process
- …
```
