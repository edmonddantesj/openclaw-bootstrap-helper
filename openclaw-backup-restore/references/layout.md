# Backup Layout

## Primary User Data

- `~/.openclaw/openclaw.json` — main config
- `~/.openclaw/.env` — environment configuration
- `~/.openclaw/memory/` — memory sqlite databases
- `~/.openclaw/workspace/` — workspace, markdown, artifacts, agents, context
- `~/.openclaw/agents/` — agent definitions and local agent state
- `~/.openclaw/credentials/` — channel and auth material
- `~/.openclaw/telegram/` — Telegram operational state
- `~/.openclaw/cron/` — cron jobs and run metadata
- `~/.openclaw/logs/` — operational logs
- `~/.openclaw/browser/` — browser state used by OpenClaw
- `~/.openclaw/media/` — media cache and inbound/outbound media
- `~/.openclaw/vault/` — local vault/env material

## Auxiliary System Data

- `~/Library/Logs/DiagnosticReports` — panic/crash reports
- `~/Library/LaunchAgents` — user launch agents
- `/Library/LaunchAgents` — system launch agents
- `/Library/LaunchDaemons` — system launch daemons

## Exclusions

Do not rely on live IPC/transient files during restore. Exclude:

- `*.sock`
- `*.lock`
- `*.lock.*`
- `*.pid`
- `.DS_Store`

These files are recreated automatically or are unsafe to restore verbatim.
