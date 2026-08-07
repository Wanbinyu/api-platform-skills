#!/usr/bin/env python3
"""Validate the skill collection, local links, commands, and plugin metadata."""
from __future__ import annotations

import json
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
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")


def read_utf8(path: Path) -> str:
    raw = path.read_bytes()
    if b"\xef\xbf\xbd" in raw:
        raise ValueError("contains U+FFFD replacement bytes")
    text = raw.decode("utf-8")
    if "\ufffd" in text:
        raise ValueError("contains U+FFFD replacement character")
    return text


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Parse the small YAML subset used by skill and command frontmatter."""
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing YAML frontmatter")
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), -1)
    if end < 0:
        raise ValueError("unterminated YAML frontmatter")

    metadata: dict[str, str] = {}
    key: str | None = None
    chunks: list[str] = []

    def flush() -> None:
        if key is not None:
            metadata[key] = " ".join(chunks).strip()

    for line in "".join(lines[1:end]).splitlines():
        if not line.strip():
            continue
        if line[0].isspace():
            if key is None:
                raise ValueError("indented frontmatter without a key")
            chunks.append(line.strip())
            continue
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not match:
            raise ValueError(f"invalid frontmatter line: {line!r}")
        flush()
        key = match.group(1)
        value = match.group(2).strip()
        chunks = [] if value in {">", "|"} else [value]
    flush()
    return metadata, "".join(lines[end + 1 :])


def local_link_errors(path: Path, text: str) -> list[str]:
    errors: list[str] = []
    root = ROOT.resolve()
    for raw_target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
        target = raw_target.split("#", 1)[0].strip().strip("<>")
        if not target or target.startswith(("#", "/")) or "://" in target:
            continue
        resolved = (path.parent / target).resolve()
        try:
            resolved.relative_to(root)
        except ValueError:
            errors.append(f"link escapes repository: {raw_target}")
            continue
        if not resolved.exists():
            errors.append(f"missing local link target: {raw_target}")
    return errors


def validate_skill(path: Path) -> list[str]:
    try:
        text = read_utf8(path)
        metadata, body = parse_frontmatter(text)
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        return [str(exc)]

    errors: list[str] = []
    folder = path.parent.name
    name = metadata.get("name", "").strip()
    description = metadata.get("description", "").strip()
    if not SLUG.fullmatch(folder):
        errors.append("folder is not a lowercase kebab-case slug")
    if name != folder:
        errors.append(f"frontmatter name={name!r} != folder {folder!r}")
    if not description:
        errors.append("missing description")
    elif len(description) < 40:
        errors.append("description too short for reliable triggering")
    for section in REQUIRED_SECTIONS:
        if section not in body:
            errors.append(f"missing section {section}")
    if not re.search(r"(?:-|\*) \[ \]", body):
        errors.append("exit criteria should include checkbox items")
    if "```" not in body:
        errors.append("missing fenced output template")
    errors.extend(local_link_errors(path, body))
    return errors


def validate_commands() -> list[str]:
    errors: list[str] = []
    command_dir = ROOT / "commands"
    if not command_dir.is_dir():
        return ["commands/: missing"]
    for path in sorted(command_dir.glob("*.md")):
        try:
            metadata, _ = parse_frontmatter(read_utf8(path))
        except (OSError, UnicodeDecodeError, ValueError) as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")
            continue
        if not metadata.get("description", "").strip():
            errors.append(f"{path.relative_to(ROOT)}: missing description")
    return errors


def validate_readme(skill_names: set[str], version: str | None) -> list[str]:
    errors: list[str] = []
    for filename in ("README.md", "README.zh-CN.md"):
        path = ROOT / filename
        try:
            text = read_utf8(path)
        except (OSError, UnicodeDecodeError, ValueError) as exc:
            errors.append(f"{filename}: {exc}")
            continue
        if filename == "README.md":
            errors.extend(f"README.md: {error}" for error in local_link_errors(path, text))

    readme = ROOT / "README.md"
    if not readme.exists():
        return errors + ["README.md: missing"]
    try:
        text = read_utf8(readme)
    except (OSError, UnicodeDecodeError, ValueError):
        return errors

    linked = set(re.findall(r"\]\(skills/([^/]+)/SKILL\.md\)", text))
    for name in sorted(skill_names - linked):
        errors.append(f"README.md: missing skill link for {name}")
    for name in sorted(linked - skill_names):
        errors.append(f"README.md: link points to unknown skill {name}")

    badge = re.search(r"version-(\d+\.\d+\.\d+)-", text)
    if version and badge and badge.group(1) != version:
        errors.append(f"README.md: version badge {badge.group(1)} != plugin version {version}")
    return errors


def validate_plugin_metadata() -> tuple[list[str], str | None]:
    errors: list[str] = []
    plugin_path = ROOT / ".claude-plugin" / "plugin.json"
    marketplace_path = ROOT / ".claude-plugin" / "marketplace.json"
    try:
        plugin = json.loads(read_utf8(plugin_path))
        marketplace = json.loads(read_utf8(marketplace_path))
    except (OSError, UnicodeDecodeError, ValueError, json.JSONDecodeError) as exc:
        return [f"plugin metadata: {exc}"], None

    name = plugin.get("name")
    version = plugin.get("version")
    version_value = version if isinstance(version, str) and SEMVER.fullmatch(version) else None
    if name != ROOT.name:
        errors.append(f"plugin.json name={name!r} != repository {ROOT.name!r}")
    if version_value is None:
        errors.append("plugin.json version must be semantic version X.Y.Z")
    if marketplace.get("name") != name:
        errors.append("marketplace.json name does not match plugin.json")

    metadata = marketplace.get("metadata")
    if not isinstance(metadata, dict):
        errors.append("marketplace.json metadata must be an object")
        metadata = {}
    if metadata.get("version") != version:
        errors.append("marketplace metadata version does not match plugin.json")

    entries = marketplace.get("plugins")
    if not isinstance(entries, list) or len(entries) != 1:
        errors.append("marketplace.json must contain exactly one plugin entry")
    elif not isinstance(entries[0], dict):
        errors.append("marketplace plugin entry must be an object")
    else:
        entry = entries[0]
        if entry.get("name") != name or entry.get("source") != "./":
            errors.append("marketplace plugin entry must point to ./ with the package name")
        if entry.get("version") != version:
            errors.append("marketplace plugin entry version does not match plugin.json")
    return errors, version_value


def main() -> int:
    if not SKILLS.is_dir():
        print(f"FAIL: missing {SKILLS}")
        return 1
    skill_dirs = sorted(path for path in SKILLS.iterdir() if path.is_dir())
    if not skill_dirs:
        print("FAIL: no skills found")
        return 1

    failed = 0
    for directory in skill_dirs:
        skill_path = directory / "SKILL.md"
        if not skill_path.is_file():
            print(f"FAIL {directory.name}: missing SKILL.md")
            failed += 1
            continue
        errors = validate_skill(skill_path)
        if errors:
            print(f"FAIL {directory.name}:")
            for error in errors:
                print(f"  - {error}")
            failed += 1
        else:
            print(f"OK   {directory.name}")

    repo_errors, version = validate_plugin_metadata()
    repo_errors.extend(validate_readme({directory.name for directory in skill_dirs}, version))
    repo_errors.extend(validate_commands())
    if repo_errors:
        print("FAIL repository metadata/index:")
        for error in repo_errors:
            print(f"  - {error}")
        failed += len(repo_errors)

    print()
    if failed:
        print(f"{failed} validation error(s)")
        return 1
    print(f"All {len(skill_dirs)} skills and repository metadata are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
