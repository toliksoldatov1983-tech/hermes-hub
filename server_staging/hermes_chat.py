"""Hermes chat with self-healing tools."""

from __future__ import annotations

import os, json, urllib.request, urllib.error, re
from pathlib import Path
from datetime import datetime, timezone
from malyarka_core.self_heal import read_file, fix_file, restart_bot, health_check

HUB_PATH = Path("/opt/hermes-hub")
BOT_LOG_PATH = Path("/opt/hermes-hub-bot-logs/chat.md")

HERMES_SYSTEM_PROMPT = (
    "Ты Hermes — помощник. Отвечай на русском, коротко. "
    "У тебя есть инструменты для исправления кода бота на сервере. "
    "Если нужно прочитать файл — напиши в ответе: [TOOL:read_file|путь] "
    "Если нужно исправить — напиши: [TOOL:fix_file|путь|старый_текст|новый_текст] "
    "Если нужно перезапустить бота: [TOOL:restart_bot] "
    "Проверить статус: [TOOL:health_check] "
    "Можно использовать несколько инструментов в одном ответе. "
    "После инструментов объясни что сделано. "
    "Пути: malyarka_telegram/app.py, malyarka_telegram/router.py, malyarka_telegram/handlers.py, "
    "malyarka_core/parsing.py, malyarka_core/economy.py, malyarka_vision/openai_vision.py."
)

DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_MODEL = "deepseek-v4-pro"

_CONTEXT_FILES = [
    "CURRENT_SESSION_CONTEXT.md", "WHAT_NEXT.md",
    "TASK_QUEUE.md", "sync/SHARED_CURRENT_STATUS.md",
]

_TOOL_RE = re.compile(r'\[TOOL:(\w+)(?:\|(.*?))?\]', re.DOTALL)

def _read_context() -> str:
    lines = ["Текущий контекст:"]
    for rel in _CONTEXT_FILES:
        fp = HUB_PATH / rel
        if fp.exists():
            lines.append(f"\n--- {rel} ---\n{fp.read_text(encoding='utf-8')[:2000]}")
    if BOT_LOG_PATH.exists():
        lines.append(f"\n--- Последние разговоры ---\n{BOT_LOG_PATH.read_text(encoding='utf-8')[-2000:]}")
    return "\n".join(lines)

def _save_to_log(user_text: str, answer: str) -> None:
    try:
        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
        with open(BOT_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"\n### {now}\n**П:** {user_text[:300]}\n**H:** {answer[:500]}\n")
    except Exception:
        pass

def _call_deepseek(messages: list) -> str:
    api_key = os.environ.get("DEEPSEEK_API_KEY", "")
    if not api_key:
        return "Hermes недоступен."
    data = json.dumps({"model": DEEPSEEK_MODEL, "messages": messages}).encode()
    req = urllib.request.Request(DEEPSEEK_API_URL, data=data, headers={
        "Authorization": f"Bearer {api_key}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())["choices"][0]["message"]["content"]

def _execute_tools(text: str) -> str:
    """Find and execute [TOOL:...] commands, return results."""
    results = []
    for m in _TOOL_RE.finditer(text):
        name = m.group(1)
        args_str = m.group(2) or ""
        args = [a.strip() for a in args_str.split("|")]
        try:
            if name == "read_file" and args:
                res = read_file(args[0])
                results.append(f"[{name}] {args[0]}:\n{res[:2000]}")
            elif name == "fix_file" and len(args) >= 3:
                res = fix_file(args[0], args[1], args[2])
                results.append(f"[{name}] {res}")
            elif name == "restart_bot":
                res = restart_bot()
                results.append(f"[{name}] {res}")
            elif name == "health_check":
                res = health_check()
                results.append(f"[{name}] {res}")
        except Exception as e:
            results.append(f"[{name}] Ошибка: {e}")
    return "\n".join(results) if results else ""

def ask_hermes(user_text: str) -> str:
    context = _read_context()
    system = f"{HERMES_SYSTEM_PROMPT}\n\n{context}"
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user_text},
    ]
    try:
        answer = _call_deepseek(messages)
        tool_results = _execute_tools(answer)
        if tool_results:
            messages.append({"role": "assistant", "content": answer})
            messages.append({"role": "user", "content": f"Результаты:\n{tool_results}\nОтветь кратко что сделано."})
            answer = _call_deepseek(messages)
        _save_to_log(user_text, answer)
        return answer
    except Exception as e:
        return f"Hermes недоступен: {e}"
