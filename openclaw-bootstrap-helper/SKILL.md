---
name: openclaw-bootstrap-helper
description: Help non-developers install/update OpenClaw skills and troubleshoot common blockers (exec approvals, missing curl/unzip/python3, wrong paths, permissions). Generates copy/paste commands and a short diagnosis report.
---

# OpenClaw Bootstrap Helper

Use this skill when a user says things like:
- "설치가 안 돼요" / "업데이트가 안 돼요" / "터미널 권한 때문에 막혀요"
- "텔레그램에서 링크만 주고 설치/업뎃시키고 싶어요"

## What to do

### 0) OpenClaw doctor (install + env)
- Run:
  - `python3 skills/public/openclaw-bootstrap-helper/scripts/openclaw_doctor.py`

### 1) Run a quick diagnosis (no secrets)
- Run:
  - `python3 skills/public/openclaw-bootstrap-helper/scripts/diagnose_openclaw_env.py`
- Paste the output into the chat.

### 2) Summarize a pasted terminal error into one next step (non-dev friendly)
- Run:
  - `python3 skills/public/openclaw-bootstrap-helper/scripts/summarize_install_error.py --text "<PASTE_ERROR>"`
  - or: `python3 skills/public/openclaw-bootstrap-helper/scripts/summarize_install_error.py --file /path/to/log.txt`
- Output is a single blocker + next action.

### 3) Generate a safe install/update command (copy/paste)
- Run:
  - `python3 skills/public/openclaw-bootstrap-helper/scripts/generate_skill_install_cmd.py --url <RELEASES_SKILL_URL> --skill openclaw-telegram-topics-router`
- The script prints OS-specific commands.

### 4) Safety defaults
- Do NOT request sudo by default.
- Prefer "safe-mode": generate a command for the user to copy/paste.
- If the environment blocks exec, explain the blocker and provide the minimal next action.

## References
- For common fixes, see:
  - `references/BLOCKERS.md`
- For channel setup checklists:
  - `references/ONBOARD_GUIDES.md`
