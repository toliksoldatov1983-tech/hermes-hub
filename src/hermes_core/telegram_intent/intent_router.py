"""Telegram Intent Router — routes chat messages to target modules.

Determines intent, context, and routes to Malyarka / Assistant / Status.
All dry-run. No Telegram API.
"""

from __future__ import annotations

from hermes_core.telegram_intent.intent_contract import IntentResult, IntentType
from hermes_core.telegram_intent.order_detector import detect_order, OrderDetectionResult


class TelegramIntentRouter:
    """Routes Telegram chat messages to intent-aware targets.

    Dry-run only. No live Telegram. No tokens.
    """

    def detect(self, text: str, context: dict | None = None) -> IntentResult:
        """Detect intent from a chat message with optional context."""
        context = context or {}
        text_lower = text.lower().strip()

        # ── Safety-sensitive check ──
        safety = self._check_safety(text_lower)
        if safety is not None:
            return safety

        # ── Explicit commands ──
        if text_lower in ("/status", "/статус", "статус", "status"):
            return IntentResult(
                intent=IntentType.PROJECT_STATUS,
                confidence=1.0,
                reason="Явный запрос статуса.",
                route_target="project-status",
            )
        if text_lower in ("/assistant", "/ассистент", "ассистент", "daily assistant"):
            return IntentResult(
                intent=IntentType.DAILY_ASSISTANT,
                confidence=1.0,
                reason="Явный запрос daily assistant.",
                route_target="daily-assistant",
            )
        if text_lower in ("/help", "/помощь", "помощь", "help", "команды"):
            return IntentResult(
                intent=IntentType.HELP,
                confidence=1.0,
                reason="Запрос помощи.",
                route_target="help-local",
            )

        # ── What next ──
        if any(w in text_lower for w in ("что дальше", "следующий шаг", "next", "what next")):
            return IntentResult(
                intent=IntentType.WHAT_NEXT,
                confidence=0.9,
                reason="Запрос следующих шагов.",
                route_target="what-next",
            )

        # ── Context-aware routing ──
        last_intent = context.get("last_intent", "")
        has_draft = context.get("has_draft_order", False)
        has_disputes = context.get("has_disputed_rows", False)
        awaiting_confirmation = context.get("awaiting_confirmation", False)

        # ── Order detection ──
        order_result = detect_order(text)

        if order_result.is_correction and (has_draft or has_disputes):
            return IntentResult(
                intent=IntentType.MALYARKA_ORDER_CORRECTION,
                confidence=0.85,
                reason=order_result.reason,
                route_target="malyarka",
                requires_clarification=False,
                suggested_question="",
            )

        if order_result.is_confirmation:
            if awaiting_confirmation:
                return IntentResult(
                    intent=IntentType.MALYARKA_ORDER_CONFIRMATION,
                    confidence=0.9,
                    reason=order_result.reason,
                    route_target="malyarka",
                )
            # A bare confirmation without an active question is not a new
            # order. Let the normal chat fallback explain the missing context.
            return IntentResult.general_chat()

        if order_result.is_order:
            if order_result.confidence >= 0.7:
                return IntentResult.malyarka_order(order_result.confidence, order_result.reason)
            elif order_result.confidence >= 0.3:
                return IntentResult.malyarka_order(
                    order_result.confidence,
                    order_result.reason + " Нужно уточнение.",
                )
            # Low confidence — treat as general chat with a hint
            return IntentResult(
                intent=IntentType.MALYARKA_ORDER,
                confidence=order_result.confidence,
                reason=order_result.reason,
                route_target="malyarka",
                requires_clarification=True,
                suggested_question="Похоже на заказ для Малярки. Разобрать как заказ?",
            )

        # ── Default: general chat ──
        return IntentResult.general_chat()

    def _check_safety(self, text: str) -> IntentResult | None:
        """Check for safety-sensitive content. Returns blocked result or None."""
        blocked_phrases = [
            ("telegram token", "Telegram token не читается. Live Telegram disabled."),
            (".env", ".env не читается. Safe-local mode."),
            ("api key", "API ключи не читаются."),
            ("google drive", "Google Drive write заблокирован."),
            ("delete", "Удаление файлов заблокировано."),
            ("gemini", "Gemini disabled. Используется mock provider."),
            ("deepseek", "DeepSeek disabled. Используется mock provider."),
            ("live", "Live-функции заблокированы."),
        ]

        for phrase, reason in blocked_phrases:
            if phrase in text:
                return IntentResult.blocked(IntentType.SAFETY_SENSITIVE, reason)

        return None
