import os

from dotenv import load_dotenv

# Load .env when running locally; in GitHub Actions env vars are set directly
load_dotenv(override=False)

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
CHAT_ID = os.getenv("CHAT_ID", "").strip()
TIMEZONE_OFFSET_HOURS = float(os.getenv("TIMEZONE_OFFSET_HOURS", "5.5"))  # default IST

POLLINATIONS_API_KEY = os.getenv("POLLINATIONS_API_KEY", "").strip()
AI_MODEL = os.getenv("AI_MODEL", "openai").strip()

if not BOT_TOKEN or not CHAT_ID:
    raise RuntimeError("BOT_TOKEN or CHAT_ID is not set. Check your environment or .env file.")
