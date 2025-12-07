# ️🛡️ Telegram Cyber Security Bot

This repo automatically posts AI-generated **Cybersecurity** education content to a Telegram **channel**.

## Features
- 🤖 **AI-Powered Content** - Uses Pollinations.ai (no API key needed) to generate educational posts.
- 🐞 **Vulnerability Focus** - Covers XSS, SQLi, RCE, IDOR, and more.
- 💻 **Code Snippets** - Every post includes a realistic code snippet demonstrating the bug or fix.
- 🎲 **Variety System** - Randomizes topics and uses seeds to ensure no two posts are alike.
- 🎨 **Dashboard** - Simple Flask web UI to manually trigger posts.
- ⏰ **Auto-Scheduling** - GitHub Actions runs periodically to keep the channel active.

## 1. Setup Telegram Bot & Channel

1. Talk to **@BotFather** on Telegram:
   - `/newbot` → get `BOT_TOKEN`
2. Add the bot as **Admin** to your channel (with "Post Messages" permission).
3. Find your `CHAT_ID` by calling:

   ```
   https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
   ```

   Look for `"chat":{"id": ... }` from your channel.

## 2. Local Setup

```bash
git clone <this-repo>
cd telegram-cyber-bot

cp .env.example .env   # then edit .env with your bot token and chat id
pip install -r requirements.txt
python -m src.main
```

This runs one cycle (posts a random cyber tip).

## 3. GitHub Actions Automation

1. Push this repo to GitHub.

2. Go to: **Settings → Secrets and variables → Actions**.

3. Add these repository secrets:
   - `BOT_TOKEN`
   - `CHAT_ID`
   - `TIMEZONE_OFFSET_HOURS` (e.g. 5.5 for IST)

The bot will run automatically according to the schedule in `.github/workflows/auto-post.yml`.

## 4. Dashboard (Manual Control)

```bash
cd dashboard
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 to manually send a Cybersecurity Post.

## Project Structure

```
telegram-cyber-bot/
├── .github/workflows/     # GitHub Actions automation
├── dashboard/             # Flask web UI for manual posting
├── src/                   # Core bot logic
│   ├── config.py         # Configuration management
│   ├── telegram_client.py # Telegram API wrapper
│   ├── pollinations_client.py # AI generation
│   ├── templates.py      # AI prompt templates (CyberSecurity focused)
│   ├── scheduler_logic.py # Scheduling logic
│   └── main.py           # Main orchestrator
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
└── README.md            # This file
```

## Customization

- **Edit prompts**: Modify `src/templates.py` to change how the AI writes about vulnerabilities.
- **Add Topics**: Edit `CYBER_TOPICS` in `src/main.py`.

## License

MIT
