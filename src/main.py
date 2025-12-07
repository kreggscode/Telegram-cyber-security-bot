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
    
    print(f"Selected topic for this run: {selected_topic}")

    try:
        # Generate content
        prompt_func = TEXT_TEMPLATES["cyber_prompt"]
        prompt = prompt_func(selected_topic)
        
        print(f"Generating content for {selected_topic}...")
        text_content = ai.generate_text(prompt)
        
        # Send to Telegram
        tg.send_text(text_content)
        
    except Exception as e:
        print(f"Error posting for {selected_topic}: {e}")
        tg.send_text(f"⚠️ Error generating content for {selected_topic}. Please check logs.")


def main():
    post_type = sched.decide_post_type()
    print(f"Decided post type: {post_type}")

    if post_type == "cyber_post":
        post_cyber_content()
    else:
        tg.send_text("No valid post type decided.")


if __name__ == "__main__":
    main()
