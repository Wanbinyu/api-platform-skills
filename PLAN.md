# 落地方案 — 你现在要做什么

仓库已在本地建好：`G:\skill\api-platform-skills`  
产品：**API Platform Skills**（契约演进垂直套装，不是又一个 api-design）

---

## 0. 今天 30 分钟（立刻）

### 0.1 本地安装并自测

```powershell
cd G:\skill\api-platform-skills
.\scripts\install.ps1 -Project
```

然后在 **Claude Code / Codex / Cursor / Grok** 任选其一，在本仓库打开对话，发送：

```text
对 examples/toy-orders-api 比较 openapi.v1.yaml 与 openapi.v2-bad.yaml，
按 breaking-change-review skill 出完整报告与 merge verdict。
```

**预期：** 报告应点出至少：

- listOrders 去掉 security  
- createOrder 201→200  
- note 变 required  
- total_cents → amount 语义破坏  
- status 取值变化  
- note / customer_email 删除  
- internal_score 过量暴露  

若 agent 没加载 skill：检查 skills 是否复制到 `.claude/skills` 或 `.agents/skills`，或手动 `@` 引用 `skills/breaking-change-review/SKILL.md`。

### 0.2 改 README 占位符

全局替换：

- GitHub：已绑定 [Wanbinyu](https://github.com/Wanbinyu)

### 0.3 初始化 Git 并推送

```powershell
cd G:\skill\api-platform-skills
git add .
git commit -m "feat: initial API Platform Skills v0.1"
git branch -M main
git remote add origin https://github.com/Wanbinyu/api-platform-skills.git
git push -u origin main
```

---

## 1. 本周交付（Week 1）— 可发布 MVP

| Day | 任务 | 完成标准 |
|-----|------|----------|
| D1 | 自测 3 个 skill：break / secure / idempotent | 各产出 1 份合格报告（可放 `examples/sample-reports/`） |
| D2 | 录 30–60s 终端/对话 GIF 或 mp4 | README 顶部可贴；对比 v1/v2-bad |
| D3 | 补 `examples/sample-reports/breaking-change-v1-vs-v2-bad.md` 金标准答案 | 别人装完能对照 |
| D4 | topics + 英文 README 打磨 slogan | Topics: `agent-skills`, `claude-code`, `openapi`, `api-design`, `codex` |
| D5 | 发版 `v0.1.0` tag；写一帖 Show HN / Reddit / 中文区 | 安装命令可复制即用 |

**不做（Week 1）：** 不要扩到 20 个 skill；不要做 Hub/Registry；不要做通用 SDLC。

---

## 2. Week 2 — 可信度

- [ ] 加 `examples/sample-reports/` 至少 3 份  
- [ ] 可选：GitHub Action 校验每个 skill 含 `## Exit criteria`  
- [ ] 在 README 写清 **与 Addy/ECC/wshobson 的差异表**（已有骨架，按反馈加长）  
- [ ] 收集 3 个真实 issue（别人的 API PR 场景）改进 anti-patterns  

---

## 3. Week 3–4 — 增长

- [ ] skills.sh / awesome-agent-skills PR（VoltAgent list）  
- [ ] 中文 README 可选 `README.zh-CN.md`  
- [ ] v0.2：OpenAPI 破坏性变更检测脚本（可选，非必须）  
- [ ] 系列包预告：`api-reliability` 已部分并入；下一包可做 **AI/MCP tool API**  

---

## 4. 仓库结构（已生成）

```text
api-platform-skills/
├── README.md                 # 安装 + 技能表 + 定位
├── PLAN.md                   # 本文件
├── AGENTS.md
├── CONTRIBUTING.md
├── LICENSE
├── commands/                 # slash 入口说明
├── skills/                   # 9 个 SKILL.md
│   ├── using-api-platform-skills/
│   ├── contract-first-openapi/
│   ├── compatibility-matrix/
│   ├── breaking-change-review/
│   ├── deprecation-playbook/
│   ├── consumer-driven-contract/
│   ├── idempotency-and-retries/
│   ├── webhook-design/
│   └── secure-api-surface/
├── references/
├── examples/toy-orders-api/  # v1 + v2-bad
└── scripts/install.{sh,ps1}
```

---

## 5. 发布检查清单

- [x] README 已绑定 Wanbinyu  

- [ ] `install.ps1 -Project` 成功  
- [ ] 9 个 skill 均有 frontmatter + Exit criteria + Output template  
- [ ] License MIT  
- [ ] 至少 1 个 demo 命令写在 README  
- [ ] 明确 **Not another REST naming tutorial**  

---

## 6. 内容冻结（v0.1 范围）

| 做 | 不做 |
|----|------|
| 契约演进 / 破坏性变更 / 弃用 | 通用 REST 命名课 |
| 幂等 + Webhook | 完整 SRE incident 套装 |
| 产品向 API 安全表面 | Trail of Bits 级审计工具链 |
| 玩具 OpenAPI 对比 | 300 个 AI 生成 skill |

---

## 7. 一句话对外叙事（发帖用）

> Most agent skills teach you how to *design* REST endpoints.  
> **API Platform Skills** teach agents how to *evolve* contracts: breaking-change review, compatibility matrices, deprecation, idempotency, webhooks, and API-surface security — with exit criteria, not prompt lore.  
> Works with Claude, Codex, Cursor, and the open Agent Skills format.
