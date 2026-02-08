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
    """
    Robustly ensure all Telegram Markdown (V1) tags are properly closed.
    V1 uses: *bold*, _italic_, `inline code`, ```pre/code blocks```, [text](url)
    """
    # 1. Balance triple backticks (Preformatted blocks)
    # We must do this first because nothing inside a pre block should be parsed.
    if text.count('```') % 2 != 0:
        text += '\n```'
    
    # Split text into parts that are NOT inside triple backticks
    parts = text.split('```')
    # parts[0], parts[2], ... are OUTSIDE code blocks
    # parts[1], parts[3], ... are INSIDE code blocks
    
    for i in range(0, len(parts), 2):
        chunk = parts[i]
        
        # 2. Balance single backticks (Inline code)
        if chunk.count('`') % 2 != 0:
            chunk += '`'
        
        # Split chunk into parts NOT inside inline code
        subparts = chunk.split('`')
        for j in range(0, len(subparts), 2):
            subchunk = subparts[j]
            
            # 3. Balance Bold (*) and Italic (_)
            # Note: Telegram V1 is picky. Underscores in URLs or variables often break it.
            if subchunk.count('*') % 2 != 0:
                subchunk += '*'
            if subchunk.count('_') % 2 != 0:
                subchunk += '_'
            
            # 4. Balance links [text](url)
            # This is hard to do perfectly with count, but we can check for unclosed [
            open_brackets = subchunk.count('[')
            closed_brackets = subchunk.count(']')
            if open_brackets > closed_brackets:
                subchunk += ']' * (open_brackets - closed_brackets)
            
            subparts[j] = subchunk
        
        parts[i] = '`'.join(subparts)
    
    return '```'.join(parts)


def send_text(text: str, add_footer: bool = True, parse_mode: str = "Markdown"):
    """Send text message with integrity checks for Markdown."""
    if add_footer:
        text = add_social_footer(text)
    
    # Telegram limit is 4096 characters. Truncate safely.
    if len(text) > 4000:
        text = text[:3800]
        # Backtrack to last newline or space
        last_space = text.rfind(' ')
        if last_space > 3500:
            text = text[:last_space]
        text += "\n\n...(Message truncated)"

    text = ensure_markdown_closed(text)

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
            # Check if it's a parsing error
            error_data = resp.json() if resp.status_code == 400 else {}
            if "can't parse" in error_data.get("description", "").lower():
                print(f"Telegram Markdown parsing failed at offset. Retrying with escaped technical characters...")
                # Hack for V1: Escape underscores inside words if they are causing issues
                # But V1 doesn't support \ escaping for _, it treats \_ as literally \ and _
                # The real fix is to balance or strip. We already balanced.
                # Let's try stripping the most problematic V1 character: standalone underscores
                sanitized_text = text.replace("_", "\\_") # Wait, V1 doesn't like \_?
                # Actually, in V1, escaping *is* done with \. (Docs say so for some versions)
                data["text"] = sanitized_text
                resp = requests.post(url, data=data, timeout=30)
                
                if resp.status_code != 200:
                    print(f"Advanced sanitization failed, trying Clean fallback (No formatting)...")
                    # Last resort: clear formatting but keep content
                    data.pop("parse_mode", None)
                    data["text"] = text.replace("*", "").replace("_", "").replace("`", "")
                    resp = requests.post(url, data=data, timeout=30)
            
            if resp.status_code != 200:
                print(f"Telegram API Error (Text): {resp.status_code} - {resp.text}")
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


def send_poll(question: str, options: list[str], correct_option_id: int = None, explanation: str = None):
    """Send a Telegram poll. If correct_option_id is provided, it becomes a Quiz."""
    import json
    url = f"{BASE_URL}/sendPoll"
    data = {
        "chat_id": CHAT_ID,
        "question": question,
        "options": json.dumps(options),
        "is_anonymous": False
    }

    if correct_option_id is not None:
        data["type"] = "quiz"
        data["correct_option_id"] = correct_option_id
        if explanation:
            # Explanation is shown when the user answers incorrectly or taps the bulb icon
            data["explanation"] = explanation
            data["explanation_parse_mode"] = "Markdown"

    try:
        resp = requests.post(url, data=data, timeout=30)
        if resp.status_code != 200:
            print(f"Telegram API Error (Poll): {resp.status_code} - {resp.text}")
        return resp
    except Exception as e:
        print(f"Telegram Poll Connection Error: {e}")
        mock_resp = requests.Response()
        mock_resp.status_code = 500
        return mock_resp


def send_thread(messages: list[str]):
    for msg in messages:
        send_text(msg)
