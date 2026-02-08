
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
- Keep the entire post UNDER 3000 characters to ensure it fits within Telegram's limits.
- Make it extremely practical for learners.
- Use bullet points and emojis to make it readable on mobile.
- Ensure all Markdown tags like backticks (```), bold (**), or italics (_) are properly closed.
- STRICT: Only use underscores (_) inside code blocks or properly closed italic tags. Never leave a single underscore hanging in plain text.
"""
    return base_prompt

def get_quiz_prompt(topic: str) -> str:
    """
    Generates a prompt for a cybersecurity quiz question.
    """
    return f"""
Topic: {topic}
Task: Create ONE challenging multiple-choice quiz question about this topic for a Telegram Quiz.

STRICT FORMAT:
Question: [The question text]
A: [Option 1]
B: [Option 2]
C: [Option 3]
D: [Option 4]
Correct: [Answer Letter, e.g., A]
Explanation: [Very brief explanation of why that's correct, max 1 sentence]

RULES:
- Keep the question clear and concise.
- Options must be plausible but only one correct.
- NO introductory or concluding text.
"""

TEXT_TEMPLATES = {
    "cyber_prompt": get_cyber_prompt,
    "quiz_prompt": get_quiz_prompt
}

IMAGE_TEMPLATES = {
    "default": "Cybersecurity abstract background, digital lock, matrix style, binary code, green and black, high tech, 4k"
}
