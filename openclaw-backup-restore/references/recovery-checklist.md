# Recovery Checklist

## Before Wipe

- Confirm external disk is mounted.
- Confirm backup root exists and is readable.
- Confirm backup contains `user/openclaw/openclaw.json`.
- Confirm backup contains `user/openclaw/memory/*.sqlite`.
- Confirm backup contains `user/openclaw/workspace/`.
- Keep the external disk attached until restore is complete.
- Prefer a second copy of the most critical data if time permits.

## After Reinstall

- Reinstall OpenClaw first.
- Run `openclaw status` before restoring backup.
- Move fresh `~/.openclaw` aside instead of deleting it.
- Restore backup with `rsync`.
- Restart gateway if needed.
- Check memory DBs, workspace docs, credentials, and channels.

## If Restore Is Unstable

- Move restored `~/.openclaw` aside.
- Recreate empty `~/.openclaw`.
- Restore only config + memory + workspace + agents.
- Add credentials / telegram / cron later.

## Validation Signals

- `openclaw status` responds normally.
- `~/.openclaw/memory/*.sqlite` exists.
- `~/.openclaw/workspace/MEMORY.md` exists.
- Agent folders exist under `~/.openclaw/workspace/agents`.
- Required channel credential folders exist.
