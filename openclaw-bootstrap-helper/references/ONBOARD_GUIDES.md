# Channel onboarding guides (checklist)

This file is a human-friendly checklist. Do not paste tokens into chat.

## Telegram (Bot)
- Create a bot in @BotFather
- Copy the bot token **locally**
- Run `openclaw onboard`
  - Choose Telegram
  - Paste the token into the local terminal prompt
- In group chats: ensure your bot can read messages (privacy mode) and is added as admin if needed.

## Discord
- Create a Discord application + bot
- Invite bot to server with required permissions
- Get the bot token **locally**
- Run `openclaw onboard`
  - Choose Discord
  - Paste token into local terminal

## Slack
- Create a Slack app
- Enable bot + scopes
- Install to workspace
- Get bot token/signing secrets **locally**
- Run `openclaw onboard` and choose Slack

## Safety
- Never paste channel tokens into public chats.
- Prefer entering secrets only in local terminal prompts.
