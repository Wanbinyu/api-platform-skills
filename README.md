# API Platform Skills

**English** | [中文](README.zh-CN.md)

<p align="center">
  <strong>Stop agents from shipping silent API breaks.</strong><br/>
  <em>Design is easy. Evolution is hard.</em>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT" /></a>
  <a href="https://github.com/agentskills/agentskills"><img src="https://img.shields.io/badge/format-Agent%20Skills-111827" alt="Agent Skills" /></a>
  <a href="https://github.com/Wanbinyu/api-platform-skills/releases"><img src="https://img.shields.io/badge/version-0.1.4-0ea5e9" alt="v0.1.4" /></a>
  <img src="https://img.shields.io/badge/Claude-Codex-Cursor-7c3aed" alt="harnesses" />
</p>

---

## Start here (60 seconds)

### 1. Install (Claude Code)

```powershell
git clone https://github.com/Wanbinyu/api-platform-skills.git
cd api-platform-skills
.\scripts\install.ps1 -Claude
```

```bash
git clone https://github.com/Wanbinyu/api-platform-skills.git
cd api-platform-skills
chmod +x scripts/install.sh && ./scripts/install.sh --claude
```

Restart Claude Code. Skills land in `~/.claude/skills/`.

### 2. Try this prompt

```text
Compare examples/toy-orders-api/openapi.v1.yaml with openapi.v2-bad.yaml.
Follow breaking-change-review. Give a merge verdict.
```

**Expected:** `request-changes` / MERGE BLOCKED — auth removed, `201→200`, money unit rename, deleted fields, etc.

<p align="center">
  <img src="assets/demo-breaking-change.gif" alt="Demo: breaking-change-review blocks a bad OpenAPI upgrade" width="800" />
</p>

---

## Why you need this

| Without these skills | With these skills |
|----------------------|-------------------|
| Agent renames fields “because TypeScript compiles” | **Breaking-change review** with migration notes |
| Delete endpoint in the same PR as “deprecation” | **Deprecation playbook** with dates & dual-track |
| Double charge on client retry | **Idempotency & retries** design |
| Partner asks “what changed?” | **API changelog** ready to publish |

This is **not** another REST naming tutorial.  
Those exist (Addy / ECC / wshobson). This pack is the **evolution layer**: compatibility, breaks, deprecation, reliability, surface security.

---

## What you get (10 skills)

| When you… | Use |
|-----------|-----|
| Write OpenAPI before code | [`contract-first-openapi`](skills/contract-first-openapi/SKILL.md) |
| Ask who breaks if we change X | [`compatibility-matrix`](skills/compatibility-matrix/SKILL.md) |
| Review an API PR | [`breaking-change-review`](skills/breaking-change-review/SKILL.md) |
| Sunset v1 | [`deprecation-playbook`](skills/deprecation-playbook/SKILL.md) |
| Need consumer contracts | [`consumer-driven-contract`](skills/consumer-driven-contract/SKILL.md) |
| Design pay/order mutations | [`idempotency-and-retries`](skills/idempotency-and-retries/SKILL.md) |
| Design webhooks | [`webhook-design`](skills/webhook-design/SKILL.md) |
| Fear IDOR / oversharing | [`secure-api-surface`](skills/secure-api-surface/SKILL.md) |
| Write partner release notes | [`api-changelog`](skills/api-changelog/SKILL.md) |
| Don’t know which skill | [`using-api-platform-skills`](skills/using-api-platform-skills/SKILL.md) |

Every skill has: **triggers · steps · exit criteria · anti-patterns · report template**.

### Machine assist

```bash
python scripts/openapi_breaking_diff.py \
  examples/billing-api/openapi.v1.yaml \
  examples/billing-api/openapi.v2-risky.yaml
# exit 0 = no hard breaks; exit 2 = hard/semantic breaks
```

---

## Install options

| Method | Command / path |
|--------|----------------|
| **Claude user (recommended)** | `.\scripts\install.ps1 -Claude` → `~/.claude/skills/` |
| All harnesses | `.\scripts\install.ps1 -All` |
| This project only | `.\scripts\install.ps1 -Project` |
| Plugin | `/plugin marketplace add Wanbinyu/api-platform-skills` then install plugin |
| **One skill only** | Install the collection, then copy or link the needed `skills/<name>` directory |

macOS/Linux: `./scripts/install.sh --claude`

---

## Sister pack (tools for agents)

| Pack | For |
|------|-----|
| **This** | HTTP / OpenAPI → humans & SDKs |
| [ai-surface-skills](https://github.com/Wanbinyu/ai-surface-skills) | Tool / MCP → **agents** |

The former standalone `skill-*` repositories are archived historical links for URL compatibility. New work and new installs should use this collection.

This repository is the canonical source for the 10 skills listed above.

---

## Not this pack

| Do | Don’t |
|----|--------|
| Contract evolution & ship gates | REST plural-noun tutorials |
| Exit criteria + report templates | Prompt lore without verification |
| Defensive API product security | Red-team / reverse engineering |

Details: [docs/NOT-ANOTHER-API-DESIGN-PACK.md](docs/NOT-ANOTHER-API-DESIGN-PACK.md)

---

## Docs

| Doc | Purpose |
|-----|---------|
| [README.zh-CN.md](README.zh-CN.md) | 中文完整版 |
| [docs/CLAUDE.md](docs/CLAUDE.md) | Claude install deep-dive |
| [docs/SOCIAL.md](docs/SOCIAL.md) | Share copy |
| [examples/](examples/) | Toy OpenAPI + golden reports |

## License

MIT · [Wanbinyu](https://github.com/Wanbinyu)
