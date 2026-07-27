"""Telegram Intent Router — safe-local dry-run module.

Routes chat messages → intent detection → target module.
No Telegram API. No tokens. All mock.
"""

from hermes_core.telegram_intent.intent_contract import IntentResult, IntentType
from hermes_core.telegram_intent.intent_router import TelegramIntentRouter
from hermes_core.telegram_intent.order_detector import OrderDetectionResult, detect_order

__all__ = [
    "IntentResult",
    "IntentType",
    "OrderDetectionResult",
    "TelegramIntentRouter",
    "detect_order",
]
