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
    """Hyper-reliable balancing of Telegram Markdown V1 tags."""
    # Pre blocks
    if text.count('```') % 2 != 0: text += '\n```'
    
    # Check outside blocks for unclosed tags
    code_parts = text.split('```')
    for i in range(0, len(code_parts), 2):
        # bold
        if code_parts[i].count('*') % 2 != 0: code_parts[i] += '*'
        # italic
        if code_parts[i].count('_') % 2 != 0: code_parts[i] += '_'
        # inline code
        if code_parts[i].count('`') % 2 != 0: code_parts[i] += '`'
        # links [text](url) - only check [ ] balance
        if code_parts[i].count('[') > code_parts[i].count(']'):
            code_parts[i] += ']'
    return '```'.join(code_parts)


def send_text(text: str, add_footer: bool = True, parse_mode: str = "Markdown"):
    """Send text with guaranteed formatting for links and code blocks."""
    if add_footer:
        text = add_social_footer(text)
    
    # Safety truncation
    if len(text) > 4000:
        text = text[:3800] + "\n\n...(truncated)"

    text = ensure_markdown_closed(text)

    url = f"{BASE_URL}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "disable_web_page_preview": True,
        "parse_mode": parse_mode
    }

    try:
        resp = requests.post(url, json=payload, timeout=30)
        if resp.status_code != 200:
            print(f"Telegram Markdown Failure: {resp.text}")
            # Try escaping ONLY the underscores (v1 major culprit) but keep everything else
            payload["text"] = text.replace("_", "\\_")
            resp = requests.post(url, json=payload, timeout=30)
            
            if resp.status_code != 200:
                print(f"STILL FAILED: {resp.status_code}. Sending without formatting to preserve content.")
                payload.pop("parse_mode", None)
                payload["text"] = text
                resp = requests.post(url, json=payload, timeout=30)
        return resp
    except Exception as e:
        print(f"Telegram Connection Error: {e}")
        return None


def send_photo(image_url: str, caption: str = "", add_footer: bool = True, parse_mode: str = "Markdown"):
    """Send photo with guaranteed caption integrity."""
    if add_footer and caption:
        caption = add_social_footer(caption)
    
    if len(caption) > 1000:
        caption = caption[:950] + "..."
    
    caption = ensure_markdown_closed(caption)

    url = f"{BASE_URL}/sendPhoto"
    payload = {
        "chat_id": CHAT_ID,
        "photo": image_url,
        "caption": caption,
        "parse_mode": parse_mode
    }

    try:
        resp = requests.post(url, json=payload, timeout=30)
        if resp.status_code != 200:
            # Fallback for photo caption
            payload["caption"] = caption.replace("_", "\\_")
            resp = requests.post(url, json=payload, timeout=30)
            if resp.status_code != 200:
                payload.pop("parse_mode", None)
                payload["caption"] = caption
                resp = requests.post(url, json=payload, timeout=30)
        return resp
    except Exception as e:
        print(f"Telegram Photo Error: {e}")
        return None


def send_poll(question: str, options: list[str], correct_option_id: int = None, explanation: str = None):
    """Send a native Telegram Quiz."""
    import json
    url = f"{BASE_URL}/sendPoll"
    payload = {
        "chat_id": CHAT_ID,
        "question": question[:300],
        "options": json.dumps(options[:10]),
        "is_anonymous": False
    }

    if correct_option_id is not None:
        payload["type"] = "quiz"
        payload["correct_option_id"] = correct_option_id
        if explanation:
            payload["explanation"] = explanation[:200]
            payload["explanation_parse_mode"] = "Markdown"

    try:
        resp = requests.post(url, json=payload, timeout=30)
        if resp.status_code != 200:
            print(f"QUIZ FAILURE: {resp.status_code} - {resp.text}")
        return resp
    except Exception as e:
        print(f"Quiz Connection Error: {e}")
        return None


def send_thread(messages: list[str]):
    for msg in messages:
        send_text(msg)
