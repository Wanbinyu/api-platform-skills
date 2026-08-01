#!/usr/bin/env bash
# Install api-platform-skills into common agent skill directories.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$ROOT/skills"
PROJECT=0

for arg in "$@"; do
  case "$arg" in
    --project|-p) PROJECT=1 ;;
    --help|-h)
      echo "Usage: $0 [--project]"
      echo "  default: user-level install (home directories)"
      echo "  --project: install into current working directory project paths"
      exit 0
      ;;
  esac
done

copy_skills() {
  local dest="$1"
  mkdir -p "$dest"
  # shellcheck disable=SC2045
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

if [ "$PROJECT" -eq 1 ]; then
  BASE="${PWD}"
  echo "mode: project ($BASE)"
  for rel in .agents/skills .claude/skills .cursor/skills .github/skills; do
    echo "-> $BASE/$rel"
    copy_skills "$BASE/$rel"
  done
else
  echo "mode: user"
  for dest in \
    "$HOME/.agents/skills" \
    "$HOME/.claude/skills" \
    "$HOME/.cursor/skills"
  do
    echo "-> $dest"
    copy_skills "$dest"
  done
fi

echo "Done. Restart or re-index your agent if skills do not appear."
