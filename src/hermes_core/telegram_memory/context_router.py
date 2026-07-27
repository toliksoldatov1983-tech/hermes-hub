"""Context-Aware Router — integrates session memory with intent detection.

Combines ConversationMemory + IntentRouter for full context-aware routing.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from hermes_core.telegram_intent import TelegramIntentRouter, IntentResult
from hermes_core.telegram_memory.conversation_memory import (
    ConversationSession,
    ConversationMode,
    ReplyExpectation,
)
from hermes_core.telegram_memory.memory_store import InMemoryMemoryStore, get_memory_store
from hermes_core.telegram_memory.order_draft import OrderDraft, OrderDraftStatus
from hermes_core.telegram_memory.draft_lifecycle import DraftLifecycle


@dataclass
class RoutedResponse:
    """Response from the context-aware router."""

    text: str = ""
    buttons: list[str] = field(default_factory=list)
    session_state: dict = field(default_factory=dict)
    draft_state: dict | None = None
    warnings: list[str] = field(default_factory=list)
    blocked_reason: str = ""
    next_step: str = ""
    audit_metadata: dict[str, Any] = field(default_factory=lambda: {
        "real_telegram_api": False,
        "token_used": False,
        "network_called": False,
        "safe_local": True,
    })

    def to_dict(self) -> dict:
        return {
            "text": self.text, "buttons": self.buttons,
            "session_state": self.session_state,
            "draft_state": self.draft_state,
            "warnings": self.warnings,
            "blocked_reason": self.blocked_reason,
            "next_step": self.next_step,
            "audit_metadata": self.audit_metadata,
        }


class ContextAwareRouter:
    """Routes messages considering session memory and draft state."""

    def __init__(self, store: InMemoryMemoryStore | None = None) -> None:
        self._intent_router = TelegramIntentRouter()
        self._store = store or get_memory_store()
        self._lifecycle = DraftLifecycle()

    def route(self, text: str, session_id: str = "dry-run-session-001") -> RoutedResponse:
        session = self._store.get_or_create(session_id)
        draft = self._lifecycle.get(session.active_order_draft_id) if session.has_active_draft else None

        # ── Detect intent with context ──
        context = session.context_dict()
        if draft:
            context["has_disputed_rows"] = draft.has_disputes

        intent: IntentResult = self._intent_router.detect(text, context=context)
        session.last_intent = intent.intent.value
        session.last_confidence = intent.confidence
        session.add_turn("user", text, intent.intent.value, intent.confidence)

        # ── Safety blocked ──
        if intent.is_blocked:
            return self._blocked_response(session, intent)

        # ── Route by intent ──
        intent_name = intent.intent.value

        if intent_name == "malyarka_order":
            return self._handle_order(session, draft, text, intent)
        elif intent_name == "malyarka_order_correction":
            return self._handle_correction(session, draft, text, intent)
        elif intent_name == "malyarka_order_confirmation":
            return self._handle_confirmation(session, draft, text, intent)
        elif intent_name in ("project_status", "daily_assistant", "what_next", "help"):
            return self._status_response(session, intent)
        elif intent_name == "general_chat":
            return self._general_chat_response(session, text)

        return self._general_chat_response(session, text)

    def _blocked_response(self, session: ConversationSession, intent: IntentResult) -> RoutedResponse:
        session.set_mode(ConversationMode.SAFETY_BLOCKED)
        session.add_turn("bot", intent.blocked_reason)
        return RoutedResponse(
            text=f"🚫 {intent.blocked_reason}",
            blocked_reason=intent.blocked_reason,
            session_state=session.to_dict(),
            next_step="Выберите безопасное действие.",
        )

    def _handle_order(self, session: ConversationSession, draft: OrderDraft | None, text: str, intent: IntentResult) -> RoutedResponse:
        # Create draft
        draft = self._lifecycle.parse_from_text(
            session.active_order_draft_id or f"draft-{len(self._lifecycle._drafts) + 1:03d}",
            text,
        )
        session.attach_draft(draft.draft_id)
        session.set_mode(ConversationMode.MALYARKA_ORDER)

        lines_preview = draft.preview_lines()
        resp_text = "📋 Черновик заказа:\n" + "\n".join(f"  {l}" for l in lines_preview)

        if draft.has_disputes:
            resp_text += f"\n\n⚠️ {len(draft.disputed_rows)} спорных строк."
            for q in draft.questions:
                resp_text += f"\n❓ {q}"
            resp_text += "\n\nУточни или исправь строки."
            buttons = ["✏️ Исправить", "❌ Отмена"]
        else:
            resp_text += "\n\n✅ Заказ готов. Подтвердить?"
            session.set_pending_question("Подтвердить заказ?", ReplyExpectation.CONFIRMATION)
            buttons = ["✅ Подтвердить", "✏️ Исправить", "❌ Отмена"]

        session.add_turn("bot", resp_text)

        return RoutedResponse(
            text=resp_text, buttons=buttons,
            session_state=session.to_dict(),
            draft_state=draft.to_dict(),
            next_step="Ответьте на вопрос.",
        )

    def _handle_correction(self, session: ConversationSession, draft: OrderDraft | None, text: str, intent: IntentResult) -> RoutedResponse:
        if not draft or not draft.has_disputes:
            return RoutedResponse(
                text="🤔 Нет активных спорных строк для исправления.",
                session_state=session.to_dict(),
                next_step="Отправьте заказ или обычный вопрос.",
            )

        # Apply correction to first disputed row
        self._lifecycle.correct(draft.draft_id, 0, text)
        session.set_mode(ConversationMode.MALYARKA_CORRECTION)

        if draft.has_disputes:
            resp_text = f"✏️ Исправление применено. Осталось {len(draft.disputed_rows)} спорных строк.\n"
            for q in draft.questions[1:]:
                resp_text += f"❓ {q}\n"
            buttons = ["✏️ Исправить дальше", "❌ Отмена"]
        else:
            resp_text = "✅ Исправление применено. Все строки подтверждены."
            draft.status = OrderDraftStatus.AWAITING_CONFIRMATION
            session.set_pending_question("Подтвердить заказ?", ReplyExpectation.CONFIRMATION)
            resp_text += "\n\nПодтвердить заказ?"
            buttons = ["✅ Подтвердить", "❌ Отмена"]

        session.add_turn("bot", resp_text)

        return RoutedResponse(
            text=resp_text, buttons=buttons,
            session_state=session.to_dict(),
            draft_state=draft.to_dict(),
            next_step="Ответьте на вопрос.",
        )

    def _handle_confirmation(self, session: ConversationSession, draft: OrderDraft | None, text: str, intent: IntentResult) -> RoutedResponse:
        if not draft:
            return RoutedResponse(
                text="🤔 Нет активного черновика для подтверждения.",
                session_state=session.to_dict(),
                next_step="Отправьте заказ.",
            )

        if draft.has_disputes:
            draft.status = OrderDraftStatus.HAS_DISPUTES
            session.set_mode(ConversationMode.AWAITING_CLARIFICATION)
            resp_text = f"⚠️ Нельзя подтвердить — есть {len(draft.disputed_rows)} спорных строк.\nИсправь их сначала."
            buttons = ["✏️ Исправить", "❌ Отмена"]
        else:
            self._lifecycle.confirm(draft.draft_id)
            session.set_mode(ConversationMode.MALYARKA_ORDER)
            resp_text = "✅ Заказ подтверждён (dry-run).\nФинальный export-файл пока не создаётся."
            buttons = ["📋 Показать черновик", "🔄 Новый заказ"]

        session.add_turn("bot", resp_text)

        return RoutedResponse(
            text=resp_text, buttons=buttons,
            session_state=session.to_dict(),
            draft_state=draft.to_dict(),
            next_step="Продолжайте.",
        )

    def _status_response(self, session: ConversationSession, intent: IntentResult) -> RoutedResponse:
        resp_text = f"📊 {intent.reason}\nRoute: {intent.route_target}"
        session.set_mode(ConversationMode.PROJECT_STATUS)
        session.add_turn("bot", resp_text)
        return RoutedResponse(
            text=resp_text, session_state=session.to_dict(),
            next_step="Выберите действие.",
        )

    def _general_chat_response(self, session: ConversationSession, text: str) -> RoutedResponse:
        session.set_mode(ConversationMode.GENERAL_CHAT)
        resp_text = f"💬 Mock assistant: получено '{text[:60]}'\nLive AI disabled. Используется mock provider."
        session.add_turn("bot", resp_text)
        return RoutedResponse(
            text=resp_text, session_state=session.to_dict(),
            next_step="Задайте вопрос или отправьте заказ.",
        )
