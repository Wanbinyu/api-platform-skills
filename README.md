# API Platform Skills

<p align="center">
  <strong>Design is easy. Evolution is hard.</strong>
</p>

<p align="center">
  Agent skills that make coding agents review API <em>contracts like a platform team</em><br/>
  — not invent another REST naming guide.
</p>

<p align="center">
  <a href="https://github.com/Wanbinyu/api-platform-skills/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License" /></a>
  <a href="https://github.com/agentskills/agentskills"><img src="https://img.shields.io/badge/format-Agent%20Skills-111827" alt="Agent Skills" /></a>
  <a href="https://github.com/Wanbinyu/api-platform-skills"><img src="https://img.shields.io/badge/version-0.1.0-0ea5e9" alt="v0.1.0" /></a>
  <img src="https://img.shields.io/badge/Claude-Codex-Cursor-Gemini-Copilot-7c3aed" alt="Multi harness" />
</p>

<p align="center">
  <a href="#install">Install</a> ·
  <a href="#skills">Skills</a> ·
  <a href="#30-second-demo">Demo</a> ·
  <a href="#why-this-exists">Why this</a> ·
  <a href="docs/NOT-ANOTHER-API-DESIGN-PACK.md">vs others</a> ·
  <a href="docs/SOCIAL.md">share copy</a>
</p>

<p align="center">
  <img src="assets/demo-breaking-change.gif" alt="Demo: breaking-change-review blocks a bad OpenAPI upgrade" width="800" />
</p>

<p align="center"><sub>Demo: agent loads <code>breaking-change-review</code> on a bad v1→v2 OpenAPI diff → <strong>MERGE BLOCKED</strong></sub></p>

---

## What you get

Install once. Your agent learns **nine workflows** for the hard part of HTTP APIs:

| When your agent is… | It should run… |
|---------------------|----------------|
| Adding endpoints from a blank page | **Contract-first OpenAPI** gates |
| Changing a field on a live API | **Breaking-change review** + **compat matrix** |
| Removing v1 after v2 ships | **Deprecation playbook** |
| Designing `POST /payments` | **Idempotency & retries** |
| Pushing events to customers | **Webhook design** |
| Reviewing public routes for abuse | **Secure API surface** (product APIs) |

Each skill ships with:

- clear **triggers** (when to load)
- numbered **steps**
- hard **exit criteria** (done ≠ “sounds good”)
- fixed **report templates**
- explicit **anti-patterns** agents usually invent

---

## Why this exists

Most skill packs stop at **shape**:

> plural nouns · status codes · pagination · “use OpenAPI”

That’s useful — and already covered well by community packs  
([addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) `api-and-interface-design`, ECC `api-design`, wshobson backend skills, etc.).

**This pack starts where those stop: the platform layer.**

```text
┌─────────────────────────────────────────────────────────┐
│  Shape layer (use other packs)                          │
│  resource design · HTTP semantics · style guides        │
└───────────────────────────┬─────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│  Evolution layer  ←  api-platform-skills                │
│  compatibility · breaking changes · deprecation         │
│  CDC · idempotency · webhooks · API surface security    │
└─────────────────────────────────────────────────────────┘
```

They compose. They don’t compete. Details: **[docs/NOT-ANOTHER-API-DESIGN-PACK.md](docs/NOT-ANOTHER-API-DESIGN-PACK.md)**.

---

## Install

### Windows (PowerShell)

```powershell
git clone https://github.com/Wanbinyu/api-platform-skills.git
cd api-platform-skills
.\scripts\install.ps1            # user-level (~/.claude, ~/.agents, …)
# .\scripts\install.ps1 -Project # this repo only
```

### macOS / Linux

```bash
git clone https://github.com/Wanbinyu/api-platform-skills.git
cd api-platform-skills
chmod +x scripts/install.sh
./scripts/install.sh             # user-level
# ./scripts/install.sh --project # this repo only
```

### Where skills land

| Agent | Directory |
|-------|-----------|
| Claude Code | `~/.claude/skills/` or `.claude/skills/` |
| Codex / open standard | `~/.agents/skills/` or `.agents/skills/` |
| Cursor | `~/.cursor/skills/` or `.cursor/skills/` |
| GitHub Copilot | `.github/skills/` |

Keep folder names unchanged. Each skill is `skills/<name>/SKILL.md`.

---

## Skills

### Lifecycle map

