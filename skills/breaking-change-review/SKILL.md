---
name: breaking-change-review
description: >
  Review API changes for breaking compatibility. Use on PRs that touch OpenAPI specs,
  public handlers, DTOs, status codes, or auth; when removing/renaming fields; or when
  the user says "/api-break", "is this breaking?", or "breaking change review".
---

# Breaking Change Review

## Overview

Produce a PR-grade audit: classify each contract delta, require migration notes for breaks, and give a merge verdict. Assumes shipped or externally consumed APIs unless labeled unreleased.

## Breaking change catalog (non-exhaustive)

Treat as **breaking** unless API is unreleased/internal-with-agreement:

- Remove endpoint or HTTP method
- Remove or rename response/request field
- Change field type or nullability (optional → required; nullable → non-null)
- Change enum set incompatibly (remove value)
- Change auth requirement (open → auth, or scopes tightened unexpectedly)
- Change success status code clients branch on
- Change error code strings clients parse
- Tighten validation rejecting previously accepted requests
- Change default values that alter behavior
- Semantic change with identical schema
- Pagination/cursor format change
- Pagination: default page size change that truncates results unexpectedly (flag as risk)

Usually **non-breaking**:

- Add optional response field
- Add endpoint
- Add optional request field with default server-side
- Add enum value (consumers should tolerate unknowns if documented)
- Relax validation (accept more)
- Add new error code for new failure mode (document it)

## Steps

1. **Obtain before/after**
   - Diff OpenAPI files, or reconstruct from DTO/handler diff if no spec.
   - If only code: extract public request/response shapes.

2. **List discrete deltas** (atomic, reviewable).

3. **Classify** each: `non-breaking | breaking | semantic-breaking | unclear`.

4. **For every breaking/semantic-breaking**
   - Required: migration note (what clients must do)
   - Required: version strategy (new version path/header vs coordinated deploy)
   - Required: deprecation path or explicit waiver (internal-only, same-day multi-repo)

5. **Check docs & SDK**
   - Changelog entry present?
   - SDK regenerate needed?

6. **Verdict**
   - `approve` | `approve-with-version-bump` | `request-changes` | `waiver-documented`

## Exit criteria

- [ ] Before/after sources identified
- [ ] All deltas classified
- [ ] Every break has migration note + strategy or explicit waiver
- [ ] Merge verdict with rationale
- [ ] Report written in template below

## Anti-patterns

- "It's just a rename, clients can update" without migration plan
- Approving removal of fields because "nobody should use that"
- Ignoring error body changes
- Calling a change non-breaking solely because server still compiles

## Output template

```markdown
## Breaking change review

### Scope
- Spec/code: `...`
- API maturity: shipped | beta | unreleased | internal

### Deltas
| # | delta | class | client impact | migration |
|---|-------|-------|---------------|-----------|

### Waivers
| # | reason | approver/evidence |
|---|--------|-------------------|

### Docs / SDK
- Changelog: yes/no
- SDK: yes/no / n/a

### Verdict
- **request-changes** | **approve** | **approve-with-version-bump** | **waiver-documented**
- Rationale: ...
- Required follow-ups: ...
```

## References

- `references/compatibility-rules.md`
- Follow with `deprecation-playbook` when removing after a window.
