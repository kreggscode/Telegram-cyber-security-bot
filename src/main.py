from . import pollinations_client as ai
from . import telegram_client as tg
from . import scheduler_logic as sched
from .templates import TEXT_TEMPLATES
import random
import time


# List of Cybersecurity Topics
CYBER_TOPICS = [
    "Cross-Site Scripting (XSS)",
    "SQL Injection (SQLi)",
    "Cross-Site Request Forgery (CSRF)",
    "Insecure Direct Object References (IDOR)",
    "Server-Side Request Forgery (SSRF)",
    "Remote Code Execution (RCE)",
    "Directory Traversal",
    "Buffer Overflow",
    "Man-in-the-Middle (MitM) Attacks",
    "DNS Spoofing",
    "Phishing & Social Engineering",
    "Cryptographic Failures",
    "Broken Access Control",
    "Security Misconfiguration",
    "XML External Entity (XXE) Injection"
]

def post_cyber_content():
    """
    Selects a random cybersecurity topic and posts educational content.
    """
    # Select 1 topic
    selected_topic = random.choice(CYBER_TOPICS)
    
    print(f"--- Started posting for topic: {selected_topic} ---")

    try:
        # Generate content
        prompt_func = TEXT_TEMPLATES["cyber_prompt"]
        prompt = prompt_func(selected_topic)
        
        print(f"Generating content for {selected_topic}...")
        text_content = ai.generate_text(prompt)
        
        # Check if generation returned an error message
        if "AI generation failed" in text_content or "AI Error" in text_content:
            print(f"FAILED: {text_content}")
            tg.send_text(f"⚠️ {text_content} for topic: {selected_topic}")
            return

        # Send to Telegram
        print(f"Sending content to Telegram...")
        resp = tg.send_text(text_content)
        
        if resp.status_code == 200:
            print(f"SUCCESS: Posted content for {selected_topic}")
        else:
            print(f"FAILED to send to Telegram: {resp.status_code} - {resp.text}")
            # Fallback if the whole message was rejected (e.g. too long or bad markdown)
            tg.send_text(f"⚠️ Error sending content for {selected_topic} to Telegram. (Status: {resp.status_code})", add_footer=False)
        
    except Exception as e:
        print(f"CRITICAL ERROR in post_cyber_content: {e}")
        tg.send_text(f"⚠️ Critical error generating content for {selected_topic}. Please check system logs.")


def main():
    post_type = sched.decide_post_type()
    print(f"Decided post type: {post_type}")

    if post_type == "cyber_post":
        post_cyber_content()
    else:
        tg.send_text("No valid post type decided.")


if __name__ == "__main__":
    main()
