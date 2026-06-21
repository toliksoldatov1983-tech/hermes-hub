"""Hermes chat: send user text to DeepSeek with current project context."""

from __future__ import annotations

import os
import json
import urllib.request
import urllib.error
from pathlib import Path

HUB_PATH = Path("/opt/hermes-hub")

HERMES_SYSTEM_PROMPT = (
    "Ты Hermes — главный помощник пользователя. "
    "Отвечай на русском, коротко, по делу. "
    "Помогай думать, планировать, принимать решения. "
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
    return "\n".join(lines)


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
            return body["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Hermes сейчас недоступен: {e}"
