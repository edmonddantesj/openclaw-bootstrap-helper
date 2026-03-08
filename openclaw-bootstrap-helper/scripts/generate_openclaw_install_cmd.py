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
        choices=[
            "macos",
            "linux",
            "windows-powershell",
            "windows-wsl",
        ],
        help="Target environment",
    )
    args = ap.parse_args()

    if args.os == "macos":
        print("# macOS (recommended) — installer script")
        print("curl -fsSL https://openclaw.ai/install.sh | bash")
        print("openclaw status")
        return 0

    if args.os == "linux":
        print("# Linux (recommended) — installer script")
        print("curl -fsSL https://openclaw.ai/install.sh | bash")
        print("openclaw status")
        return 0

    if args.os == "windows-wsl":
        print("# Windows (WSL2 Ubuntu) — recommended")
        print("# 1) Install WSL2 (PowerShell as Admin): wsl --install")
        print("# 2) Then run OpenClaw installer in Ubuntu:")
        print("wsl.exe bash -lc 'curl -fsSL https://openclaw.ai/install.sh | bash' ")
        print("wsl.exe bash -lc 'openclaw status'")
        return 0

    if args.os == "windows-powershell":
        print("# Windows (PowerShell) — installer script")
        print("iwr -useb https://openclaw.ai/install.ps1 | iex")
        print("openclaw status")
        print("")
        print("# If 'openclaw' is not recognized after install:")
        print("# - Run: npm config get prefix")
        print("# - Add that directory to your user PATH, reopen PowerShell")
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
