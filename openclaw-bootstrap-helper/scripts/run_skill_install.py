#!/usr/bin/env python3
"""Run a .skill install/update (optional execute mode).

Default behavior is SAFE-MODE: print commands.
With --execute, will attempt to run them (no sudo).

This exists to support the workflow:
- Assistant asks user: "자동으로 진행할까?"
- If user says YES, assistant runs this script via exec.

Usage:
  python3 .../run_skill_install.py --url <.skill_url> --skill openclaw-telegram-topics-router
  python3 .../run_skill_install.py --url <.skill_url> --skill openclaw-telegram-topics-router --execute

Notes
- Installs to: skills/public/<skill>
- Downloads to: /tmp/<skill>.skill (or %TEMP% on Windows if supported)
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


def sh(cmd: list[str]) -> int:
    print("RUN:", " ".join(cmd))
    return subprocess.call(cmd)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--skill", required=True)
    ap.add_argument("--execute", action="store_true", help="Actually run the install commands")
    args = ap.parse_args()

    url = args.url
    skill = args.skill

    # Build commands (POSIX)
    target_dir = Path("skills") / "public" / skill
    tmp_path = Path("/tmp") / f"{skill}.skill"

    cmds = [
        ["mkdir", "-p", str(target_dir)],
        ["curl", "-fsSL", url, "-o", str(tmp_path)],
        ["unzip", "-o", str(tmp_path), "-d", str(target_dir)],
    ]

    if not args.execute:
        print("STATUS: plan")
        print("NOTE: safe-mode (printing only). Re-run with --execute to run.")
        for c in cmds:
            print(" ".join(c))
        return 0

    # Execute mode
    print("STATUS: executing")
    # Preconditions
    for bin_name in ["curl", "unzip", "mkdir"]:
        if not shutil_which(bin_name):
            print(f"ERROR: missing required tool: {bin_name}")
            return 2

    # Run
    for c in cmds:
        rc = sh(c)
        if rc != 0:
            print(f"ERROR: command failed rc={rc}")
            return rc

    print("STATUS: done")
    print(f"PROOF: installed_to={target_dir}")
    return 0


def shutil_which(name: str) -> str | None:
    # tiny local which to avoid importing shutil in older envs
    paths = os.environ.get("PATH", "").split(os.pathsep)
    exts = [""]
    if sys.platform.startswith("win"):
        exts = os.environ.get("PATHEXT", ".EXE;.BAT;.CMD").split(";")
    for p in paths:
        cand_base = Path(p) / name
        for e in exts:
            cand = Path(str(cand_base) + e)
            if cand.exists() and os.access(str(cand), os.X_OK):
                return str(cand)
    return None


if __name__ == "__main__":
    raise SystemExit(main())
