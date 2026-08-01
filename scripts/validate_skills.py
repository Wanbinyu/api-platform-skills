#!/usr/bin/env python3
"""Validate skills/*/SKILL.md structure for API Platform Skills."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"

REQUIRED_SECTIONS = [
    "## Overview",
    "## Steps",
    "## Exit criteria",
    "## Anti-patterns",
    "## Output template",
]


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---"):
        raise ValueError("missing YAML frontmatter")
    end = text.find("\n---", 3)
    if end < 0:
        raise ValueError("unterminated frontmatter")
    raw = text[3:end].strip()
    body = text[end + 4 :]
    meta: dict[str, str] = {}
    key = None
    chunks: list[str] = []
    for line in raw.splitlines():
        if re.match(r"^[a-zA-Z0-9_-]+:\s*", line) and not line.startswith(" "):
            if key is not None:
                meta[key] = "\n".join(chunks).strip()
            key, _, rest = line.partition(":")
            key = key.strip()
            rest = rest.strip()
            if rest == ">" or rest == "|":
                chunks = []
            else:
                chunks = [rest]
        else:
            chunks.append(line.strip())
    if key is not None:
        meta[key] = "\n".join(chunks).strip()
    return meta, body


def validate_skill(path: Path) -> list[str]:
    errors: list[str] = []
    raw = path.read_bytes()
    if b"\xef\xbf\xbd" in raw:
        errors.append("contains U+FFFD replacement bytes (bad encoding)")
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as e:
        return [f"not valid UTF-8: {e}"]

    if "\ufffd" in text:
        errors.append("contains U+FFFD replacement character")

    try:
        meta, body = parse_frontmatter(text)
    except ValueError as e:
        return [str(e)]

    name = meta.get("name", "").strip()
    folder = path.parent.name
    if name != folder:
        errors.append(f"frontmatter name={name!r} != folder {folder!r}")
    if not meta.get("description"):
        errors.append("missing description")
    elif len(meta["description"]) < 40:
        errors.append("description too short for reliable triggering")

    for section in REQUIRED_SECTIONS:
        if section not in body:
            errors.append(f"missing section {section}")

    if "- [ ]" not in body and "* [ ]" not in body:
        errors.append("exit criteria should include checkbox items")

    if "```markdown" not in body and "```" not in body:
        errors.append("missing fenced output template")

    return errors


def main() -> int:
    skill_dirs = sorted(p for p in SKILLS.iterdir() if p.is_dir())
    if not skill_dirs:
        print("No skills found", file=sys.stderr)
        return 1

    failed = 0
    for d in skill_dirs:
        skill = d / "SKILL.md"
        if not skill.exists():
            print(f"FAIL {d.name}: missing SKILL.md")
            failed += 1
            continue
        errs = validate_skill(skill)
        if errs:
            print(f"FAIL {d.name}:")
            for e in errs:
                print(f"  - {e}")
            failed += 1
        else:
            print(f"OK   {d.name}")

    print()
    if failed:
        print(f"{failed} skill(s) failed")
        return 1
    print(f"All {len(skill_dirs)} skills valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
