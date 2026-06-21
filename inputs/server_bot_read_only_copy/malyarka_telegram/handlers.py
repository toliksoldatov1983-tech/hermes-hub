"""Pure message handlers for the first safe Telegram stage.

These functions intentionally do not import aiogram and do not access Telegram
network APIs. They are small wrappers around the core preview adapter and the
Russian message formatters.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

from malyarka_core.adapters.telegram import build_order_preview_from_text
from malyarka_core.parsing import parse_size_line
from malyarka_telegram.keyboards import (
    CopyKeyboardSpec,
    build_clarify_intent_keyboard,
    build_copy_keyboard_for_preview,
    build_engineer_task_keyboard,
)
from malyarka_telegram.messages import (
    format_access_denied_message,
    format_help_message,
    format_order_format_message,
    format_photo_not_supported_message,
    format_preview_message,
    format_unknown_text_message,
    format_welcome_message,
)
from malyarka_telegram.obsidian_inbox import (
    ObsidianInboxError,
    append_hermes_inbox_note,
)
from malyarka_telegram.router import route_telegram_text
from malyarka_telegram.session import InMemoryModeSessionStore


@dataclass(frozen=True)
class TelegramTextResponse:
    """Text plus optional framework-free inline keyboard specification."""

    text: str
    copy_keyboard: CopyKeyboardSpec | None = None


_SIZE_LINE_RE = re.compile(
    r"(?:^|\n)\s*(?:(?:№\s*)?\d+\s*[\).\:]\s*)?\d+\s*(?:[\*xхXХ×]|\s)\s*\d+"
)

_WELCOME_COMMANDS = {
    "/start",
    "старт",
    "здравствуйте",
    "здравствуй",
    "привет",
    "новый заказ",
}
_HELP_COMMANDS = {"/help", "помощь", "статус"}
_FORMAT_COMMANDS = {"формат заказа"}
_STOP_COMMANDS = {"/cancel", "стоп", "отмена"}
_PREVIEW_ONLY_COMMANDS = {
    "показать спорные",
    "показать подтверждённые",
    "сделать corel",
    "сделать файл малярки",
}


def handle_text_message(text: str, user_id: int | str | None = None) -> str:
    """Handle any text message as a command or possible text order."""

    return build_text_response(text, user_id=user_id).text


def build_text_response(
    text: str, user_id: int | str | None = None
) -> TelegramTextResponse:
    """Handle text and return message text with optional inline keyboard spec."""

    if text is None:
        text = ""

    stripped = text.strip()
    lower_text = stripped.lower()
    dangerous_words = (
        ".env",
        "git add .",
        "bot.py",
        "orders.db",
        "token",
        "токен",
        "hermes_bot.py",
        "delete",
        "remove",
        "os.remove",
        "shutil",
        "vision",
        "фото",
        "cp",
        "chmod",
    )

    if stripped == "" or stripped.startswith("!"):
        return TelegramTextResponse(
            "Hermes из Telegram на этом этапе не запускается. Выберите /инженер для read-only управления проектом."
        )
    if any(dangerous_word in lower_text for dangerous_word in dangerous_words):
        return TelegramTextResponse(
            "Опасная команда не выполнена. Файлы, секреты и системные действия защищены."
        )

    normalized = _normalize_text(text)
    if not normalized:
        return TelegramTextResponse(format_unknown_text_message())

    if normalized in _WELCOME_COMMANDS:
        return TelegramTextResponse(format_welcome_message())
    if normalized in _HELP_COMMANDS:
        return TelegramTextResponse(format_help_message())
    if normalized in _FORMAT_COMMANDS:
        return TelegramTextResponse(format_order_format_message())
    if normalized in _STOP_COMMANDS:
        return TelegramTextResponse(
            "Остановлено. Чтобы начать заново, нажмите «Новый заказ»."
        )
    if normalized in _PREVIEW_ONLY_COMMANDS:
        return TelegramTextResponse("Сначала пришлите заказ текстом.")

    if _looks_like_order(text):
        preview = build_order_preview_from_text(text)
        preview["editable_copy_text"] = _build_editable_copy_text(text)
        return TelegramTextResponse(
            format_preview_message(preview),
            copy_keyboard=build_copy_keyboard_for_preview(preview),
        )

    return TelegramTextResponse(format_unknown_text_message())


def handle_text_message_with_router(
    text: str,
    user_id: int,
    session_store: InMemoryModeSessionStore,
    owner_id: int | None = None,
    *,
    write_obsidian_inbox: bool = False,
    obsidian_inbox_path: str | Path | None = None,
) -> TelegramTextResponse:
    """Route text through safe mode state before using the existing preview path."""

    route_result = route_telegram_text(
        user_id=user_id,
        text=text,
        session_store=session_store,
        owner_id=owner_id,
    )
    if route_result.should_parse_order:
        if str(text or "").strip().startswith("!"):
            return TelegramTextResponse(
                "Hermes из Telegram на этом этапе не запускается. Используйте read-only режим /инженер."
            )
        return build_text_response(text, user_id=user_id)
    if route_result.action == "access_denied":
        return TelegramTextResponse(format_access_denied_message())
    if route_result.action == "clarify_intent":
        return TelegramTextResponse(
            route_result.message,
            copy_keyboard=build_clarify_intent_keyboard(),
        )
    if route_result.action == "engineer_task_card":
        response_text = route_result.message
        if write_obsidian_inbox:
            response_text = _append_engineer_task_to_obsidian(
                route_result.message,
                user_id=user_id,
                obsidian_inbox_path=obsidian_inbox_path,
            )
        return TelegramTextResponse(
            response_text,
            copy_keyboard=build_engineer_task_keyboard(route_result.message),
        )
    return TelegramTextResponse(route_result.message)


def _append_engineer_task_to_obsidian(
    message: str,
    *,
    user_id: int,
    obsidian_inbox_path: str | Path | None,
) -> str:
    try:
        inbox_path = append_hermes_inbox_note(
            message,
            user_id=user_id,
            inbox_path=obsidian_inbox_path,
        )
    except (ObsidianInboxError, OSError) as error:
        return "\n\n".join((message, f"Obsidian inbox: not saved ({error})."))

    return "\n\n".join(
        (
            message,
            f"Obsidian inbox: saved to {inbox_path.name}.",
        )
    )


def handle_photo_message() -> str:
    """Handle a Telegram photo without downloading or processing it."""

    return format_photo_not_supported_message()


def handle_command_message(text: str) -> str:
    """Handle slash commands as technical compatibility, not the main UX."""

    return handle_text_message(text)


def _normalize_text(text: str) -> str:
    return " ".join(text.strip().lower().split())


def _looks_like_order(text: str) -> bool:
    return bool(_SIZE_LINE_RE.search(text))


def _build_editable_copy_text(text: str) -> str:
    lines: list[str] = []
    for line in text.splitlines():
        item, disputed_item = parse_size_line(line)
        if item is not None:
            lines.append(f"{item.height} {item.width} {item.quantity}")
        elif disputed_item is not None:
            lines.append(disputed_item.raw)
    return "\n".join(lines)
