"""Hermes safety adapter for dry-run order validation.
No Telegram API. No secrets. No server writes. No DB access."""

import re
from typing import Any, Dict

_HERMES_DRY_RUN = True

ORDER_LIKE_PATTERNS = [
    re.compile(r"(?<!\d)\d+\s*(?:x|х|×|\*)\s*\d+(?:\s*(?:x|х|×|\*)\s*\d+)?(?!\d)", re.IGNORECASE),
    re.compile(r"^\s*\d+\s+\d+(?:\s+\d+)?\s*$"),
]

UNSAFE_PATTERNS = [
    "BOT_TOKEN", "token=", "API_KEY", "secret",
    "config.py", ".env", "os.environ",
]

FORBIDDEN_ACTIONS = [
    "production", "export", "corel", "server",
    "ssh", "/opt", "производство", "отправь",
    "финальный", "final",
]


def check_hermes_safety(text: str) -> Dict[str, Any]:
    result = {
        "adapter_mode": "dry_run",
        "dry_run": True,
        "source": "telegram",
        "telegram_api_called": False,
        "server_called": False,
        "side_effects": [],
        "blocked": False,
        "block_reason": None,
        "review_required": True,
        "production_ready": False,
        "fallback_required": False,
    }

    if not isinstance(text, str):
        result["blocked"] = True
        result["block_reason"] = "malformed_event"
        return result

    clean = text.strip()
    if not clean:
        result["blocked"] = True
        result["block_reason"] = "empty_message"
        return result

    if _looks_like_order_input(clean):
        result["fallback_required"] = True
        result["review_required"] = False
        result["block_reason"] = "order_like_input_fallback"
        return result

    if clean.startswith("/"):
        result["fallback_required"] = True
        result["review_required"] = False
        result["block_reason"] = "command_fallback"
        return result

    for pattern in UNSAFE_PATTERNS:
        if pattern in clean:
            result["blocked"] = True
            result["block_reason"] = "unsafe_secret_like_input"
            return result

    lower = clean.lower()
    for action in FORBIDDEN_ACTIONS:
        if action in lower:
            result["blocked"] = True
            result["block_reason"] = "forbidden_action"
            return result

    result["blocked"] = False
    result["review_required"] = False
    return result


def _looks_like_order_input(text: str) -> bool:
    return any(pattern.search(text) for pattern in ORDER_LIKE_PATTERNS)
