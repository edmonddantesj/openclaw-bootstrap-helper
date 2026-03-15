---
name: openclaw-backup-restore
description: Back up and restore OpenClaw user data, workspace, memories, credentials, logs, and related launch settings before macOS reset, machine migration, crash recovery, or reinstall. Use when preparing for wipe/reinstall, creating an external-disk backup, restoring ~/.openclaw after reinstall, or doing staged disaster recovery with bootstrap-based reinstall plus selective data restore.
---

# OpenClaw Backup & Restore

Use this skill for pre-wipe backups, post-reinstall recovery, migration to a new machine, or disaster recovery after repeated crashes.

## Workflow

1. Identify the backup target volume and verify free space.
2. Save environment snapshots before copying anything.
3. Back up `~/.openclaw` first.
4. Also back up diagnostic and launch configuration paths.
5. Exclude live IPC/transient files (`*.sock`, `*.lock`, `*.pid`, `.DS_Store`).
6. After reinstall, reinstall OpenClaw first.
7. Start OpenClaw once in a clean state before restoring user data.
8. Restore backup with `rsync`.
9. If full restore is unstable, fall back to minimal restore: config + memory + workspace + agents.

## Paths to Back Up

Always treat these as the default backup set:

- `~/.openclaw`
- `~/Library/Logs/DiagnosticReports`
- `~/Library/LaunchAgents`
- `/Library/LaunchAgents`
- `/Library/LaunchDaemons`

## Restore Order

1. Reinstall macOS / machine base.
2. Reinstall OpenClaw using the user's preferred bootstrap method.
3. Confirm `openclaw status` works in a fresh state.
4. Move the newly created `~/.openclaw` aside.
5. Restore from backup with `scripts/restore_openclaw.sh`.
6. Restart OpenClaw / gateway.
7. Validate memory DBs, workspace files, credentials, and channel state.

## Scripts

- For backup: run `scripts/backup_openclaw.sh <backup-root>`
- For restore: run `scripts/restore_openclaw.sh <backup-root>`

`<backup-root>` should be the parent folder created for a single backup run, for example:

- `/Volumes/ExternalDisk/openclaw-backup-2026-03-15-094159`

## When Full Restore Fails

Restore only these first:

- `openclaw.json`
- `.env`
- `memory/`
- `workspace/`
- `agents/`

Then add these later once the base runtime is stable:

- `credentials/`
- `telegram/`
- `cron/`
- `logs/`
- `browser/`
- `media/`
- `vault/`

## References

Read `references/recovery-checklist.md` for operator checklist and staged recovery guidance.
Read `references/layout.md` for backup contents and rationale.
