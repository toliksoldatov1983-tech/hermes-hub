"""Telegram Intent Router — dry-run intent detection for chat messages.

Detects: general_chat, malyarka_order, corrections, confirmations, safety-sensitive.
All mock. No Telegram API. No tokens.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any


class IntentType(Enum):
    """Detected intent from a user message."""

    GENERAL_CHAT = "general_chat"
    MALYARKA_ORDER = "malyarka_order"
    MALYARKA_ORDER_CORRECTION = "malyarka_order_correction"
    MALYARKA_ORDER_CONFIRMATION = "malyarka_order_confirmation"
    PROJECT_STATUS = "project_status"
    DAILY_ASSISTANT = "daily_assistant"
    WHAT_NEXT = "what_next"
    HELP = "help"
    SAFETY_SENSITIVE = "safety_sensitive"
    UNKNOWN = "unknown"


@dataclass
class IntentResult:
    """Result of intent detection."""

    intent: IntentType
    confidence: float  # 0.0 — 1.0
    reason: str = ""
    safe_local: bool = True
    requires_confirmation: bool = False
    requires_clarification: bool = False
    suggested_question: str = ""
    route_target: str = ""  # module/command to route to
    blocked_reason: str = ""
    audit_metadata: dict[str, Any] = field(default_factory=lambda: {
        "router_version": "1.0",
        "real_telegram_api": False,
        "token_used": False,
        "env_read": False,
        "network_called": False,
        "live_send": False,
    })

    @property
    def is_confident(self) -> bool:
        return self.confidence >= 0.7

    @property
    def needs_clarification(self) -> bool:
        return self.requires_clarification or (0.3 <= self.confidence < 0.7)

    @property
    def is_blocked(self) -> bool:
        return bool(self.blocked_reason)

    def to_dict(self) -> dict[str, Any]:
        return {
            "intent": self.intent.value,
            "confidence": self.confidence,
            "reason": self.reason,
            "safe_local": self.safe_local,
            "requires_confirmation": self.requires_confirmation,
            "requires_clarification": self.requires_clarification,
            "suggested_question": self.suggested_question,
            "route_target": self.route_target,
            "blocked_reason": self.blocked_reason,
            "audit_metadata": self.audit_metadata,
        }

    @staticmethod
    def general_chat(reason: str = "") -> IntentResult:
        return IntentResult(
            intent=IntentType.GENERAL_CHAT,
            confidence=0.95,
            reason=reason or "Обычный вопрос/чат.",
            route_target="assistant",
            requires_clarification=False,
        )

    @staticmethod
    def malyarka_order(confidence: float, reason: str = "") -> IntentResult:
        needs_clar = confidence < 0.7
        return IntentResult(
            intent=IntentType.MALYARKA_ORDER,
            confidence=confidence,
            reason=reason,
            route_target="malyarka",
            requires_clarification=needs_clar,
            suggested_question=(
                "Похоже на заказ для Малярки. Разобрать как заказ?"
                if needs_clar else ""
            ),
        )

    @staticmethod
    def blocked(intent: IntentType, reason: str) -> IntentResult:
        return IntentResult(
            intent=intent,
            confidence=1.0,
            reason=reason,
            route_target="blocked",
            blocked_reason=reason,
        )
