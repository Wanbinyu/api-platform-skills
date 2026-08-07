#!/usr/bin/env bash
# Install api-platform-skills for Claude Code and other agents.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$ROOT/skills"
PROJECT=0
CLAUDE=0
ALL=0
CLEAN=0

usage() {
  cat <<'EOF'
Usage: install.sh [--claude] [--project] [--all] [--clean]

  --claude, -c   Install to ~/.claude/skills (the default)
  --project, -p  Install to the current project's agent skill directories
  --all, -a      Install to Claude, .agents, and .cursor user directories
  --clean        Remove each existing package skill directory before copying
EOF
}

die() {
  echo "Error: $*" >&2
  exit 2
}

if [ ! -d "$SRC" ]; then
  die "skills/ not found at $SRC"
fi

for arg in "$@"; do
  case "$arg" in
    --project|-p) PROJECT=1 ;;
    --claude|-c) CLAUDE=1 ;;
    --all|-a) ALL=1 ;;
    --clean) CLEAN=1 ;;
    --help|-h) usage; exit 0 ;;
    *) usage >&2; die "unknown option: $arg" ;;
  esac
done

if [ "$PROJECT" -eq 0 ] && [ "$CLAUDE" -eq 0 ] && [ "$ALL" -eq 0 ]; then
  CLAUDE=1
fi

assert_destination() {
  local dest="$1"
  case "$dest" in
    ""|/) die "refusing to install into filesystem root" ;;
    "$SRC"|"$SRC"/*) die "refusing to install into the source tree: $dest" ;;
  esac
  if [ -L "$dest" ]; then
    die "refusing to install through a symlink: $dest"
  fi
  if [ -e "$dest" ] && [ ! -d "$dest" ]; then
    die "destination exists as a file: $dest"
  fi
}

assert_no_link_ancestors() {
  local current="$1"
  while [ -n "$current" ] && [ "$current" != "/" ]; do
    if [ -L "$current" ]; then
      die "refusing to install through a symlink: $current"
    fi
    current="$(dirname "$current")"
  done
}

copy_skills() {
  local dest="$1"
  assert_destination "$dest"
  assert_no_link_ancestors "$dest"
  mkdir -p "$dest"
  for source in "$SRC"/*; do
    [ -d "$source" ] || continue
    local name target
    name="$(basename "$source")"
    target="$dest/$name"
    if [ -L "$target" ]; then
      die "refusing to write through a symlink: $target"
    fi
    if [ -e "$target" ] && [ ! -d "$target" ]; then
      die "skill destination exists as a file: $target"
    fi
    if [ "$CLEAN" -eq 1 ] && [ -e "$target" ]; then
      rm -rf -- "$target"
    elif [ -d "$target" ] && [ -n "$(find "$target" -type l -print -quit)" ]; then
      die "refusing to write through a symlink below: $target"
    fi
    mkdir -p "$target"
    cp -R "$source/." "$target/"
    echo "  + $name -> $target"
  done
}

echo "api-platform-skills installer"
echo "source: $SRC"
if [ "$CLEAN" -eq 1 ]; then
  echo "Clean mode: existing package skill directories will be removed before copying."
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
  base="$PWD"
  echo "mode: project ($base)"
  for rel in .claude/skills .agents/skills .cursor/skills .github/skills; do
    echo "-> $base/$rel"
    copy_skills "$base/$rel"
  done
fi

echo ""
echo "Done."
