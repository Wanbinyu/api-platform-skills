# AGENTS.md — API Platform Skills

Rules for any coding agent working **in this repository** or **with these skills installed**.

## Mission

Optimize for **contract evolution and consumer safety**, not clever endpoint naming.

## Operating rules

1. **Contract-first** — public HTTP changes need a reviewable spec (OpenAPI or equivalent) before or with the code, never as a silent afterthought.
2. **No silent breaks** — removing, renaming, retyping, or re-semantizing a shipped field requires `breaking-change-review` + migration notes (or a documented waiver).
3. **Additive by default** — prefer add + deprecate over hard cutovers on shipped APIs.
4. **Retries are real** — create/payment/webhook-style mutations need an idempotency story (`idempotency-and-retries` / `webhook-design`).
5. **Authz is not optional** — public/authenticated routes get `secure-api-surface` checks (object-level + oversharing) before merge.
6. **Load less context** — use `using-api-platform-skills` to pick **one** primary skill; do not dump all nine into the prompt.
7. **Do not reinvent the shape layer** — for pure REST style questions, say so and optionally defer to external design packs; stay in the evolution layer here.

## Ship-check order

When asked “can we merge this API change?”:

1. `contract-first-openapi`  
2. `breaking-change-review`  
3. `secure-api-surface`  
4. `idempotency-and-retries` if mutations/retries  
5. `webhook-design` if outbound events  

Stop on the first hard blocker and report it clearly.

## Output quality

Prefer the skill’s **output template**. Check every **exit criteria** box (or mark blocked with why). Never claim “non-breaking” without listing discrete deltas.
