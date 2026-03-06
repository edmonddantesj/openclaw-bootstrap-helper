#!/usr/bin/env python3
"""Summarize common install/update errors into a single actionable next step.

This is meant for non-developers who paste a terminal error block.

Inputs:
- --text "..." (string)
- --file path/to/log.txt
- stdin (fallback)

Outputs:
- STATUS: ok|blocked|unknown
- BLOCKER: <short>
- NEXT: <one command or one instruction>

No secrets are extracted; this is pattern-based.
"""

from __future__ import annotations

import argparse
import re
import sys


PATTERNS: list[tuple[str, str, str]] = [
    (
        "missing_curl",
        r"(command not found: curl|curl: command not found)",
        "curl is missing",
        "Install curl, then re-run the install command. (Ubuntu/Debian: sudo apt-get update && sudo apt-get install -y curl)",
    ),
    (
        "missing_unzip",
        r"(command not found: unzip|unzip: command not found)",
        "unzip is missing",
        "Install unzip, then re-run the install command. (Ubuntu/Debian: sudo apt-get install -y unzip)",
    ),
    (
        "permission_denied",
        r"(Permission denied|EACCES|operation not permitted)",
        "permission denied (write/exec)",
        "Run the command in a writable folder, or create skills/public/<skill> under your OpenClaw workspace.",
    ),
    (
        "github_403",
        r"(HTTP 403|permission to .* denied|The requested URL returned error: 403)",
        "GitHub permission/auth issue (403)",
        "Re-auth GitHub (gh auth login) or use a token with repo scope; then retry.",
    ),
    (
        "not_a_zip",
        r"(End-of-central-directory signature not found|not a zipfile|cannot find zipfile directory)",
        "downloaded file is not a valid .skill zip",
        "Check the URL points to a .skill artifact (GitHub Releases) and that the download succeeded.",
    ),
    (
        "openclaw_missing",
        r"(openclaw: command not found|command not found: openclaw)",
        "openclaw CLI not found",
        "Install OpenClaw first, then retry. If installed, restart terminal so PATH updates.",
    ),
    (
        "python_missing",
        r"(python3: command not found|command not found: python3)",
        "python3 is missing",
        "Install Python 3, then retry. (macOS: brew install python | Ubuntu: sudo apt-get install -y python3)",
    ),
]


def read_text(args: argparse.Namespace) -> str:
    if args.text:
        return args.text
    if args.file:
        return open(args.file, "r", encoding="utf-8", errors="replace").read()
    return sys.stdin.read()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", default=None, help="Paste error text")
    ap.add_argument("--file", default=None, help="Read error text from file")
    args = ap.parse_args()

    text = read_text(args)
    text_norm = text.strip()

    if not text_norm:
        print("STATUS: unknown")
        print("BLOCKER: empty input")
        print("NEXT: paste the full error block (including the command you ran)")
        return 1

    # Reduce noise
    t = text_norm
    # Make matching more robust
    t_low = t.lower()

    for key, rx, blocker, nxt in PATTERNS:
        if re.search(rx, t, flags=re.IGNORECASE | re.MULTILINE) or re.search(rx, t_low, flags=re.IGNORECASE | re.MULTILINE):
            print("STATUS: blocked")
            print(f"BLOCKER: {blocker}")
            print(f"NEXT: {nxt}")
            print(f"HINT: pattern={key}")
            return 0

    # Generic fallback
    print("STATUS: unknown")
    print("BLOCKER: unrecognized error")
    print("NEXT: run the env diagnosis script and paste its output")
    print("CMD: python3 skills/public/openclaw-bootstrap-helper/scripts/diagnose_openclaw_env.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
