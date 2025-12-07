import urllib.parse
import requests
import random
import time
from datetime import datetime


def generate_text(prompt: str) -> str:
    """Generate free-form text from Pollinations.ai with randomization for variety."""
    # Add randomization to ensure unique content every day
    seed = random.randint(1000, 999999)
    timestamp = int(time.time())
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    # Enhance prompt with context to ensure variety
    enhanced_prompt = f"{prompt}\n\nIMPORTANT: Make this unique and different. Today's date: {date_str}. Generate fresh, original content not seen before. Seed: {seed}"
    
    encoded = urllib.parse.quote(enhanced_prompt)
    # Add seed parameter to URL for additional randomization
    url = f"https://text.pollinations.ai/{encoded}?seed={seed}&timestamp={timestamp}"
    
    resp = requests.get(url, timeout=30)
    if resp.status_code == 200:
        return resp.text.strip()
    return "AI generation failed. Please try again."


def image_url(prompt: str) -> str:
    """Return an image URL from Pollinations based on prompt with randomization."""
    seed = random.randint(1000, 999999)
    encoded = urllib.parse.quote(prompt)
    # Add seed for image variety
    return f"https://image.pollinations.ai/prompt/{encoded}?seed={seed}"
