# AGENTS.md — API Platform Skills

When working in a repository that uses **api-platform-skills**:

1. Prefer **contract-first**: OpenAPI (or equivalent) changes land before or with implementation, never after silently.
2. Never remove, rename, or retype a shipped public field without running **breaking-change-review** and producing a migration note.
3. Default to **additive evolution**. Breaking changes require version strategy + deprecation window unless the API is explicitly unreleased/internal-only.
4. Mutations that clients may retry (create payment, place order, webhook delivery) must address **idempotency**.
5. Public HTTP APIs must pass **secure-api-surface** checks for object-level auth and excess data exposure before merge.
6. Load only the skill(s) needed for the task (see `using-api-platform-skills`). Do not dump all skills into context.
