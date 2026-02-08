import requests
import re
from .config import BOT_TOKEN, CHAT_ID

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


def markdown_to_html(text: str) -> str:
    """
    Converts basic Markdown (Bold, Code, Links) to Telegram-flavor HTML.
    This is much more robust than MarkdownV1/V2 for generated content.
    """
    if not text:
        return ""

    # 1. Escape HTML special characters (CRITICAL first step)
    html = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

    # 2. Convert Code blocks (```...```)
    # Use a placeholder system to avoid messing with content inside code blocks
    code_blocks = []
    def save_code(match):
        content = match.group(1).strip()
        code_blocks.append(content)
        return f"___CODEBLOCK_{len(code_blocks)-1}___"
    
    html = re.sub(r'```(?:[\w]*\n)?([\s\S]*?)```', save_code, html)

    # 3. Convert Inline code (`...`)
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)

    # 4. Convert Bold (**...**)
    html = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', html)

    # 5. Convert Links ([text](url))
    html = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', html)

    # 6. Restore code blocks with <pre>
    for i, block in enumerate(code_blocks):
        html = html.replace(f"___CODEBLOCK_{i}___", f"<pre>{block}</pre>")

    return html


def add_social_footer(text: str) -> str:
    """Add social media links footer using robust HTML hyperlinks."""
    footer = """
━━━━━━━━━━━━━━━━━━━━
🔗 <b>Connect with kreggscode:</b>

📷 <a href="https://instagram.com/kreggscode">Instagram</a> • ✖️ <a href="https://x.com/kreggscode">X/Twitter</a>
▶️ <a href="https://youtube.com/@kreggscode">YouTube</a> • 💬 <a href="https://t.me/kreggscode">Telegram</a>
📘 <a href="https://www.facebook.com/share/1b95f6Sn3c/">Facebook Page</a> • 🎮 <a href="https://play.google.com/store/apps/dev?id=4822923174061161987">My Apps</a>
"""
    return text + footer


def send_text(text: str, add_footer: bool = True, parse_mode: str = "HTML"):
    """Send text with robust HTML formatting."""
    # Convert Markdown to HTML if we are in HTML mode
    if parse_mode == "HTML":
        text = markdown_to_html(text)
    
    if add_footer:
        text = add_social_footer(text)
    
    # Safety truncation for Telegram limits
    if len(text) > 4000:
        text = text[:3800] + "\n\n...(truncated)"

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
            print(f"Telegram HTML Failure: {resp.text}")
            # Final fallback: Send as plain text if HTML is somehow broken
            payload.pop("parse_mode", None)
            payload["text"] = text.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&') # Clean for plain text
            resp = requests.post(url, json=payload, timeout=30)
        return resp
    except Exception as e:
        print(f"Telegram Connection Error: {e}")
        return None


def send_photo(image_url: str, caption: str = "", add_footer: bool = True, parse_mode: str = "HTML"):
    """Send photo with robust HTML caption."""
    if parse_mode == "HTML":
        caption = markdown_to_html(caption)

    if add_footer and caption:
        caption = add_social_footer(caption)
    
    if len(caption) > 1000:
        caption = caption[:950] + "..."
    
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
            print(f"Telegram Photo HTML Failure: {resp.text}")
            payload.pop("parse_mode", None)
            payload["caption"] = caption
            resp = requests.post(url, json=payload, timeout=30)
        return resp
    except Exception as e:
        print(f"Telegram Photo Error: {e}")
        return None


def send_poll(question: str, options: list[str], correct_option_id: int = None, explanation: str = None):
    """Send a native Telegram Quiz with HTML explanation support."""
    import json
    url = f"{BASE_URL}/sendPoll"
    
    # Process explanation if present
    if explanation:
        explanation = markdown_to_html(explanation)

    payload = {
        "chat_id": CHAT_ID,
        "question": question[:300],
        "options": json.dumps(options[:10]),
        "is_anonymous": True
    }

    if correct_option_id is not None:
        payload["type"] = "quiz"
        payload["correct_option_id"] = correct_option_id
        if explanation:
            payload["explanation"] = explanation[:200]
            payload["explanation_parse_mode"] = "HTML"

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
