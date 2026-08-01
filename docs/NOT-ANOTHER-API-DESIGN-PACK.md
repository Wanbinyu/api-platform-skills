# Not another API design pack

This document exists so humans (and agents) can see **what we deliberately do not copy**.

## Positioning in one diagram

```text
                    CONTENT FOCUS
                    ─────────────
  shape / style                 evolution / platform
  (naming, verbs,               (compat, deprecation,
   status codes)                 idempotency, webhooks)
        │                                  │
        ▼                                  ▼
  ┌─────────────┐                   ┌──────────────────┐
  │ ECC api-    │                   │ THIS REPO        │
  │ design      │                   │ api-platform-    │
  │ Addy api-   │  ── compose ──►   │ skills           │
  │ and-interface│                  └──────────────────┘
  │ wshobson    │
  │ api-design- │
  │ principles  │
  └─────────────┘

  security research / exploits     product API surface review
  (Trail of Bits skills, …)   ≠   (secure-api-surface here)
```

## Side-by-side

| Topic | Covered heavily elsewhere | Covered here |
|-------|---------------------------|--------------|
| REST resource naming, plural nouns | ECC, clones of `api-design` | **No** — out of scope |
| HTTP method / status style guides | Addy, wshobson, many forks | Only as needed for **breaks** |
| Contract-first + review **gate** | Partial in many packs | **Yes** — exit criteria + ready/blocked |
| Field-level **blast radius** matrix | Rare | **Yes** — first-class skill |
| PR **breaking-change verdict** | Release-note labels only | **Yes** — catalog + migration required |
| Dated **deprecation** (headers, sunset) | Sparse | **Yes** |
| Consumer-driven contracts | Scattered testing skills | **Yes** — process + CI ownership |
| **Idempotency-Key** design | Almost never a dedicated skill | **Yes** |
| Signed **webhooks** + retries | Almost never a pack focus | **Yes** |
| OWASP essay / AppSec one-shot | Addy `security-and-hardening` | Only **API object/function authz & exposure** |
| Binary audit / reverse eng | Trail of Bits | **No** |
| Full SDLC `/spec /plan /build` | Superpowers, Addy lifecycle | **No** |

## Name collision policy

We **avoid** skill directory names that are already flooded on GitHub:

| Avoided name | Why | Our name |
|--------------|-----|----------|
| `api-design` | Dozens of clones | `contract-first-openapi` |
| `security-review` alone | Generic noise | `secure-api-surface` |
| `incident-response` | Already in mega-packs | not in this repo |

## How to use with other packs

```text
1. Optional: install a general design skill pack for style.
2. Install this pack for evolution / reliability / API surface.
3. On API PRs, prefer /api-ship-check from this pack.
```

## Contribution rule

PRs that only restate “use plural nouns / return 404 for missing resources” will be closed as **duplicate of the shape layer**. Bring evolution, reliability, or surface-security depth — or golden reports that prove the skill changes agent output.
