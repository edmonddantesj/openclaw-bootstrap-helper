# OpenClaw Bootstrap Helper — Pre-bootstrap (Windows PowerShell)
# Goal: make Windows onboarding resilient (Git -> OpenClaw -> bootstrap-helper skill -> next steps)
# Safe posture: best-effort automation with clear fallbacks; no secrets collected.

$ErrorActionPreference = 'Stop'

function Write-Section($t) { Write-Host "`n=== $t ===" }
function Write-Warn($t) { Write-Host "[WARN] $t" -ForegroundColor Yellow }
function Write-Ok($t)   { Write-Host "[OK] $t" -ForegroundColor Green }
function Write-Err($t)  { Write-Host "[ERROR] $t" -ForegroundColor Red }

function Has-Cmd($name) {
  return [bool](Get-Command $name -ErrorAction SilentlyContinue)
}

function Ensure-Git {
  Write-Section "1) Git 확인"
  if (Has-Cmd git) {
    $v = (git --version 2>$null)
    Write-Ok "Git found: $v"
    return
  }

  Write-Warn "Git이 설치되어 있지 않습니다. OpenClaw 설치에 Git이 필요합니다."

  # Try winget if present
  if (Has-Cmd winget) {
    try {
      Write-Host "winget로 Git 설치를 시도합니다..."
      winget install --id Git.Git -e --source winget
      Write-Ok "winget Git install attempted. PowerShell을 새로 열고 다시 실행해 주세요."
      throw "RESTART_REQUIRED"
    } catch {
      if ($_.Exception.Message -eq 'RESTART_REQUIRED') { throw }
      Write-Warn "winget 설치가 실패했거나 권한/정책으로 차단되었습니다. 아래 링크로 수동 설치해 주세요."
    }
  }

  Write-Host "Git for Windows 설치 링크: https://git-scm.com/download/win"
  Write-Host "설치 후 PowerShell을 완전히 닫았다가 다시 열고, 아래로 확인해 주세요:"
  Write-Host "  git --version"
  throw "GIT_MISSING"
}

function Ensure-OpenClaw {
  Write-Section "2) OpenClaw 설치 여부 확인"
  if (Has-Cmd openclaw) {
    Write-Ok "openclaw command found"
    try {
      openclaw status | Select-Object -First 1 | ForEach-Object { Write-Ok "openclaw status: $_" }
    } catch {
      Write-Warn "openclaw status 실행이 실패했습니다. 그래도 설치는 되어 있을 수 있습니다. 다음 단계로 진행합니다."
    }
    return
  }

  Write-Warn "OpenClaw가 설치되어 있지 않습니다. 공식 설치 스크립트로 설치합니다."
  Write-Host "실행: iwr -useb https://openclaw.ai/install.ps1 | iex"
  try {
    iwr -useb https://openclaw.ai/install.ps1 | iex
  } catch {
    Write-Err "OpenClaw 설치 스크립트 실행이 실패했습니다. 오류 메시지를 운영자에게 전달해 주세요."
    throw
  }

  if (!(Has-Cmd openclaw)) {
    Write-Warn "설치 후에도 openclaw가 인식되지 않습니다. 보통 PATH 문제입니다."
    Write-Host "아래를 실행해서 나온 경로를 Windows 사용자 PATH에 추가 후 PowerShell 재실행:"
    Write-Host "  npm config get prefix"
    throw "OPENCLAW_PATH"
  }

  Write-Ok "OpenClaw installed"
}

function Install-BootstrapHelperSkill {
  Write-Section "3) openclaw-bootstrap-helper 스킬 설치(.skill)"

  $url = "https://github.com/edmonddantesj/openclaw-bootstrap-helper/releases/latest/download/openclaw-bootstrap-helper.skill"
  $tmp = Join-Path $env:TEMP "openclaw-bootstrap-helper.skill"

  $dest = Join-Path (Get-Location) "skills\public\openclaw-bootstrap-helper"
  New-Item -ItemType Directory -Force -Path $dest | Out-Null

  Write-Host "Downloading: $url"
  Invoke-WebRequest $url -OutFile $tmp

  Write-Host "Extracting skill to: $dest"
  Expand-Archive -Force $tmp $dest

  Write-Ok "Skill installed"
}

function Print-NextSteps {
  Write-Section "NEXT (채널 연결)"
  Write-Host "기본은 Telegram을 추천드립니다. (Slack/Discord도 선택 가능)"
  Write-Host "OpenClaw에서 onboarding 실행:"
  Write-Host "  openclaw onboard --install-daemon"
  Write-Host ""
  Write-Host "채널 선택:" 
  Write-Host "  - Telegram: 봇 토큰 + 채팅/그룹 연결"
  Write-Host "  - Discord: 봇 토큰 + 서버 연결"
  Write-Host "  - Slack: 앱 토큰/서명 시크릿 등"
  Write-Host ""
  Write-Host "설치 검증:"
  Write-Host "  openclaw status"
}

try {
  Write-Section "OpenClaw Pre-bootstrap (Windows)"
  Ensure-Git
  Ensure-OpenClaw
  Install-BootstrapHelperSkill
  Print-NextSteps
  Write-Ok "Done"
} catch {
  Write-Err "Pre-bootstrap failed: $($_.Exception.Message)"
  Write-Host "오류 화면/로그를 운영자에게 전달해 주세요." 
  throw
}
