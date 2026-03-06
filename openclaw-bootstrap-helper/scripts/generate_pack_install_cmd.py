#!/usr/bin/env python3
"""Generate copy/paste install commands for a skill *pack*.

Safe-mode by design: prints shell commands; does not execute.

Examples:
  # Minimal baseline (lite)
  python3 skills/public/openclaw-bootstrap-helper/scripts/generate_pack_install_cmd.py --pack minimal

  # Full lite pack
  python3 skills/public/openclaw-bootstrap-helper/scripts/generate_pack_install_cmd.py --pack full-lite

  # Full = full-lite + restricted (explicit opt-in)
  python3 skills/public/openclaw-bootstrap-helper/scripts/generate_pack_install_cmd.py --pack full-lite --include-restricted

Notes:
- Packs are pinned lists under `openclaw-bootstrap-helper/packs/`.
- Catalog is pinned in `openclaw-bootstrap-helper/packs/catalog.json`.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


HERE = Path(__file__).resolve()
SKILL_ROOT = HERE.parents[1]
PACKS_DIR = SKILL_ROOT / "packs"


PACK_FILE_BY_NAME = {
    "minimal": "pack_minimal.txt",
    "recommended": "pack_recommended.txt",
    "full-lite": "pack_full_lite.txt",
    "full-restricted": "pack_full_restricted.txt",
}


def _read_pack_slugs(pack_file: Path) -> list[str]:
    slugs: list[str] = []
    for raw in pack_file.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        slugs.append(line)
    return slugs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--pack",
        required=True,
        choices=sorted(PACK_FILE_BY_NAME.keys()),
        help="Pack name to generate commands for",
    )
    ap.add_argument(
        "--include-restricted",
        action="store_true",
        help="If set, additionally appends the full-restricted pack.",
    )
    args = ap.parse_args()

    catalog_path = PACKS_DIR / "catalog.json"
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    skills: dict = catalog.get("skills", {})

    pack_file = PACKS_DIR / PACK_FILE_BY_NAME[args.pack]
    slugs = _read_pack_slugs(pack_file)

    if args.include_restricted and args.pack != "full-restricted":
        restricted_file = PACKS_DIR / PACK_FILE_BY_NAME["full-restricted"]
        slugs.extend(_read_pack_slugs(restricted_file))

    # De-dupe while preserving order
    seen = set()
    deduped: list[str] = []
    for s in slugs:
        if s in seen:
            continue
        seen.add(s)
        deduped.append(s)

    # Validate
    missing = [s for s in deduped if s not in skills]
    if missing:
        print("# ERROR: missing slugs in catalog.json")
        for s in missing:
            print(f"# - {s}")
        print("# Fix: add them to openclaw-bootstrap-helper/packs/catalog.json")
        return 2

    print("# OpenClaw Bootstrap Helper — Pack install commands")
    print(f"# pack={args.pack} include_restricted={args.include_restricted}")
    print("set -euo pipefail")
    print("")

    for slug in deduped:
        meta = skills[slug]
        url = meta["url"]
        tags = ",".join(meta.get("tags", []))
        desc = meta.get("desc", "")
        print(f"# {slug} ({tags}) — {desc}")
        print(f"URL=\"{url}\"")
        print(f"mkdir -p skills/public/{slug}")
        print(f"curl -fsSL \"$URL\" -o /tmp/{slug}.skill")
        print(f"unzip -o /tmp/{slug}.skill -d skills/public/{slug}")
        print("")

    print("# Done. Restart OpenClaw if needed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
