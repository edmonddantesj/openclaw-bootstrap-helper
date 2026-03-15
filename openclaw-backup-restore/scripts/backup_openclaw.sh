#!/bin/zsh
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <backup-root>" >&2
  exit 1
fi

BACKUP_ROOT="$1"
mkdir -p "$BACKUP_ROOT"/{snapshots,system,user}

cat > /tmp/openclaw-backup-excludes.txt <<'EOF'
*.sock
*.lock
*.lock.*
*.pid
.DS_Store
EOF

{
  echo '# OpenClaw status'
  openclaw status || true
} > "$BACKUP_ROOT/snapshots/openclaw-status.txt"

{
  echo '# Uptime'
  uptime || true
  echo
  echo '# Last reboot'
  last reboot | head -20 || true
  echo
  echo '# pmset assertions'
  pmset -g assertions || true
  echo
  echo '# pmset custom'
  pmset -g custom || true
} > "$BACKUP_ROOT/snapshots/power-and-reboot.txt"

{
  echo '# Applications'
  ls /Applications || true
} > "$BACKUP_ROOT/snapshots/applications.txt"

{
  echo '# openclaw top-level'
  find ~/.openclaw -maxdepth 2 -mindepth 1 | sort || true
} > "$BACKUP_ROOT/snapshots/openclaw-top-level.txt"

rsync -aH --exclude-from=/tmp/openclaw-backup-excludes.txt ~/.openclaw/ "$BACKUP_ROOT/user/openclaw/"
rsync -a ~/Library/Logs/DiagnosticReports/ "$BACKUP_ROOT/user/DiagnosticReports/"
rsync -a ~/Library/LaunchAgents/ "$BACKUP_ROOT/user/LaunchAgents/"
rsync -a /Library/LaunchAgents/ "$BACKUP_ROOT/system/LaunchAgents/"
rsync -a /Library/LaunchDaemons/ "$BACKUP_ROOT/system/LaunchDaemons/"

find "$BACKUP_ROOT" -type f | sort > "$BACKUP_ROOT/snapshots/manifest.txt"
du -sh "$BACKUP_ROOT" > "$BACKUP_ROOT/snapshots/backup-size.txt"
cp /tmp/openclaw-backup-excludes.txt "$BACKUP_ROOT/snapshots/rsync-excludes.txt"

echo "Backup complete: $BACKUP_ROOT"
