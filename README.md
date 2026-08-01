# API Platform Skills

**Design is easy. Evolution is hard.**

Production-grade **Agent Skills** for API contract design, compatibility, breaking-change review, deprecation, reliability (idempotency / webhooks), and API-surface security.

Works with **Claude Code**, **Codex**, **Cursor**, **Gemini CLI**, **GitHub Copilot**, and any harness that supports the [Agent Skills](https://github.com/agentskills/agentskills) open format (`SKILL.md`).

> **Not another REST naming tutorial.**  
> Packs like [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) (`api-and-interface-design`) and ECC `api-design` teach *how to shape endpoints*.  
> **This pack** teaches *how contracts evolve without breaking consumers* — versioning, compatibility matrices, deprecation, dual-write, idempotency, webhooks, and OWASP API surface checks.

---

## Install

### One-liner (recommended)

```bash
# Linux / macOS / Git Bash
curl -fsSL https://raw.githubusercontent.com/Wanbinyu/api-platform-skills/main/scripts/install.sh | bash

# Or clone then install
git clone https://github.com/Wanbinyu/api-platform-skills.git
cd api-platform-skills
./scripts/install.sh          # user-level
./scripts/install.sh --project   # current repo only
```

### Windows (PowerShell)

```powershell
git clone https://github.com/Wanbinyu/api-platform-skills.git
cd api-platform-skills
.\scripts\install.ps1
# or project-local:
.\scripts\install.ps1 -Project
```

### Manual copy

| Harness | Copy `skills/*` into |
|---------|----------------------|
| Claude Code | `~/.claude/skills/` or `.claude/skills/` |
| Codex / Agent Skills standard | `~/.agents/skills/` or `.agents/skills/` |
| Cursor | `.cursor/skills/` or `~/.cursor/skills/` |
| GitHub Copilot | `.github/skills/` |
| Gemini CLI | follow your CLI skills path (often `~/.gemini/skills/`) |

Each skill is a folder containing `SKILL.md`. Keep folder names as-is.

### Compose with general packs (optional)

```text
general design principles  →  addyosmani api-and-interface-design / ECC api-design
contract evolution         →  this pack (api-platform-skills)
```

---

## Skills (v0.1)

| Skill | When to use |
|-------|-------------|
| [`using-api-platform-skills`](skills/using-api-platform-skills/SKILL.md) | Meta-router: pick the right skill |
| [`contract-first-openapi`](skills/contract-first-openapi/SKILL.md) | Spec before code; OpenAPI review gates |
| [`compatibility-matrix`](skills/compatibility-matrix/SKILL.md) | Who breaks if this field/endpoint changes? |
| [`breaking-change-review`](skills/breaking-change-review/SKILL.md) | PR-level breaking change audit + migration notes |
| [`deprecation-playbook`](skills/deprecation-playbook/SKILL.md) | Sunset, dual-track, consumer communication |
| [`consumer-driven-contract`](skills/consumer-driven-contract/SKILL.md) | Consumer expectations & contract tests |
| [`idempotency-and-retries`](skills/idempotency-and-retries/SKILL.md) | Keys, storage, retry/timeout design |
| [`webhook-design`](skills/webhook-design/SKILL.md) | Signatures, replay, at-least-once delivery |
| [`secure-api-surface`](skills/secure-api-surface/SKILL.md) | OWASP API Top 10 style surface review (product APIs) |

### Slash-style entry points

If your harness supports custom commands, see [`commands/`](commands/):

| Command | Activates |
|---------|-----------|
| `/api-contract` | contract-first-openapi |
| `/api-compat` | compatibility-matrix |
| `/api-break` | breaking-change-review |
| `/api-deprecate` | deprecation-playbook |
| `/api-cdc` | consumer-driven-contract |
| `/api-idempotent` | idempotency-and-retries |
| `/api-webhook` | webhook-design |
| `/api-secure` | secure-api-surface |
| `/api-ship-check` | full pre-merge API platform gate |

Or just say naturally: *“review this PR for breaking API changes”*, *“design idempotent create-order”*, *“deprecation plan for v1 users”*.

---

## Quick demo (toy API)

```bash
# Open the intentionally messy contract
ls examples/toy-orders-api/

# Ask your agent (after install):
# "Run breaking-change-review on examples/toy-orders-api comparing openapi.v1.yaml and openapi.v2-bad.yaml"
```

Expected: agent flags removed fields, status renames, auth weakening, missing migration notes.

---

## What this is / is not

| Is | Is not |
|----|--------|
| Contract lifecycle & platform discipline | Another REST plural-noun tutorial |
| Exit criteria + report templates | Prompt lore without verification |
| Multi-harness `SKILL.md` | Claude-only lock-in |
| Defensive API product security | Red-team / reverse engineering (see Trail of Bits) |

---

## Roadmap

- [x] v0.1 — 9 skills + toy example + install scripts  
- [ ] v0.2 — OpenAPI lint script hooks + CI sample workflow  
- [ ] v0.3 — Skill eval fixtures (before/after agent quality)  
- [ ] v0.4 — gRPC / GraphQL evolution add-on skills  

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). New skills must include: triggers, steps, **exit criteria**, anti-patterns, output template.

## License

MIT — see [LICENSE](LICENSE).

## Maintainers

- [Wanbinyu](https://github.com/Wanbinyu)
