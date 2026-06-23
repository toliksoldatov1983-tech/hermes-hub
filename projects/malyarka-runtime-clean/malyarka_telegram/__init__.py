"""Safe Telegram layer scaffold for the Malyarka project."""

from malyarka_telegram.intent import (
    IntentResult,
    classify_intent,
)

__all__ = [
    "IntentResult",
    "classify_intent",
]
