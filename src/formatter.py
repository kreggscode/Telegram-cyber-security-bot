"""
Formatter Engine for Telegram Messages.
Converts Markdown to rock-solid Telegram HTML, handles code blocks,
syntax highlighting, interactive Copy buttons, hyperlinks, and edge cases.
"""

import html
import re


def markdown_to_telegram_html(text: str) -> str:
    """
    Convert Markdown content to clean, fully-compliant Telegram HTML.
    Supports code blocks with syntax highlighting and Copy button,
    inline code, bold, italics, hyperlinks, and blockquotes.
    """
    if not text:
        return ""

    text = text.replace("\r\n", "\n")

    # Auto-close unclosed code blocks if AI output was cut off
    if text.count("```") % 2 != 0:
        text += "\n```"

    code_blocks = []
    def save_code_block(match):
        lang = (match.group(1) or "").strip().lower()
        code = match.group(2)
        escaped_code = html.escape(code.strip("\n"), quote=False)
        if lang:
            replacement = f'<pre><code class="language-{lang}">{escaped_code}</code></pre>'
        else:
            replacement = f'<pre><code>{escaped_code}</code></pre>'
        placeholder = f"TOKENXCODEBLOCKX{len(code_blocks)}XTOKEN"
        code_blocks.append(replacement)
        return f"\n{placeholder}\n"

    text = re.sub(r"```([a-zA-Z0-9_\-+]*)\n?(.*?)```", save_code_block, text, flags=re.DOTALL)

    inline_codes = []
    def save_inline_code(match):
        code = match.group(1)
        escaped_code = html.escape(code, quote=False)
        placeholder = f"TOKENXINLINEX{len(inline_codes)}XTOKEN"
        inline_codes.append(f"<code>{escaped_code}</code>")
        return placeholder

    text = re.sub(r"`([^`\n]+)`", save_inline_code, text)

    def quote_repl(match):
        lines = [
            line.strip()[2:].strip() if line.strip().startswith("> ") else line.strip()[1:].strip()
            for line in match.group(0).split("\n")
            if line.strip()
        ]
        return f"<blockquote>{chr(10).join(lines)}</blockquote>"
    
    text = re.sub(r"(?:^[ \t]*>[^\n]*(?:\n|$))+", quote_repl, text, flags=re.MULTILINE)

    blockquotes = []
    def save_quote(match):
        placeholder = f"TOKENXBLOCKQUOTEX{len(blockquotes)}XTOKEN"
        blockquotes.append(match.group(0))
        return placeholder

    text = re.sub(r"<blockquote>.*?</blockquote>", save_quote, text, flags=re.DOTALL)

    text = html.escape(text, quote=False)

    def link_repl(match):
        label = match.group(1).strip()
        url = match.group(2).strip()
        safe_url = url.replace('"', "%22")
        return f'<a href="{safe_url}">{label}</a>'

    text = re.sub(r"\[([^\]]+)\]\((https?://[^\s\)]+|t\.me/[^\s\)]+)\)", link_repl, text)
    text = re.sub(r"^(?:#{1,4})\s+(.+)$", r"<b>\1</b>", text, flags=re.MULTILINE)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text, flags=re.DOTALL)
    text = re.sub(r"__(.+?)__", r"<b>\1</b>", text, flags=re.DOTALL)
    text = re.sub(r"(?<!\*)\*([^\*\n]+)\*(?!\*)", r"<i>\1</i>", text)

    for i, replacement in enumerate(blockquotes):
        text = text.replace(f"TOKENXBLOCKQUOTEX{i}XTOKEN", replacement)

    for i, replacement in enumerate(inline_codes):
        text = text.replace(f"TOKENXINLINEX{i}XTOKEN", replacement)

    for i, replacement in enumerate(code_blocks):
        text = text.replace(f"TOKENXCODEBLOCKX{i}XTOKEN", replacement)

    return re.sub(r"\n{3,}", "\n\n", text).strip()


def plain_text_fallback_formatter(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"\[([^\]]+)\]\((https?://[^\s\)]+|t\.me/[^\s\)]+)\)", r"\1: \2", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"__(.+?)__", r"\1", text)
    text = re.sub(r"(?<!\*)\*([^\*\n]+)\*(?!\*)", r"\1", text)
    text = re.sub(r"^(?:#{1,4})\s+(.+)$", r"\1", text, flags=re.MULTILINE)
    text = re.sub(r"^[ \t]*>[ \t]?", "", text, flags=re.MULTILINE)
    return text.strip()


def safe_truncate_html(text: str, max_chars: int = 4000) -> str:
    if len(text) <= max_chars:
        return text
    trimmed = text[:max_chars - 20]
    last_space = max(trimmed.rfind(" "), trimmed.rfind("\n"))
    if last_space > 0:
        trimmed = trimmed[:last_space]
    trimmed += "..."
    for tag in ["code", "pre", "b", "i", "blockquote", "a"]:
        if trimmed.count(f"<{tag}") > trimmed.count(f"</{tag}>"):
            trimmed += f"</{tag}>"
    return trimmed
