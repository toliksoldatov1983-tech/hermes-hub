"""Safe Telegram mode router.

This module is intentionally detached from the live Telegram app and handlers.
It does not start polling, call AI providers, read environment variables, or
touch databases.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from malyarka_telegram.access import is_owner, is_owner_id_configured
from malyarka_telegram.intent import classify_intent
from malyarka_telegram.messages import (
    format_access_denied_message,
    format_admin_diagnostics_message,
    format_engineer_mode_message,
    format_engineer_task_card_message,
    format_ideas_mode_message,
)
from malyarka_telegram.modes import TelegramMode, mode_from_command
from malyarka_telegram.session import InMemoryModeSessionStore


ORDER_LIKE_PATTERN = re.compile(
    r"(?<!\d)\d+(?:\s*[*xхXХ×]\s*|\s+)\d+(?:\s*[*xхXХ×]\s*|\s+)?\d*(?!\d)"
)

MODE_SWITCH_MESSAGES: dict[TelegramMode, str] = {
    TelegramMode.ORDER: "Включён режим заказа. Пришлите размеры.",
    TelegramMode.CHAT: "Включён режим чата. Можно обсуждать идеи и вопросы.",
    TelegramMode.ENGINEER: "Инженер проекта включён.",
    TelegramMode.IDEAS: "Режим идей включён.",
    TelegramMode.ADMIN: "Админ-диагностика включена.",
    TelegramMode.SUMMARY: "Включён режим выжимки. Пришлите текст идеи или разговора.",
    TelegramMode.RULES: "Включён режим правил. Напишите, какое правило проверить.",
}

OWNER_ONLY_MODES = {
    TelegramMode.ENGINEER,
    TelegramMode.IDEAS,
    TelegramMode.ADMIN,
}


@dataclass(frozen=True)
class TelegramRouteResult:
    mode: TelegramMode
    action: str
    message: str
    should_parse_order: bool = False
    should_call_ai: bool = False
    should_change_code: bool = False
    should_use_rules: bool = False
    should_make_summary: bool = False


def route_telegram_text(
    *,
    user_id: int,
    text: str | None,
    session_store: InMemoryModeSessionStore,
    owner_id: int | None = None,
) -> TelegramRouteResult:
    """Route text according to the user's current safe Telegram mode."""

    safe_text = "" if text is None else text.strip()

    if safe_text.lower() in {"/start", "start", "старт", "меню", "отмена"}:
        mode = session_store.reset_mode(user_id)
        return TelegramRouteResult(
            mode=mode,
            action="show_neutral_menu",
            message="Выберите режим: 🧾 Новый заказ, 🛠 Инженер проекта или 💬 Идеи / разговор.",
        )

    command_mode = mode_from_command(safe_text)
    if command_mode is not None:
        if command_mode in OWNER_ONLY_MODES and not is_owner(user_id, owner_id):
            return TelegramRouteResult(
                mode=session_store.get_mode(user_id),
                action="access_denied",
                message=format_access_denied_message(),
            )
        mode = session_store.set_mode(user_id, command_mode)
        message = MODE_SWITCH_MESSAGES[mode]
        if mode == TelegramMode.ENGINEER:
            message = format_engineer_mode_message()
        elif mode == TelegramMode.IDEAS:
            message = format_ideas_mode_message()
        elif mode == TelegramMode.ADMIN:
            message = format_admin_diagnostics_message(
                current_mode=mode.value,
                owner_id_configured=is_owner_id_configured(owner_id),
                polling_started=False,
            )
        return TelegramRouteResult(
            mode=mode,
            action="switch_mode",
            message=message,
        )

    mode = session_store.get_mode(user_id)
    if mode == TelegramMode.NEUTRAL:
        if looks_like_order_text(safe_text):
            mode = session_store.set_mode(user_id, TelegramMode.ORDER)
            return TelegramRouteResult(
                mode=mode,
                action="parse_order",
                message="Текст будет обработан как заказ.",
                should_parse_order=True,
            )
        return _route_neutral_text(safe_text)
    if mode == TelegramMode.ORDER:
        return TelegramRouteResult(
            mode=mode,
            action="parse_order",
            message="Текст будет обработан как заказ.",
            should_parse_order=True,
        )
    if mode == TelegramMode.CHAT:
        if looks_like_order_text(safe_text):
            message = "Похоже на заказ. Перейдите в /заказ, если хотите разобрать размеры."
        else:
            message = "Текст принят как разговор. AI на этом этапе не вызывается."
        return TelegramRouteResult(mode=mode, action="chat_placeholder", message=message)
    if mode == TelegramMode.ENGINEER:
        return TelegramRouteResult(
            mode=mode,
            action="engineer_task_card",
            message=format_engineer_task_card_message(safe_text),
        )
    if mode == TelegramMode.IDEAS:
        return TelegramRouteResult(
            mode=mode,
            action="ideas_placeholder",
            message=format_ideas_mode_message(),
        )
    if mode == TelegramMode.ADMIN:
        return TelegramRouteResult(
            mode=mode,
            action="admin_diagnostics",
            message=format_admin_diagnostics_message(
                current_mode=mode.value,
                owner_id_configured=is_owner_id_configured(owner_id),
                polling_started=False,
            ),
        )
    if mode == TelegramMode.SUMMARY:
        return TelegramRouteResult(
            mode=mode,
            action="summary_placeholder",
            message="Текст можно использовать для подготовки выжимки.",
            should_make_summary=True,
        )
    if mode == TelegramMode.RULES:
        return TelegramRouteResult(
            mode=mode,
            action="rules_placeholder",
            message="Текст можно использовать для поиска или объяснения правила.",
            should_use_rules=True,
        )

    return _route_neutral_text(safe_text)


