---
name: api-changelog
description: >
  Write a consumer-facing API changelog from OpenAPI or code diffs. Use when shipping
  API changes, drafting release notes for partners/SDKs, summarizing breaks vs additive
  changes, or when the user says "/api-changelog", "API changelog", "release notes for
  the API", or in Chinese "接口变更日志", "API 发布说明", "给调用方写 changelog",
  "版本更新说明". Prefer pairing with breaking-change-review deltas. Not a git commit
  message skill and not a marketing blog post.
---

# API Changelog

> Callers should know what broke, what is new, and what to do next - in one page.

## Overview

Turn structural API deltas into a **consumer-facing changelog**: clear sections for
breaking / additive / deprecations, migration steps, and rollout timing. Write for
SDK authors and integrators, not for internal eng ego.

## When to run

- After `breaking-change-review` or `openapi_breaking_diff.py`
- Before tagging an API release
- When partners ask "what changed in vX?"

## Steps

1. **Collect inputs**
   - Before/after OpenAPI (or DTO diff)
   - Optional: tool output from `python scripts/openapi_breaking_diff.py old.yaml new.yaml`
   - API maturity: shipped | beta | unreleased | internal
   - Target audience: public partners | first-party only | internal services

2. **Bucket every delta**

   | Bucket | Examples |
   |--------|----------|
   | Breaking | Removed fields, type changes, required adds, auth changes, status renames |
   | Semantic | Same shape, new meaning (units, status meaning) |
   | Additive | New endpoints, optional fields, new enum values |
   | Deprecations | Still works; sunset date announced |
   | Security / authz | Auth added/removed, oversharing fixes (call out carefully) |
   | Internal-only | Not for public changelog (omit or label internal) |

3. **Write migration for each breaking/semantic item**
   - What clients must change
   - Temporary dual-support if any
   - Link to deprecation plan if sunsetting

4. **Draft changelog** using the output template (Keep a Changelog style, API-flavored).

5. **Quality pass**
   - No jargon without a path/field name
   - Every break has a "What to do" line
   - Dates/versions explicit
   - Do not claim non-breaking if review said otherwise

6. **Optional artifacts**
   - Short email/Slack blurb (5 lines)
   - SDK upgrade checklist bullets

## Exit criteria

- [ ] Inputs and audience stated
- [ ] All known deltas bucketed (or listed as unknown)
- [ ] Every breaking/semantic item has migration guidance
- [ ] Changelog uses the template structure
- [ ] Version / date / contact filled or marked TBD
- [ ] Explicit: safe to publish to consumers? yes/no + why

## Anti-patterns

- "Various bug fixes and improvements" with no field names
- Hiding breaks under "Improvements"
- Mixing internal refactors with public contract changes
- Copy-pasting OpenAPI YAML into the changelog
- Writing only for engineers who already merged the PR

## Output template

```markdown
# API Changelog

## [X.Y.Z] - YYYY-MM-DD

### Summary
- One paragraph: what shipped and who is affected.
- Maturity: shipped | beta | internal
- Compatibility: additive-only | contains breaking changes | deprecations only

### Breaking changes
| Change | Impact | What to do |
|--------|--------|------------|
| ... | ... | ... |

### Semantic changes
| Change | Old meaning | New meaning | What to do |
|--------|-------------|-------------|------------|

### Deprecated (still work)
| Item | Replacement | Sunset |
|------|-------------|--------|

### Added
- ...

### Fixed (contract-visible only)
- ...

### Security
- ...

### Migration checklist
- [ ] ...

### Support
- Docs: ...
- Contact: ...

### Publish?
- [ ] Yes - consumer-ready
- [ ] No - blockers: ...
```

### Short blurb template

```markdown
**API [X.Y.Z]** (YYYY-MM-DD)
- Breaks: ...
- Adds: ...
- Action: ...
Details: <changelog link>
```

## Tooling assist

```bash
python scripts/openapi_breaking_diff.py old.yaml new.yaml
```

Use the table as draft input; rephrase for humans; never paste raw tool output as the final changelog without editing.

## References

- Pair with: `breaking-change-review`, `deprecation-playbook`, `compatibility-matrix`
- Fixtures: `examples/billing-api/`, `examples/sample-reports/`
