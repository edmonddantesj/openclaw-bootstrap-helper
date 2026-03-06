# OpenClaw Bootstrap Helper (Skill)

A small open-source skill that helps non-developers **install / update skills** and debug common blockers
(exec approvals, missing tools like `curl`/`unzip`, wrong paths, permissions, etc.).

## Install (latest .skill)

```bash
set -euo pipefail
URL="https://github.com/edmonddantesj/openclaw-bootstrap-helper/releases/latest/download/openclaw-bootstrap-helper.skill"
mkdir -p skills/public/openclaw-bootstrap-helper
curl -fsSL "$URL" -o /tmp/openclaw-bootstrap-helper.skill
unzip -o /tmp/openclaw-bootstrap-helper.skill -d skills/public/openclaw-bootstrap-helper
```

## What’s inside
- Skill folder: `openclaw-bootstrap-helper/`
- Scripts for diagnostics + generating copy/paste commands.

License: MIT
