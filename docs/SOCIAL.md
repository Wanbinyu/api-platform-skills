# Social / Star copy

Short posts you can paste. Link always:

**https://github.com/Wanbinyu/api-platform-skills**

---

## English — short (Twitter/X, HN comment)

```text
Most agent skills teach REST *design*.

API Platform Skills teach contract *evolution*:
breaking-change review · compat matrix · deprecation ·
idempotency · webhooks · API surface security.

Exit criteria, not prompt lore. Claude / Codex / Cursor.

https://github.com/Wanbinyu/api-platform-skills
```

## English — Show HN

**Title:** Show HN: Agent skills for API contract evolution (not another REST guide)

**Body:**

```text
I kept seeing coding agents rename fields and call it a “small refactor.”

So I open-sourced a focused Agent Skills pack for the platform layer:

- breaking-change review with merge verdicts
- consumer blast-radius matrix
- deprecation playbooks
- idempotency + signed webhooks
- product API surface security (BOLA/oversharing)

It deliberately does *not* redo REST naming tutorials (those already exist).
It composes with them.

Demo fixture ships with a bad OpenAPI upgrade that should fail review.

MIT · works with Claude Code, Codex, Cursor, Copilot.

https://github.com/Wanbinyu/api-platform-skills
```

## English — Reddit (r/claudeai, r/LocalLLaMA, r/programming)

**Title:** Agent skills pack for API *evolution* (breaking changes, deprecation, idempotency)

```text
If your agent happily deletes response fields “because TypeScript still compiles,” this is for you.

**API Platform Skills** — 9 SKILL.md workflows for:

1. Contract-first OpenAPI gates
2. Compatibility matrices
3. Breaking-change PR reviews
4. Deprecation timelines
5. Consumer-driven contracts
6. Idempotency keys / retries
7. Signed webhooks
8. Secure API surface (product-side)
9. A router skill for ship-check

Explicit non-goals: another `api-design` clone, full SDLC packs, red-team exploits.

Install: clone + `install.ps1` / `install.sh`

https://github.com/Wanbinyu/api-platform-skills
```

---

## 中文 — 短帖（即刻 / 朋友圈 / 微博）

```text
大多数 Agent Skill 教「怎么设计 REST」。

这个开源包教「契约怎么演进、怎么别炸调用方」：
破坏性变更审查 · 兼容矩阵 · 弃用计划 · 幂等 · Webhook · API 表面安全。

带 exit criteria 和报告模板，不是一堆 prompt 水文。
兼容 Claude / Codex / Cursor。

https://github.com/Wanbinyu/api-platform-skills
```

## 中文 — V2EX / 掘金风格

**标题：** 开源：给 Coding Agent 用的 API 平台 Skills（契约演进，不是又一个 api-design）

```text
背景：用 Claude/Codex 改接口时，模型很会「起资源名」，但经常：
- 默默改字段类型
- 把 201 改成 200
- 没有弃用窗口就删字段
- POST 重试直接双写订单

所以做了 **API Platform Skills**（MIT）：

- 9 个垂直 SKILL.md（破坏性变更 / 兼容矩阵 / 弃用 / CDC / 幂等 / Webhook / API 安全表面…）
- 故意做坏的 OpenAPI 玩具 diff + 金标准报告
- 一键装到 Claude Code / Codex / Cursor

刻意不做：REST 命名课、完整 SDLC、红队利用（避免和现有高星包撞车）。

仓库：https://github.com/Wanbinyu/api-platform-skills
欢迎 star / issue / PR。
```

## 中文 — 一句话简介（GitHub About 备用）

```text
开源 Agent Skills：API 契约演进（破坏性变更、弃用、幂等、Webhook），不是又一个 REST 命名教程。
```

---

## Star 话术（评论区回复）

```text
Thanks! If you try the toy OpenAPI under examples/toy-orders-api with breaking-change-review, I’d love feedback on false positives/negatives.
```

```text
谢谢！装完后可以对 examples/toy-orders-api 跑 breaking-change-review，欢迎反馈漏报/误报。
```
