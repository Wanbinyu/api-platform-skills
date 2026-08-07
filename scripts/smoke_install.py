#!/usr/bin/env python3
"""Exercise the project-scoped installer without touching a user home directory."""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


TARGETS = (
    Path(".claude") / "skills",
    Path(".agents") / "skills",
    Path(".cursor") / "skills",
    Path(".github") / "skills",
)


def run_installer(root: Path, project: Path, clean: bool = False) -> None:
    if os.name == "nt":
        shell = shutil.which("pwsh") or shutil.which("powershell")
        if shell is None:
            raise RuntimeError("PowerShell is required for the Windows smoke test")
        command = [
            shell,
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(root / "scripts" / "install.ps1"),
            "-Project",
        ]
        if clean:
            command.append("-Clean")
    else:
        shell = shutil.which("bash")
        if shell is None:
            raise RuntimeError("bash is required for the Unix smoke test")
        command = [shell, str(root / "scripts" / "install.sh"), "--project"]
        if clean:
            command.append("--clean")

    result = subprocess.run(command, cwd=project, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(
            f"installer failed with exit code {result.returncode}\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )


def assert_installed(root: Path, project: Path) -> None:
    source_root = root / "skills"
    source_files = {
        path.relative_to(source_root): path.read_bytes()
        for path in source_root.rglob("*")
        if path.is_file()
    }
    expected_names = sorted(path.name for path in source_root.iterdir() if path.is_dir())

    for relative_target in TARGETS:
        target = project / relative_target
        if not target.is_dir():
            raise RuntimeError(f"missing install target: {target}")
        actual_names = sorted(path.name for path in target.iterdir() if path.is_dir())
        if actual_names != expected_names:
            raise RuntimeError(f"skill directory mismatch in {target}: {actual_names}")
        actual_files = {
            path.relative_to(target): path.read_bytes()
            for path in target.rglob("*")
            if path.is_file()
        }
        if actual_files != source_files:
            raise RuntimeError(f"installed files differ in {target}")


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    try:
        with tempfile.TemporaryDirectory(prefix="api-platform-install-") as temporary:
            project = Path(temporary)
            run_installer(root, project)
            assert_installed(root, project)

            stale = project / ".claude" / "skills" / "api-changelog" / "stale.txt"
            stale.write_text("preserve by default", encoding="utf-8")
            run_installer(root, project)
            if not stale.exists():
                raise RuntimeError("default install unexpectedly removed an existing file")

            run_installer(root, project, clean=True)
            if stale.exists():
                raise RuntimeError("clean install did not remove the stale file")
            assert_installed(root, project)
    except (OSError, RuntimeError) as exc:
        print(f"FAIL smoke install: {exc}", file=sys.stderr)
        return 1

    print("OK   project-scoped installer smoke test")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
