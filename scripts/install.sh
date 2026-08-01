#!/usr/bin/env bash
# Install api-platform-skills for Claude Code and other agents.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$ROOT/skills"
PROJECT=0
CLAUDE=0
ALL=0

for arg in "$@"; do
  case "$arg" in
    --project|-p) PROJECT=1 ;;
    --claude|-c) CLAUDE=1 ;;
    --all|-a) ALL=1 ;;
    --help|-h)
      echo "Usage: $0 [--claude] [--project] [--all]"
      echo "  --claude   (default) install to ~/.claude/skills"
      echo "  --project  install into current directory project paths"
      echo "  --all      also ~/.agents/skills and ~/.cursor/skills"
      exit 0
      ;;
  esac
done

if [ ! -d "$SRC" ]; then
  echo "skills/ not found at $SRC" >&2
  exit 1
fi

copy_skills() {
  local dest="$1"
  mkdir -p "$dest"
  for d in "$SRC"/*; do
    [ -d "$d" ] || continue
    name="$(basename "$d")"
    rm -rf "$dest/$name"
    cp -R "$d" "$dest/$name"
    echo "  + $name -> $dest/$name"
  done
}

echo "api-platform-skills installer"
echo "source: $SRC"

if [ "$PROJECT" -eq 0 ] && [ "$CLAUDE" -eq 0 ] && [ "$ALL" -eq 0 ]; then
  CLAUDE=1
fi

if [ "$CLAUDE" -eq 1 ] || [ "$ALL" -eq 1 ]; then
  dest="$HOME/.claude/skills"
  echo "mode: Claude Code user skills"
  echo "-> $dest"
  copy_skills "$dest"
fi

if [ "$ALL" -eq 1 ]; then
  echo "mode: all user harnesses"
  for rel in .agents/skills .cursor/skills; do
    dest="$HOME/$rel"
    echo "-> $dest"
    copy_skills "$dest"
  done
fi

if [ "$PROJECT" -eq 1 ]; then
  BASE="${PWD}"
  echo "mode: project ($BASE)"
  for rel in .claude/skills .agents/skills .cursor/skills .github/skills; do
    echo "-> $BASE/$rel"
    copy_skills "$BASE/$rel"
  done
fi

echo ""
echo "Done. Restart Claude Code (or /reload-plugins)."
echo "Try: Review openapi.v1 vs openapi.v2-bad with breaking-change-review"
