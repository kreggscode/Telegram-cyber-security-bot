from . import pollinations_client as ai
from . import telegram_client as tg
from . import scheduler_logic as sched
from .templates import TEXT_TEMPLATES
import random
import time
import re


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
    "XML External Entity (XXE) Injection",
    "API Security & Broken Object Level Authorization (BOLA)",
    "JWT Authentication Bypass & Algorithm Confusion",
    "Server-Side Template Injection (SSTI)"
]


def post_cyber_content():
    """
    Selects a random cybersecurity topic and posts educational content.
    """
    selected_topic = random.choice(CYBER_TOPICS)
    print(f"--- Started posting for topic: {selected_topic} ---")

    try:
        prompt_func = TEXT_TEMPLATES["cyber_prompt"]
        prompt = prompt_func(selected_topic)
        
        print(f"Generating content for {selected_topic}...")
        text_content = ai.generate_text(prompt)
        
        if "AI generation failed" in text_content or "AI Error" in text_content:
            print(f"FAILED: {text_content}")
            tg.send_text(f"⚠️ {text_content} for topic: {selected_topic}")
            raise RuntimeError(f"AI Generation Failed: {text_content}")

        # High-Intent SEO Search Index Bar & Hashtags
        hashtags = (
            "\n\n━━━━━━━━━━━━━━━━━━━━\n"
            "🔍 Topics: Cyber Security • Ethical Hacking • Bug Bounty • OWASP • AppSec\n"
            "🏷️ #CyberSecurity #EthicalHacking #InfoSec #PenetrationTesting #Hacking #BugBounty #AppSec #SecOps #SecurityAlert #LearnHacking"
        )
        text_content += hashtags

        # Send to Telegram
        print(f"Sending content to Telegram...")
        resp = tg.send_text(text_content)
        
        if resp and (resp.status_code == 200):
            print(f"SUCCESS: Posted content for {selected_topic}")
            
            # --- POST QUIZ BASED ON TOPIC ---
            print(f"Generating quiz for {selected_topic}...")
            quiz_prompt_func = TEXT_TEMPLATES["quiz_prompt"]
            quiz_prompt = quiz_prompt_func(selected_topic)
            quiz_raw = ai.generate_text(quiz_prompt)
            
            try:
                lines = [l.strip() for l in quiz_raw.split('\n') if l.strip()]
                q_text = ""
                options = []
                correct_letter = ""
                explanation = ""
                
                for line in lines:
                    line_lower = line.lower()
                    if line_lower.startswith("question:"):
                        q_text = line.split(":", 1)[1].strip()
                    elif re.match(r'^[A-D][:.)]\s+', line, re.I):
                        option_content = re.sub(r'^[A-D][:.)]\s+', '', line, flags=re.I).strip()
                        options.append(option_content)
                    elif "correct:" in line_lower:
                        match = re.search(r'[A-D]', line_lower.split(":", 1)[1])
                        if match:
                            correct_letter = match.group().upper()
                    elif "explanation:" in line_lower:
                        explanation = line.split(":", 1)[1].strip()
                
                if not q_text and lines:
                    q_text = lines[0]
                
                letter_to_index = {"A": 0, "B": 1, "C": 2, "D": 3}
                correct_id = letter_to_index.get(correct_letter if correct_letter else "A", 0)
                
                if q_text and len(options) >= 2:
                    print(f"Sending Quiz ({len(options)} options)...")
                    tg.send_quiz(
                        question=q_text,
                        options=options,
                        correct_option_id=correct_id,
                        explanation=explanation
                    )
                    print(f"SUCCESS: Posted Quiz for {selected_topic}")
                else:
                    print(f"WARNING: Quiz parsing failed (insufficient options: {len(options)})")
            except Exception as q_err:
                print(f"ERROR: Exception while creating Quiz: {q_err}")

    except Exception as e:
        print(f"ERROR: Failed posting cyber content: {e}")


def main():
    post_cyber_content()


if __name__ == "__main__":
    main()
