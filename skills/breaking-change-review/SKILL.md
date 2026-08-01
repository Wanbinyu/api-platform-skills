---
name: breaking-change-review
description: >
  PR-grade breaking change audit for shipped HTTP APIs. Use on PRs touching OpenAPI,
  public DTOs/handlers, status codes, or auth; on field removals/renames; or when the
  user asks "is this breaking?", "/api-break", "breaking change review", "can we merge
  this API change", or in Chinese "破坏性变更", "有没有 break", "能不能合并这个接口",
  "兼容吗", "字段删了行不行". Requires migration notes or an explicit waiver.
---

# Breaking Change Review

> Merge verdict or it did not happen.

## Overview

Classify every contract delta, demand migration notes for breaks, emit
**approve / request-changes / version-bump / waiver**.

## Catalog (shipped APIs)

**Usually breaking**

| Category | Examples |
|----------|----------|
| Surface | Remove endpoint/method |
| Shape | Remove/rename field; type/nullability tighten |
| Enums | Remove value |
| Auth | Newly required auth; narrowed scopes |
| Protocol | Success status clients branch on; parsed error codes |
| Validation | Reject previously accepted requests |
| Semantics | Same schema, different meaning |
| Pagination | Cursor format change; surprising default size cuts |

**Usually non-breaking**

- Optional response field, new endpoint, optional request field with server default
- New enum value (if clients must tolerate unknowns - document)
- Relaxed validation, new documented error code for a new failure mode

## Steps

1. **Before / after** - OpenAPI diff, or reconstruct public shapes from code.
2. **Atomic deltas** - one row per change.
3. **Classify** - `non-breaking | breaking | semantic-breaking | unclear`.
4. **For each break** - migration note + version strategy, or written waiver (internal-only / multi-repo same day).
5. **Docs and SDK** - changelog? regenerate clients?
6. **Verdict** - see template.

## Exit criteria

- [ ] Before/after sources named
- [ ] All deltas classified
- [ ] Every break has migration + strategy or waiver
- [ ] Merge verdict + rationale
- [ ] Report uses the template below

## Anti-patterns

- "Just a rename, clients will update" without a plan
- Approving removals because "nobody should use that"
- Ignoring error body / status changes
- "Non-breaking" only because the server compiles
- Dumping a full REST style guide instead of a delta table

## Output template

```markdown
## Breaking change review

### Scope
- Spec/code: `...`
- Maturity: shipped | beta | unreleased | internal

### Deltas
| # | delta | class | client impact | migration |
|---|-------|-------|---------------|-----------|

### Waivers
| # | reason | evidence |
|---|--------|----------|

### Docs / SDK
- Changelog: yes/no
- SDK: yes/no/n/a

### Verdict
- **request-changes** | **approve** | **approve-with-version-bump** | **waiver-documented**
- Rationale: ...
- Follow-ups: ...
```

## References

- [compatibility-rules.md](references/compatibility-rules.md)
- Next: `deprecation-playbook` when removing after a window
