import os
from flask import Flask, render_template, redirect, url_for, flash
from dotenv import load_dotenv

# Allow dashboard to use same bot config
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"), override=False)

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src import telegram_client as tg
from src import pollinations_client as ai
from src.templates import TEXT_TEMPLATES, IMAGE_TEMPLATES

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")


@app.route("/")
def index():
    return render_template("dashboard.html")



@app.route("/send/cyber")
def send_cyber_post():
    from src.main import post_cyber_content
    # Redirecting stdout to capture print output if needed, or simply let it run
    # Since post_cyber_content prints to console, we might just trust it works or refactor main to return string.
    # For now, we will just call the function. It handles sending to Telegram.
    try:
        post_cyber_content()
        flash("Cyber Security Post sent!", "success")
    except Exception as e:
        flash(f"Error sending post: {e}", "error")
        
    return redirect(url_for("index"))



if __name__ == "__main__":
    app.run(debug=True)
