"""Safe adapter from raw order text to a Telegram-style reply."""

from malyarka_clean_core import build_order_result

from .messages import format_order_reply


def build_telegram_order_reply(order_text: str) -> str:
    """Return a Russian Telegram-style reply for an order text.

    This function intentionally does not import Telegram libraries, read tokens,
    read .env files, start polling, send messages or create Excel files.
    """
    result = build_order_result(order_text, source="telegram_skeleton")
    return format_order_reply(result)

