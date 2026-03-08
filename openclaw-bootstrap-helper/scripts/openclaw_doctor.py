#!/usr/bin/env python3
"""OpenClaw doctor: check install, version, and common blockers.

Safe-mode: read-only checks.

Usage:
  python3 skills/public/openclaw-bootstrap-helper/scripts/openclaw_doctor.py
"""

from __future__ import annotations

import os
import platform
import shutil
import subprocess
from pathlib import Path


def which(cmd: str) -> str:
    return shutil.which(cmd) or "(missing)"


def run(cmd: list[str]) -> tuple[int, str]:
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
        return 0, out.strip()
    except subprocess.CalledProcessError as e:
        return int(e.returncode), (e.output or "").strip()
    except FileNotFoundError:
        return 127, "(missing)"


def head1(s: str) -> str:
    return (s.splitlines()[:1] or [""])[0]


def main() -> int:
    home = Path.home()
    cwd = Path.cwd()

    print("OPENCLAW_DOCTOR: v0.2")
    print(f"OS: {platform.platform()}")
    print(f"Python: {platform.python_version()}")
    print(f"CWD: {cwd}")
    print(f"CWD writable: {os.access(str(cwd), os.W_OK)}")

    print("BIN:")
    print(f"- openclaw: {which('openclaw')}")

    print("TOOLS:")
    for tool in ["curl", "unzip", "git", "gh", "python3", "node", "npm"]:
        print(f"- {tool}: {which(tool)}")

    rc, out = run(["openclaw", "status"])
    print(f"openclaw status rc={rc}")
    if out:
        print(f"openclaw status head: {head1(out)}")

    # Quick hint for workspace
    ws = home / ".openclaw" / "workspace"
    print(f"default workspace exists: {ws.exists()} ({ws})")

    # Exec approvals sock hint
    sock = home / ".openclaw" / "exec-approvals.sock"
    print(f"exec approvals sock exists: {sock.exists()}")

    print("NEXT:")
    if which("openclaw") == "(missing)":
        print("- OpenClaw is not installed.")
        print("  Generate copy/paste install commands:")
        print("  - Windows (PowerShell): python3 skills/public/openclaw-bootstrap-helper/scripts/generate_openclaw_install_cmd.py --os windows-powershell")
        print("  - Windows (WSL2):      python3 skills/public/openclaw-bootstrap-helper/scripts/generate_openclaw_install_cmd.py --os windows-wsl")
        print("  - macOS:               python3 skills/public/openclaw-bootstrap-helper/scripts/generate_openclaw_install_cmd.py --os macos")
        print("  - Linux:               python3 skills/public/openclaw-bootstrap-helper/scripts/generate_openclaw_install_cmd.py --os linux")
    else:
        print("- If channels/models are not configured, run: openclaw onboard")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
