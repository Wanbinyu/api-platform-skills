# Compatibility rules

Quick reference for `breaking-change-review` and `compatibility-matrix`.

## Usually safe (additive)

| Change | Notes |
|--------|--------|
| New endpoint | — |
| New optional response property | — |
| New optional request property | Server must default if absent |
| New enum **value** | Clients should tolerate unknowns |
| New error code for a new failure | Document it |

## Usually breaking (shipped APIs)

| Change | Notes |
|--------|--------|
| Remove/rename path, method, property | — |
| Type change / optional → required | — |
| Remove enum value | — |
| Incompatible auth change | — |
| Status codes clients branch on | — |
| Semantic change, same schema | e.g. unit change |
| Tighter validation | Rejects old clients |
| Cursor / pagination format change | — |

## Gray area (always flag)

- Changing undocumented behavior  
- Default page size that truncates results  
- Stricter rate limits (product/comms)  
- Error **message text** if clients parse strings (discourage parsing)

## Heuristic

1. Consumed outside this deploy unit? → apply breaking rules strictly.  
2. Can we **add** instead of change? Prefer add + deprecate.  
3. Must break? → new version + migration + timeline.
