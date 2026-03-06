#!/usr/bin/env python3
"""Diagnose common OpenClaw install/update blockers.

This script is designed for copy/paste debugging.
- Prints ONLY non-secret signals.
- Does not modify the system.

Typical usage:
  python3 skills/public/openclaw-bootstrap-helper/scripts/diagnose_openclaw_env.py
"""

from __future__ import annotations

import os
import platform
import shutil
import subprocess
from pathlib import Path


def which(cmd: str) -> str:
    p = shutil.which(cmd)
    return p or "(missing)"


def run(cmd: list[str]) -> tuple[int, str]:
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
        return 0, out.strip()
    except subprocess.CalledProcessError as e:
        return int(e.returncode), (e.output or "").strip()
    except FileNotFoundError:
        return 127, "(missing)"


def main() -> int:
    home = Path.home()
    cwd = Path.cwd()

    print("OPENCLAW_ENV_DIAG: v0.1")
    print(f"OS: {platform.platform()}")
    print(f"Python: {platform.python_version()}")
    print(f"CWD: {cwd}")
    print(f"CWD writable: {os.access(str(cwd), os.W_OK)}")

    skills_dir = cwd / "skills" / "public"
    alt_skills_dir = home / ".openclaw" / "workspace" / "skills" / "public"
    print(f"skills/public exists (cwd): {skills_dir.exists()}")
    print(f"skills/public exists (~/.openclaw/workspace): {alt_skills_dir.exists()}")

    print("TOOLS:")
    for tool in ["openclaw", "curl", "unzip", "git", "gh", "python3"]:
        print(f"- {tool}: {which(tool)}")

    code, out = run(["openclaw", "status"])
    print(f"openclaw status rc={code}")
    if out:
        print(out.splitlines()[0])

    code, out = run(["openclaw", "models", "list"])
    print(f"openclaw models list rc={code}")
    if out:
        print(out.splitlines()[0])

    # Exec approvals sock is a strong hint whether exec approvals are in play
    sock = home / ".openclaw" / "exec-approvals.sock"
    print(f"exec approvals sock exists: {sock.exists()}")

    print("NEXT:")
    print("- If curl/unzip missing, install them first.")
    print("- If openclaw status fails, run: openclaw status --all")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
