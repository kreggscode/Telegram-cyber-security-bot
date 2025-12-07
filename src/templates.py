
def get_cyber_prompt(topic: str) -> str:
    """
    Generates a prompt for a cybersecurity topic.
    """
    base_prompt = f"""
You are an expert Cybersecurity Researcher and Bug Bounty Hunter.
Topic: {topic}

Your task is to create a detailed, educational Telegram post about this topic.

The post MUST include the following structure:
1. **Headline**: Engaging title with emojis (e.g., 🛡️ XSS Attack Vector 🛡️).
2. **Explanation**: A clear, concise explanation of the vulnerability or concept (max 3 sentences).
3. **⚠️ Code Snippet ⚠️**: 
   - PROVIDE A REALISTIC CODE SNIPPET (in Python, JavaScript, PHP, or HTML) that demonstrates the vulnerability OR the fix. 
   - Wrap the code in specific language markdown (e.g., ```javascript ... ```). 
   - The snippet should be educational.
4. **🐞 Bug Bounty Tip**: A practical tip for finding this bug in the wild (e.g., "Check hidden input fields for...").
5. **Mitigation**: How developers can fix this.

IMPORTANT:
- DO NOT be repetitive.
- Make it extremely practical for learners.
- Use bullet points and emojis to make it readable on mobile.
"""
    return base_prompt

TEXT_TEMPLATES = {
    "cyber_prompt": get_cyber_prompt
}

IMAGE_TEMPLATES = {
    "default": "Cybersecurity abstract background, digital lock, matrix style, binary code, green and black, high tech, 4k"
}
