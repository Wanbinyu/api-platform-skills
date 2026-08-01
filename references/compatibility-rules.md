# Compatibility rules (quick reference)

Use with `breaking-change-review` and `compatibility-matrix`.

## Additive (usually safe)

- New endpoint
- New optional response property
- New optional request property (server defaults if absent)
- New enum **value** if clients tolerate unknown enums
- New error code for new failure modes (document it)

## Breaking (usually unsafe for shipped APIs)

- Remove/rename path, method, or property
- Change property type or make optional field required
- Remove enum value
- Change auth requirements incompatibly
- Change status codes clients depend on
- Semantic change with same schema
- Tighten validation rejecting old clients

## Gray areas (flag explicitly)

- Reordering JSON properties (almost always OK)
- Changing undocumented behavior
- Default page size changes
- Adding stricter rate limits (product/comms issue)
- Error message text changes (if clients parse text — discourage parsing)

## Decision heuristic

1. Is the API shipped to any consumer outside this PR's deploy unit?  
   - No → mark unreleased; still document.  
   - Yes → apply breaking rules strictly.
2. Can we add instead of change? Prefer add + deprecate.
3. If we must break → new version + migration note + timeline.
