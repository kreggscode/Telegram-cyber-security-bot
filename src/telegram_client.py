import requests
from .config import BOT_TOKEN, CHAT_ID

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


def send_text(text: str):
    url = f"{BASE_URL}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    resp = requests.post(url, data=data)
    return resp


def send_photo(image_url: str, caption: str = ""):
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
