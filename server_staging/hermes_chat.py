"""Hermes chat: send user text to DeepSeek with project context, save conversation log."""

from __future__ import annotations

import os
import json
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime, timezone

HUB_PATH = Path("/opt/hermes-hub")
BOT_LOG_PATH = Path("/opt/hermes-hub-bot-logs/chat.md")

HERMES_SYSTEM_PROMPT = (
    "Ты Hermes — главный помощник пользователя. "
    "Отвечай на русском, коротко, по делу. "
    "Помогай думать, планировать, принимать решения. "
    "Ты общаешься с пользователем через Telegram. "
    "Не читай секреты, не меняй код, не трогай сервер без явной команды."
)

DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_MODEL = "deepseek-v4-pro"

_CONTEXT_FILES = [
    "CURRENT_SESSION_CONTEXT.md",
    "WHAT_NEXT.md",
    "TASK_QUEUE.md",
    "sync/SHARED_CURRENT_STATUS.md",
]


def _read_context() -> str:
    """Read current project state from Hub files."""
    lines = ["Текущий контекст проекта:"]
    for rel in _CONTEXT_FILES:
        fp = HUB_PATH / rel
        if fp.exists():
            content = fp.read_text(encoding="utf-8")[:2000]
            lines.append(f"\n--- {rel} ---\n{content}")
    if BOT_LOG_PATH.exists():
        recent = BOT_LOG_PATH.read_text(encoding="utf-8")[-3000:]
        lines.append(f"\n--- Последние разговоры в боте ---\n{recent}")
    return "\n".join(lines)


def _save_to_log(user_text: str, hermes_answer: str) -> None:
    """Append conversation to log file."""
    try:
        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
        entry = f"\n### {now}\n**Пользователь:** {user_text[:300]}\n**Hermes:** {hermes_answer[:500]}\n"
        with open(BOT_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(entry)
    except Exception:
        pass  # silently ignore log errors


def ask_hermes(user_text: str) -> str:
    """Send user text to DeepSeek with project context and return response."""

    api_key = os.environ.get("DEEPSEEK_API_KEY", "")
    if not api_key:
        return "Hermes сейчас недоступен (нет ключа API)."

    context = _read_context()
    full_prompt = f"{HERMES_SYSTEM_PROMPT}\n\n{context}"

    try:
        data = json.dumps({
            "model": DEEPSEEK_MODEL,
            "messages": [
                {"role": "system", "content": full_prompt},
                {"role": "user", "content": user_text},
            ],
        }).encode("utf-8")

        req = urllib.request.Request(
            DEEPSEEK_API_URL,
            data=data,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
        )

        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            answer = body["choices"][0]["message"]["content"]

        _save_to_log(user_text, answer)
        return answer

    except Exception as e:
        return f"Hermes сейчас недоступен: {e}"
