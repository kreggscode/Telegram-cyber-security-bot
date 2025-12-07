import requests
from .config import BOT_TOKEN, CHAT_ID

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


def add_social_footer(text: str) -> str:
    """Add social media links footer with larger, clickable text buttons."""
    footer = """

━━━━━━━━━━━━━━━━━━━━
🔗 **Connect with kreggscode:**

📷 [Instagram](https://instagram.com/kreggscode) • ✖️ [X/Twitter](https://x.com/kreggscode)
▶️ [YouTube](https://youtube.com/@kreggscode) • 💬 [Telegram](https://t.me/kreggscode)
📘 [Facebook Page](https://www.facebook.com/share/1b95f6Sn3c/) • 🎮 [My Apps](https://play.google.com/store/apps/dev?id=4822923174061161987)
"""
    return text + footer


def send_text(text: str, add_footer: bool = True):
    """Send text message with optional social media footer."""
    if add_footer:
        text = add_social_footer(text)
    
    url = f"{BASE_URL}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True  # Prevent link previews for cleaner posts
    }
    resp = requests.post(url, data=data)
    return resp


def send_photo(image_url: str, caption: str = "", add_footer: bool = True):
    """Send photo with optional social media footer in caption."""
    if add_footer and caption:
        caption = add_social_footer(caption)
    
    url = f"{BASE_URL}/sendPhoto"
    data = {
        "chat_id": CHAT_ID,
        "photo": image_url,
        "caption": caption,
        "parse_mode": "Markdown"
    }
    resp = requests.post(url, data=data)
    return resp


def send_poll(question: str, options: list[str]):
    import json
    url = f"{BASE_URL}/sendPoll"
    data = {
        "chat_id": CHAT_ID,
        "question": question,
        "options": json.dumps(options),
        "is_anonymous": False
    }
    resp = requests.post(url, data=data)
    return resp


def send_thread(messages: list[str]):
    for msg in messages:
        send_text(msg)
