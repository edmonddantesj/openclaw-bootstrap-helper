# OpenClaw Bootstrap Helper (Skill)

A small open-source skill that helps non-developers **install / update skills** and debug common blockers
(exec approvals, missing tools like `curl`/`unzip`, wrong paths, permissions, etc.).

It also supports **install packs** (minimal / recommended / full) while keeping a strict safety split:
- **Lite packs**: public-safe utilities (no wallet/payment/autopost)
- **Restricted pack**: wallet/payment/autopost/credential-handling skills (**opt-in only**)

## Install (latest .skill)

```bash
set -euo pipefail
URL="https://github.com/edmonddantesj/openclaw-bootstrap-helper/releases/latest/download/openclaw-bootstrap-helper.skill"
mkdir -p skills/public/openclaw-bootstrap-helper
curl -fsSL "$URL" -o /tmp/openclaw-bootstrap-helper.skill
unzip -o /tmp/openclaw-bootstrap-helper.skill -d skills/public/openclaw-bootstrap-helper
```

## Packs (copy/paste command generator)

Generate commands for a pack (safe-mode: prints commands only):

```bash
python3 skills/public/openclaw-bootstrap-helper/scripts/generate_pack_install_cmd.py --pack minimal
python3 skills/public/openclaw-bootstrap-helper/scripts/generate_pack_install_cmd.py --pack recommended
python3 skills/public/openclaw-bootstrap-helper/scripts/generate_pack_install_cmd.py --pack full-lite

# Explicit opt-in to restricted skills
python3 skills/public/openclaw-bootstrap-helper/scripts/generate_pack_install_cmd.py --pack full-lite --include-restricted
```

### Pack contents
Packs are pinned lists under `openclaw-bootstrap-helper/packs/`:
- `catalog.json` — skill slug → .skill URL, tags (Lite/Pro/Restricted), 1-line description
- `pack_*.txt` — newline-separated slugs

> We intentionally do NOT scrape web pages to build the list.
> Pinned lists are more reliable and easier to review.

## What’s inside
- Skill folder: `openclaw-bootstrap-helper/`
- Scripts for diagnostics + generating copy/paste commands.

License: MIT