def looks_like_order_text(text: str | None) -> bool:
    if not text:
        return False
    return bool(ORDER_LIKE_PATTERN.search(text))


def _route_neutral_text(text: str) -> TelegramRouteResult:
    """Route free text in neutral mode using local intent recognition.

    Uses classify_intent() from the intent module — a local signature-based
    classifier with no external AI/API calls, no .env reads, no database access.
    """
    result = classify_intent(text)

    # --- Blocked (dangerous content detected) ---
    if result.blocked:
        return TelegramRouteResult(
            mode=TelegramMode.NEUTRAL,
            action="blocked",
            message=result.block_message or "⚠️ Запрос заблокирован по соображениям безопасности.",
        )

    # --- Unknown / needs clarification ---
    if result.is_unknown():
        return TelegramRouteResult(
            mode=TelegramMode.NEUTRAL,
            action="clarify_intent",
            message=result.clarify_question or (
                "Я не совсем понял, что вы хотите сделать. Выберите:\n\n"
                "🧾 Новый заказ\n"
                "💬 Идея / обсуждение\n"
                "🛠 Инженер проекта\n"
                "← Отмена"
            ),
        )

    # --- Order intent ---
    if result.is_order():
        return TelegramRouteResult(
            mode=TelegramMode.NEUTRAL,
            action="suggest_order_mode",
            message="Похоже на заказ. Перейдите в /заказ, чтобы разобрать размеры.",
        )

    # --- Ideas intent ---
    if result.is_ideas():
        return TelegramRouteResult(
            mode=TelegramMode.NEUTRAL,
            action="suggest_ideas_mode",
            message="Похоже, у вас есть идея или предложение. Перейдите в /идеи, чтобы обсудить.",
        )

    # --- Engineer intent ---
    if result.is_engineer():
        return TelegramRouteResult(
            mode=TelegramMode.NEUTRAL,
            action="suggest_engineer_mode",
            message="Похоже, вы хотите проверить статус проекта. Перейдите в /инженер.",
        )

    # --- Admin intent — always clarify (never auto-route to hidden mode) ---
    if result.is_admin():
        return TelegramRouteResult(
            mode=TelegramMode.NEUTRAL,
            action="clarify_intent",
            message=result.clarify_question or (
                "Я не совсем понял, что вы хотите сделать. Выберите:\n\n"
                "🧾 Новый заказ\n"
                "💬 Идея / обсуждение\n"
                "🛠 Инженер проекта\n"
                "← Отмена"
            ),
        )

    # Fallback — should never reach here
    return TelegramRouteResult(
        mode=TelegramMode.NEUTRAL,
        action="choose_mode",
        message="Выберите режим: 🧾 Новый заказ, 🛠 Инженер проекта или 💬 Идеи / разговор.",
    )
