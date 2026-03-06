# Common blockers (quick fixes)

## Missing tools
- `curl` missing
  - macOS: install Xcode Command Line Tools (`xcode-select --install`)
  - Ubuntu/Debian: `sudo apt-get update && sudo apt-get install -y curl`
- `unzip` missing
  - macOS: usually present; otherwise via Homebrew (`brew install unzip`)
  - Ubuntu/Debian: `sudo apt-get install -y unzip`

## Permissions / paths
- Make sure you're in a writable folder and `skills/public/<skill>` exists.
- If the agent can't run commands (exec approvals): copy/paste the printed command into terminal.

## Network
- GitHub Releases URL must be reachable.
- If corporate network blocks GitHub, try another network.
