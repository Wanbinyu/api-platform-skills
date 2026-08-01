# Contributing

## Skill quality bar

Every skill under `skills/<name>/SKILL.md` **must** include:

1. YAML frontmatter: `name`, `description` (with clear **when to use** triggers)
2. Overview (1 short paragraph)
3. Numbered workflow steps
4. **Exit criteria** (checkbox list — agent is not done until all pass)
5. Anti-patterns (what agents commonly get wrong)
6. Output template (fixed Markdown report structure)
7. Optional `references/` links for progressive disclosure

## Naming

- Directory and `name:` field: lowercase kebab-case, match exactly
- Avoid names already flooded on GitHub (`api-design`, `security-review` alone)
- Prefer platform verbs: `breaking-change-review`, `deprecation-playbook`

## Before PR

```bash
# Name collision check (optional, needs gh)
gh search code "name: your-skill-name" --filename SKILL.md --limit 10
```

- Do not add skills that only restate REST resource naming (out of scope)
- Prefer depth + exit criteria over length
- Update README skill table if adding/removing skills

## Local install for testing

```bash
./scripts/install.sh --project
# then invoke the skill in your coding agent inside this repo
```
