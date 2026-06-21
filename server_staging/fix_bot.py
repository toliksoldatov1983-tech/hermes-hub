#!/usr/bin/env python3
"""Re-apply all Hermes chat changes to the Telegram bot."""

import sys

BASE = "/opt/malyarka-telegram-bot"

# 1. Fix router.py
with open(f"{BASE}/malyarka_telegram/router.py") as f:
    c = f.read()

# Add import
c = c.replace(
    "from malyarka_telegram.modes import TelegramMode, mode_from_command",
    "from malyarka_telegram.modes import TelegramMode, mode_from_command\nfrom malyarka_core.hermes_chat import ask_hermes"
)

# Disable start menu
old_menu = 'if safe_text.lower() in {"/start", "start", "старт", "меню", "отмена"}:'
c = c.replace(old_menu, "if False:  # menu disabled")

# CHAT mode: non-order -> Hermes
old_chat_placeholder = 'message = "Текст принят как разговор. AI на этом этапе не вызывается."'
c = c.replace(old_chat_placeholder, "message = ask_hermes(safe_text)")

# CHAT mode: order-like -> parse
old_order_suggest = 'message = "Похоже на заказ. Перейдите в /заказ, если хотите разобрать размеры."\n        return TelegramRouteResult(mode=mode, action="chat_placeholder", message=message)'
new_order_parse = 'return TelegramRouteResult(mode=mode, action="parse_order", message="", should_parse_order=True)'
c = c.replace(old_order_suggest, new_order_parse)

# NEUTRAL mode -> CHAT-like
old_neutral = "if mode == TelegramMode.NEUTRAL:\n        return _route_neutral_text(safe_text)"
new_neutral = (
    "if mode == TelegramMode.NEUTRAL:\n"
    "        if looks_like_order_text(safe_text):\n"
    '            return TelegramRouteResult(mode=mode, action="parse_order", message="", should_parse_order=True)\n'
    "        else:\n"
    "            message = ask_hermes(safe_text)\n"
    '            return TelegramRouteResult(mode=mode, action="hermes_chat", message=message)'
)
c = c.replace(old_neutral, new_neutral)

with open(f"{BASE}/malyarka_telegram/router.py", "w") as f:
    f.write(c)

# 2. Fix session.py default to CHAT
with open(f"{BASE}/malyarka_telegram/session.py") as f:
    s = f.read()
s = s.replace("TelegramMode.NEUTRAL", "TelegramMode.CHAT")
with open(f"{BASE}/malyarka_telegram/session.py", "w") as f:
    f.write(s)

print("ALL FIXES APPLIED")
