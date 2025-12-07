# 🚀 Setup Guide - Telegram AI Coding Channel Bot

## ✅ What's Been Done

Your Telegram bot is now fully set up with:
- ✅ Complete file structure
- ✅ Git repository initialized
- ✅ Initial commit created
- ✅ GitHub Actions workflow configured
- ✅ Flask dashboard for manual posting
- ✅ AI-powered content generation (Pollinations.ai)

## 📁 Project Structure

```
Telegram AI Coding Channel Bot/
├── .github/workflows/
│   └── auto-post.yml          # GitHub Actions automation
├── dashboard/
│   ├── app.py                 # Flask web app
│   ├── requirements.txt       # Dashboard dependencies
│   ├── templates/
│   │   ├── base.html         # Base template
│   │   └── dashboard.html    # Main dashboard
│   └── static/
│       └── styles.css        # Modern dark theme CSS
├── src/
│   ├── __init__.py
│   ├── config.py             # Environment configuration
│   ├── telegram_client.py    # Telegram API wrapper
│   ├── pollinations_client.py # AI generation
│   ├── templates.py          # AI prompt templates
│   ├── scheduler_logic.py    # Time-based posting
│   └── main.py               # Main orchestrator
├── .env.example              # Environment template
├── .gitignore                # Git ignore rules
├── README.md                 # Project documentation
└── requirements.txt          # Python dependencies
```

---

## 🔧 Step 1: Create Telegram Bot & Channel

### 1.1 Create Bot with BotFather

1. Open Telegram and search for **@BotFather**
2. Send `/newbot`
3. Follow the prompts to name your bot
4. **Save the BOT_TOKEN** (looks like: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 1.2 Create Your Channel

1. In Telegram, create a new channel (not a group)
2. Make it public or private (your choice)
3. Add your bot as an **Administrator** with "Post Messages" permission

### 1.3 Get Your CHAT_ID

1. Post something in your channel
2. Visit this URL in your browser (replace `<YOUR_BOT_TOKEN>`):
   ```
   https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
   ```
3. Look for `"chat":{"id": -1001234567890}` in the response
4. **Save the CHAT_ID** (it's a negative number for channels)

---

## 🖥️ Step 2: Local Setup & Testing

### 2.1 Create .env File

```bash
# Copy the example file
cp .env.example .env
```

Then edit `.env` with your actual values:
```env
BOT_TOKEN=1234567890:YOUR_ACTUAL_BOT_TOKEN
CHAT_ID=-1001234567890
TIMEZONE_OFFSET_HOURS=5.5
```

### 2.2 Install Dependencies

```bash
pip install -r requirements.txt
```

### 2.3 Test the Bot

```bash
python -m src.main
```

This will post content to your channel based on the current time!

### 2.4 Test the Dashboard

```bash
cd dashboard
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 in your browser and test manual posting.

---

## 🌐 Step 3: Push to GitHub

### 3.1 Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `telegram-ai-coding-channel` (or your choice)
3. **DO NOT** initialize with README (we already have one)
4. Click "Create repository"

### 3.2 Push Your Code

Run these commands in your terminal:

```bash
# Add GitHub as remote (replace YOUR_USERNAME and REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/telegram-ai-coding-channel.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Alternative with SSH:**
```bash
git remote add origin git@github.com:YOUR_USERNAME/telegram-ai-coding-channel.git
git branch -M main
git push -u origin main
```

---

## ⚙️ Step 4: Configure GitHub Actions

### 4.1 Add Repository Secrets

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add these three secrets:

| Name | Value | Example |
|------|-------|---------|
| `BOT_TOKEN` | Your bot token from BotFather | `1234567890:ABCdef...` |
| `CHAT_ID` | Your channel ID | `-1001234567890` |
| `TIMEZONE_OFFSET_HOURS` | Your timezone offset | `5.5` (for IST) |

### 4.2 Enable GitHub Actions

1. Go to **Actions** tab in your repository
2. If prompted, click "I understand my workflows, go ahead and enable them"
3. The workflow will now run automatically at:
   - 03:00 UTC
   - 09:00 UTC
   - 15:00 UTC
   - 21:00 UTC

### 4.3 Manual Trigger (Optional)

You can also trigger the workflow manually:
1. Go to **Actions** tab
2. Click "Telegram AI Auto Poster"
3. Click "Run workflow"

---

## 🎨 Step 5: Customization

### Change Posting Schedule

Edit `.github/workflows/auto-post.yml`:
```yaml
schedule:
  - cron: "0 3,9,15,21 * * *"  # Change these times
```

### Modify AI Prompts

Edit `src/templates.py` to customize what the AI generates.

### Adjust Time-Based Logic

Edit `src/scheduler_logic.py` to change what posts when.

---

## 🧪 Testing Checklist

- [ ] Bot token is valid
- [ ] Bot is admin in channel
- [ ] CHAT_ID is correct (negative number)
- [ ] Local test works (`python -m src.main`)
- [ ] Dashboard works (http://127.0.0.1:5000)
- [ ] Code pushed to GitHub
- [ ] GitHub secrets configured
- [ ] GitHub Actions enabled
- [ ] Manual workflow trigger works

---

## 🐛 Troubleshooting

### "BOT_TOKEN or CHAT_ID is not set"
- Check your `.env` file exists and has correct values
- For GitHub Actions, verify secrets are set correctly

### "Chat not found"
- Make sure bot is added as admin to channel
- Verify CHAT_ID is negative (for channels)
- Try posting in channel first, then get updates

### GitHub Actions not running
- Check if Actions are enabled in repository settings
- Verify secrets are named exactly: `BOT_TOKEN`, `CHAT_ID`, `TIMEZONE_OFFSET_HOURS`

### AI generation fails
- Pollinations.ai is free but may have rate limits
- Check your internet connection
- The API doesn't require authentication

---

## 📚 Next Steps

1. **Monitor**: Check your channel to see automated posts
2. **Customize**: Adjust prompts and schedules to your liking
3. **Expand**: Add more post types in `src/templates.py`
4. **Analytics**: Consider adding post tracking
5. **Backup**: Keep your `.env` file secure (never commit it!)

---

## 🆘 Need Help?

- Check the [README.md](README.md) for basic usage
- Review [Telegram Bot API docs](https://core.telegram.org/bots/api)
- Check [Pollinations.ai docs](https://pollinations.ai/)

---

**Happy Coding! 🎉**
