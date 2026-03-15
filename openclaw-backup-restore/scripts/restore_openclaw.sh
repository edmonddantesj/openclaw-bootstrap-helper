#!/bin/zsh
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <backup-root>" >&2
  exit 1
fi

BACKUP_ROOT="$1"
SRC="$BACKUP_ROOT/user/openclaw"

if [[ ! -d "$SRC" ]]; then
  echo "Backup source not found: $SRC" >&2
  exit 1
fi

cat > /tmp/openclaw-restore-excludes.txt <<'EOF'
*.sock
*.lock
*.lock.*
*.pid
.DS_Store
EOF

if [[ -d "$HOME/.openclaw" ]]; then
  mv "$HOME/.openclaw" "$HOME/.openclaw.fresh.$(date +%F-%H%M%S)"
fi
mkdir -p "$HOME/.openclaw"

rsync -aH --exclude-from=/tmp/openclaw-restore-excludes.txt "$SRC/" "$HOME/.openclaw/"

openclaw status || true
openclaw gateway restart || true
openclaw status || true

echo "Restore complete from: $BACKUP_ROOT"
