#!/usr/bin/env python3
"""Generate copy/paste commands to install OpenClaw.

Safe-mode: prints commands only.

Usage:
  python3 skills/public/openclaw-bootstrap-helper/scripts/generate_openclaw_install_cmd.py --os macos
  python3 ... --os windows-wsl

Note: Installation methods may vary by environment. This script provides a conservative baseline.
"""

from __future__ import annotations

import argparse


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--os",
        required=True,
        choices=["macos", "windows-wsl", "windows-gitbash", "linux"],
        help="Target environment",
    )
    args = ap.parse_args()

    if args.os == "macos":
        print("# macOS (Homebrew)")
        print("brew install openclaw")
        print("openclaw status")
        return 0

    if args.os == "linux":
        print("# Linux")
        print("# Install method depends on distro/package manager.")
        print("# If you already have npm/pnpm: you can install OpenClaw via npm.")
        print("npm install -g openclaw")
        print("openclaw status")
        return 0

    if args.os == "windows-wsl":
        print("# Windows (WSL Ubuntu) — run in PowerShell")
        print("wsl.exe bash -lc 'set -euo pipefail; npm install -g openclaw; openclaw status'")
        return 0

    if args.os == "windows-gitbash":
        print("# Windows (Git Bash)")
        print("# Requires Node.js + npm")
        print("npm install -g openclaw")
        print("openclaw status")
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
