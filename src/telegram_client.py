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


def ensure_markdown_closed(text: str) -> str:
    """Ensure all markdown tags are properly closed to avoid Telegram parser errors."""
    if text.count('```') % 2 != 0:
        text += '\n```'
    if text.count('**') % 2 != 0:
        text += '**'
    # For single * or _, only close if it's likely a tag (not a bullet point)
    # But for Telegram V1, it's safer to just count.
    if text.count('*') % 2 != 0:
        text += '*'
    if text.count('_') % 2 != 0:
        text += '_'
    return text


def send_text(text: str, add_footer: bool = True, parse_mode: str = "Markdown"):
    """Send text message with integrity checks for Markdown."""
    if add_footer:
        text = add_social_footer(text)
    
    # Telegram limit is 4096 characters. Truncate safely.
    if len(text) > 4000:
        text = text[:3900]
        # Backtrack to last newline or space to avoid cutting words
        last_space = text.rfind(' ')
        if last_space > 3500:
            text = text[:last_space]
        text = ensure_markdown_closed(text)
        text += "\n\n...(Message truncated)"

    url = f"{BASE_URL}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text,
        "disable_web_page_preview": True,
        "parse_mode": parse_mode
    }

    try:
        resp = requests.post(url, data=data, timeout=30)
        if resp.status_code != 200:
            print(f"Telegram API Error (Text): {resp.status_code} - {resp.text}")
            # If it STILL fails, it might be due to a character that needs escaping in V1.
            # But we NEVER drop parse_mode because that ruins the links and code blocks.
        return resp
    except Exception as e:
        print(f"Telegram Connection Error: {e}")
        mock_resp = requests.Response()
        mock_resp.status_code = 500
        return mock_resp


def send_photo(image_url: str, caption: str = "", add_footer: bool = True, parse_mode: str = "Markdown"):
    """Send photo with protected caption integrity."""
    if add_footer and caption:
        caption = add_social_footer(caption)
    
    # Telegram limit for captions is 1024 characters
    if len(caption) > 1000:
        caption = caption[:950]
        last_space = caption.rfind(' ')
        if last_space > 800:
            caption = caption[:last_space]
        caption = ensure_markdown_closed(caption)
        caption += "..."

    url = f"{BASE_URL}/sendPhoto"
    data = {
        "chat_id": CHAT_ID,
        "photo": image_url,
        "caption": caption,
        "parse_mode": parse_mode
    }

    try:
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
