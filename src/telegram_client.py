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


def send_text(text: str, add_footer: bool = True, parse_mode: str = "Markdown"):
    """Send text message with optional social media footer and retry on failure."""
    if add_footer:
        text = add_social_footer(text)
    
    # Telegram limit is 4096 characters. Truncate if extreme.
    if len(text) > 4000:
        text = text[:3997] + "..."

    url = f"{BASE_URL}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text,
        "disable_web_page_preview": True
    }
    if parse_mode:
        data["parse_mode"] = parse_mode

    try:
        resp = requests.post(url, data=data, timeout=30)
        if resp.status_code != 200:
            # If Markdown fails, retry without formatting
            if parse_mode == "Markdown":
                print(f"Telegram Markdown failed, retrying without formatting...")
                data.pop("parse_mode", None)
                resp = requests.post(url, data=data, timeout=30)
            
            if resp.status_code != 200:
                print(f"Telegram API Error (Text): {resp.status_code} - {resp.text}")
        return resp
    except Exception as e:
        print(f"Telegram Connection Error: {e}")
        # Return a mock response object for compatibility
        mock_resp = requests.Response()
        mock_resp.status_code = 500
        return mock_resp


def send_photo(image_url: str, caption: str = "", add_footer: bool = True, parse_mode: str = "Markdown"):
    """Send photo with optional social media footer in caption and retry on failure."""
    if add_footer and caption:
        caption = add_social_footer(caption)
    
    # Telegram limit for captions is 1024 characters
    if len(caption) > 1000:
        caption = caption[:997] + "..."

    url = f"{BASE_URL}/sendPhoto"
    data = {
        "chat_id": CHAT_ID,
        "photo": image_url,
        "caption": caption
    }
    if parse_mode:
        data["parse_mode"] = parse_mode

    try:
        resp = requests.post(url, data=data, timeout=30)
        if resp.status_code != 200:
            # If Markdown fails, retry without formatting
            if parse_mode == "Markdown":
                print(f"Telegram Markdown (Photo) failed, retrying without formatting...")
                data.pop("parse_mode", None)
                resp = requests.post(url, data=data, timeout=30)
            
            if resp.status_code != 200:
                print(f"Telegram API Error (Photo): {resp.status_code} - {resp.text}")
        return resp
    except Exception as e:
        print(f"Telegram Photo Connection Error: {e}")
        mock_resp = requests.Response()
        mock_resp.status_code = 500
        return mock_resp


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
