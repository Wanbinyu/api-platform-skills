# Contributing

Thanks for helping **API Platform Skills** stay sharp and non-duplicative.

## What we accept

| Welcome | Not welcome |
|---------|-------------|
| Deeper exit criteria / better templates | Restating REST naming 101 |
| New **evolution / reliability** skills with unique names | Another `api-design` clone |
| Golden reports under `examples/sample-reports/` | AI-slop skill dumps (20 thin files) |
| Install / harness path fixes | Exploit payloads or attack runbooks |

Read [docs/NOT-ANOTHER-API-DESIGN-PACK.md](docs/NOT-ANOTHER-API-DESIGN-PACK.md) before proposing overlap with ECC / Addy / ToB.

## Skill file standard

Every `skills/<kebab-name>/SKILL.md` must have:

```markdown
---
name: kebab-name          # must match folder
description: >            # include WHEN to use + trigger phrases
  ...
---

# Title

## Overview
## Steps                    # numbered
## Exit criteria            # checkboxes — required
## Anti-patterns
## Output template          # fenced markdown report
```

Optional: `## References` pointing at `references/*.md`.

### Naming

- Lowercase kebab-case only  
- Prefer platform verbs: `breaking-change-review`, `deprecation-playbook`  
- Before opening a PR, check:

```bash
gh search code "name: your-skill-name" --filename SKILL.md --limit 15
```

If ≥5 high-quality hits for the same job, **change the angle** or drop it.

## Doc style

- Short paragraphs, scannable tables  
- Prefer checklists over essays  
- No filler (“In today’s fast-paced world…”)  
- ASCII diagrams OK; keep line length reasonable  

## Local check

```powershell
cd G:\skill\api-platform-skills   # or your clone path
.\scripts\install.ps1 -Project
# then run an agent against examples/toy-orders-api
```

## License

By contributing, you agree your changes are licensed under the repository **MIT** license.
