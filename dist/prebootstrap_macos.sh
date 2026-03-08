#!/usr/bin/env bash
set -euo pipefail

# OpenClaw Bootstrap Helper — Pre-bootstrap (macOS)
# Goal: make macOS onboarding resilient (tools -> OpenClaw -> bootstrap-helper skill -> next steps)
# Safe posture: best-effort automation with clear fallbacks; no secrets collected.

say() { printf "\n=== %s ===\n" "$*"; }
ok()  { printf "[OK] %s\n" "$*"; }
warn(){ printf "[WARN] %s\n" "$*" >&2; }
err() { printf "[ERROR] %s\n" "$*" >&2; }

need_cmd() {
  command -v "$1" >/dev/null 2>&1
}

ensure_xcode_clt() {
  # Many macOS setups miss git until Xcode CLT is installed.
  if need_cmd git; then return 0; fi

  say "1) Required tools (git)"
  warn "git is missing. On macOS this usually means Xcode Command Line Tools are not installed."
  warn "Attempting: xcode-select --install (a GUI prompt may appear)."

  if xcode-select -p >/dev/null 2>&1; then
    warn "xcode-select already configured but git is still missing. Please install Git manually or reinstall CLT."
  else
    # This may return non-zero if the installer is already in progress.
    xcode-select --install >/dev/null 2>&1 || true
  fi

  warn "After CLT installation completes, re-run this script."
  exit 20
}

ensure_tools() {
  say "1) Tooling check"
  # curl/unzip are usually present on macOS; git may be missing.
  for t in curl unzip; do
    if need_cmd "$t"; then ok "$t found"; else err "$t missing"; exit 21; fi
  done

  if ! need_cmd git; then
    ensure_xcode_clt
  fi

  ok "git found: $(git --version 2>/dev/null || true)"
}

ensure_openclaw() {
  say "2) OpenClaw install check"
  if need_cmd openclaw; then
    ok "openclaw command found"
    openclaw status 2>/dev/null | head -n 1 || true
    return 0
  fi

  warn "OpenClaw is not installed. Installing via official installer script."
  curl -fsSL https://openclaw.ai/install.sh | bash

  if ! need_cmd openclaw; then
    err "OpenClaw install finished but 'openclaw' is still not on PATH."
    err "Please open a NEW terminal and run: openclaw status"
    exit 22
  fi

  ok "OpenClaw installed"
}

install_bootstrap_helper_skill() {
  say "3) Install openclaw-bootstrap-helper skill (.skill)"

  local url tmp workspace dest
  url="https://github.com/edmonddantesj/openclaw-bootstrap-helper/releases/latest/download/openclaw-bootstrap-helper.skill"
  tmp="/tmp/openclaw-bootstrap-helper.skill"

  workspace="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
  dest="$workspace/skills/public/openclaw-bootstrap-helper"

  mkdir -p "$dest"
  ok "workspace: $workspace"

  ok "downloading: $url"
  curl -fsSL "$url" -o "$tmp"

  ok "extracting to: $dest"
  unzip -o "$tmp" -d "$dest" >/dev/null

  ok "skill installed"
}

print_next_steps() {
  say "NEXT (channels)"
  cat <<'TXT'
Default recommendation: Telegram.
You can also choose Slack/Discord later.

Next commands:
- openclaw onboard --install-daemon
- openclaw status
TXT
}

main() {
  say "OpenClaw Pre-bootstrap (macOS)"
  ensure_tools
  ensure_openclaw
  install_bootstrap_helper_skill
  print_next_steps
  ok "Done"
}

main "$@"
