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
        
        # If successfully sent (including fallback), proceed to Quiz
        if resp and (resp.status_code == 200):
            print(f"SUCCESS: Posted content for {selected_topic}")
            
            # --- POST QUIZ BASED ON TOPIC ---
            print(f"Generating quiz for {selected_topic}...")
            quiz_prompt_func = TEXT_TEMPLATES["quiz_prompt"]
            quiz_prompt = quiz_prompt_func(selected_topic)
            quiz_raw = ai.generate_text(quiz_prompt)
            
            # Robust Parsing for Quiz
            try:
                import re
                lines = [l.strip() for l in quiz_raw.split('\n') if l.strip()]
                q_text = ""
                options = []
                correct_letter = ""
                explanation = ""
                
                for line in lines:
                    line_lower = line.lower()
                    if line_lower.startswith("question:"):
                        q_text = line.split(":", 1)[1].strip()
                    # Match A: B: A) B) A. B. etc.
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
                    # Fallback if AI didn't use "Question:" label
                    q_text = lines[0]
                
                letter_to_index = {"A": 0, "B": 1, "C": 2, "D": 3}
                correct_id = letter_to_index.get(correct_letter if correct_letter else "A", 0)
                
                if q_text and len(options) >= 2:
                    print(f"Sending quiz for {selected_topic}...")
                    tg.send_poll(q_text, options[:10], correct_id, explanation)
                else:
                    print(f"Quiz parsing failed. Options found: {len(options)}. Raw: {quiz_raw[:50]}...")
            except Exception as quiz_err:
                print(f"Error processing quiz: {quiz_err}")
                
        else:
            status = resp.status_code if resp else "No Response"
            print(f"FAILED to send to Telegram: {status}")
        
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