```text
  define contract          ship change              run reliably
 ───────────────     ─────────────────────     ──────────────────
 contract-first   →  compat-matrix             idempotency
                     breaking-change-review    webhook-design
                     deprecation-playbook      secure-api-surface
                     consumer-driven-contract
                              │
                              ▼
                     /api-ship-check  (gate them in order)
```

### Catalog

| # | Skill | One-line job |
|---|--------|--------------|
| 0 | [`using-api-platform-skills`](skills/using-api-platform-skills/SKILL.md) | Router — pick the smallest right skill |
| 1 | [`contract-first-openapi`](skills/contract-first-openapi/SKILL.md) | Spec + review gate **before** handlers |
| 2 | [`compatibility-matrix`](skills/compatibility-matrix/SKILL.md) | Delta × consumer blast radius |
| 3 | [`breaking-change-review`](skills/breaking-change-review/SKILL.md) | PR verdict + migration notes |
| 4 | [`deprecation-playbook`](skills/deprecation-playbook/SKILL.md) | Announce → dual-track → sunset |
| 5 | [`consumer-driven-contract`](skills/consumer-driven-contract/SKILL.md) | Consumer expectations → CI gates |
| 6 | [`idempotency-and-retries`](skills/idempotency-and-retries/SKILL.md) | Keys, storage, safe retries |
| 7 | [`webhook-design`](skills/webhook-design/SKILL.md) | Sign, replay, at-least-once |
| 8 | [`secure-api-surface`](skills/secure-api-surface/SKILL.md) | BOLA/BFLA, oversharing, mass-assignment |

### Natural language triggers

You don’t need slash commands. Say things like:

- *“Review this PR for breaking API changes.”*
- *“Build a deprecation plan for `/v1/orders`.”*
- *“Make `POST /payments` idempotent under client retries.”*
- *“Ship-check this OpenAPI diff before merge.”*

Optional command stubs live in [`commands/`](commands/) for harnesses that support them (`/api-break`, `/api-ship-check`, …).

---

## 30-second demo

<p align="center">
  <img src="assets/demo-poster.png" alt="MERGE BLOCKED verdict poster" width="720" />
</p>

Repo includes a **deliberately bad** upgrade:

| File | Role |
|------|------|
| [`examples/toy-orders-api/openapi.v1.yaml`](examples/toy-orders-api/openapi.v1.yaml) | Shipped baseline |
| [`examples/toy-orders-api/openapi.v2-bad.yaml`](examples/toy-orders-api/openapi.v2-bad.yaml) | Silent breaks on purpose |
| [`examples/sample-reports/breaking-change-v1-vs-v2-bad.md`](examples/sample-reports/breaking-change-v1-vs-v2-bad.md) | Golden report |
| [`assets/demo-breaking-change.gif`](assets/demo-breaking-change.gif) | Animated walkthrough |

After install, ask your agent:

```text
Compare examples/toy-orders-api/openapi.v1.yaml with openapi.v2-bad.yaml.
Follow skills/breaking-change-review/SKILL.md exactly.
Give a merge verdict. Diff against the golden sample report.
```

A good run flags auth removal, `201→200`, required-field tighten, cents→dollars semantic break, status enum rewrite, deleted fields, and oversharing `internal_score` — then **request-changes**.

### Share / star

Ready-to-post copy (EN + 中文): **[docs/SOCIAL.md](docs/SOCIAL.md)**

---

## Quality bar (how we avoid “prompt lore”)

Every skill in this repo must include:

1. YAML `name` + trigger-rich `description`
2. Numbered workflow
3. **Exit criteria** (checkboxes)
4. Anti-patterns
5. Copy-paste **output template**

If a skill can’t fail a checklist, it doesn’t ship. See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Roadmap

| Version | Focus |
|---------|--------|
| **0.1** | Nine skills · toy OpenAPI · installers · golden report |
| **0.2** | CI check for skill structure · more sample reports |
| **0.3** | Lightweight eval fixtures (agent with/without skill) |
| **0.4** | Optional gRPC / GraphQL evolution add-ons |

---

## Contributing · License · Author

- **Contribute:** [CONTRIBUTING.md](CONTRIBUTING.md)
- **License:** [MIT](LICENSE) — free to use, fork, and ship in commercial products
- **Author:** [Wanbinyu](https://github.com/Wanbinyu)

```text
MIT · open source · https://github.com/Wanbinyu/api-platform-skills
```
