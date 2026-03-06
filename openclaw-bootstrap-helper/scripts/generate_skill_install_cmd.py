#!/usr/bin/env python3
"""Generate copy/paste install/update commands for a .skill zip.

This script intentionally prints commands (safe-mode) instead of executing them.

Usage:
  python3 skills/public/openclaw-bootstrap-helper/scripts/generate_skill_install_cmd.py \
    --url https://github.com/OWNER/REPO/releases/latest/download/<name>.skill \
    --skill openclaw-telegram-topics-router
"""

from __future__ import annotations

import argparse


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True, help="Direct URL to .skill artifact")
    ap.add_argument("--skill", required=True, help="Target skill folder name")
    args = ap.parse_args()

    url = args.url
    skill = args.skill

    print("# macOS/Linux")
    print("set -euo pipefail")
    print(f"URL=\"{url}\"")
    print(f"mkdir -p skills/public/{skill}")
    print(f"curl -fsSL \"$URL\" -o /tmp/{skill}.skill")
    print(f"unzip -o /tmp/{skill}.skill -d skills/public/{skill}")
    print("")

    print("# Windows (WSL Ubuntu) — run in PowerShell")
    wsl_cmd = (
        "wsl.exe bash -lc 'set -euo pipefail; "
        + f"URL=\"{url}\"; "
        + f"mkdir -p skills/public/{skill}; "
        + f"curl -fsSL \"$URL\" -o /tmp/{skill}.skill; "
        + f"unzip -o /tmp/{skill}.skill -d skills/public/{skill}'"
    )
    print(wsl_cmd)
    print("")

    print("# Windows (Git Bash)")
    print("set -euo pipefail")
    print(f"URL=\"{url}\"")
    print(f"mkdir -p skills/public/{skill}")
    print(f"curl -fsSL \"$URL\" -o /tmp/{skill}.skill")
    print(f"unzip -o /tmp/{skill}.skill -d skills/public/{skill}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
