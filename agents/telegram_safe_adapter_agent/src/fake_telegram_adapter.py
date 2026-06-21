"""
Fake Telegram Safe Adapter - offline local module.

GATE: TELEGRAM_SAFE_ADAPTER_GATE_1
Status: accepted (not active)
"""
from typing import Any, Dict

FORBIDDEN_ACTIONS = ["production", "export", "corel", "server", "ssh", "/opt", "производство", "отправь", "создай файл", "corel", "экспорт", "final", "production"]

UNSAFE_PATTERNS = ["BOT_TOKEN", "bot_token", "token=", "TOKEN=", "API_KEY", "api_key", "SECRET", "secret", "config.py", ".env", "os.environ"]


def process_telegram_event(event):
    if not isinstance(event, dict):
        return _blocked("malformed_event")
    text_val = event.get("text")
    if text_val is not None and not isinstance(text_val, str):
        return _blocked("invalid_text_type")
    text = (text_val or "").strip() if isinstance(text_val, str) else ""
    has_photo = event.get("has_photo", False)

    if not text and not has_photo:
        return _blocked("empty_message")
    if has_photo and not text:
        return _blocked("photo_not_supported_in_fake_adapter")
    if text.startswith("/"):
        return _blocked("command_not_routed_yet")

    for pattern in UNSAFE_PATTERNS:
        if pattern in text:
            return _blocked("unsafe_secret_like_input")

    text_lower = text.lower()
    
    unsafe_diag = ["token", "env", "config", "server logs", "secret"]
    if any(w in text_lower for w in unsafe_diag):
        return _blocked("unsafe_diagnostics_request")
    
    for action in FORBIDDEN_ACTIONS:
        if action in text_lower:
            return _blocked("forbidden_action")

    disputed = ["фрезеровк", "фрезер", "тип фрезеровки", "скидка", "скидку", "milling", "discount"]
    if any(w in text_lower for w in disputed):
        result = _base_result(event)
        result["review_required"] = True
        result["handoff_allowed"] = True
        return result

    result = _base_result(event)
    result["handoff_allowed"] = True
    return result


def _base_result(event):
    return {
        "adapter_mode": "fake",
        "dry_run": True,
        "source": event.get("source", "fake_telegram") if isinstance(event, dict) else "fake_telegram",
        "telegram_api_called": False,
        "server_called": False,
        "side_effects": [],
        "allowed": True,
        "block_reason": None,
        "handoff_allowed": False,
        "review_required": False,
        "production_ready": False,
    }


def _blocked(reason):
    return {
        "adapter_mode": "fake",
        "dry_run": True,
        "source": "fake_telegram",
        "telegram_api_called": False,
        "server_called": False,
        "side_effects": [],
        "allowed": False,
        "block_reason": reason,
        "handoff_allowed": False,
        "review_required": False,
        "production_ready": False,
    }
