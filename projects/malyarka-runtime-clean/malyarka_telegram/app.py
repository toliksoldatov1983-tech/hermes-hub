"""Safe app scaffold for a future aiogram Telegram bot.

Importing this module must not require aiogram, a token, or network access.
Polling is only prepared inside explicit runtime functions.
"""

from __future__ import annotations

import argparse
import asyncio
import importlib.util
import json
import re
import sys
import tempfile
from dataclasses import dataclass, replace
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from malyarka_telegram.access import is_owner, is_owner_id_configured
from malyarka_telegram.config import TelegramConfig, load_config
from malyarka_telegram.keyboards import (
    CLARIFY_INTENT_ACTIONS,
    COREL_EXCEL_ACTION,
    ENGINEER_TASK_ACTIONS,
    ENGINEER_TASK_ALLOW_ACTION,
    ENGINEER_TASK_CANCEL_ACTION,
    MALYARKA_FILE_ACTION,
)
from malyarka_telegram.messages import (
    format_access_denied_message,
    format_engineer_task_callback_message,
    format_voice_not_configured_message,
    format_voice_transcribed_message,
    format_voice_transcription_failed_message,
)
from malyarka_telegram.session import InMemoryModeSessionStore
from malyarka_telegram.voice import (
    VoiceTranscriptionFailed,
    VoiceTranscriptionNotConfigured,
    transcribe_voice_file,
)


_RUNTIME_SESSION_STORE = InMemoryModeSessionStore()
_RUNTIME_COREL_ROWS: dict[int, tuple[tuple[int, int, int], ...]] = {}
_RUNTIME_ENGINEER_TASKS: dict[int, str] = {}
TELEGRAM_MESSAGE_SAFE_LIMIT = 3900
POLLING_EXIT_UNAUTHORIZED = 4
POLLING_EXIT_CONFLICT = 5
POLLING_EXIT_NETWORK_ERROR = 6
POLLING_EXIT_UNEXPECTED_ERROR = 1


@dataclass(frozen=True)
class PreparedCorelExcel:
    """Result of safe Corel Excel preparation without Telegram file sending."""

    action: str
    path: Path
    rows_count: int
    sent_to_telegram: bool = False


@dataclass(frozen=True)
class PreparedMalyarkaFile:
    """Result of safe Malyarka File preparation without Telegram file sending."""

    action: str
    path: Path
    rows_count: int
    sent_to_telegram: bool = False


def _is_aiogram_available() -> bool:
    return importlib.util.find_spec("aiogram") is not None


def _load_handler_status() -> tuple[bool, bool]:
    try:
        from malyarka_telegram.handlers import handle_text_message
    except ImportError:
        return False, False

    handler_available = callable(handle_text_message)
    return handler_available, handler_available


def create_app(config: TelegramConfig | None = None) -> dict[str, Any]:
    """Create a small runtime descriptor without starting network polling."""

    runtime_config = load_config() if config is None else config
    hermes_available, handler_available = _load_handler_status()
    has_token = bool(runtime_config.bot_token)
    aiogram_available = _is_aiogram_available()

    reason = ""
    if not aiogram_available:
        reason = "aiogram is not installed"
    elif not has_token:
        reason = "Telegram token is not configured"
    elif not handler_available:
        reason = "Telegram text handler is not available"
    elif not hermes_available:
        reason = "Hermes Router is not available"

    ready = aiogram_available and has_token and handler_available and hermes_available
    return {
        "ready": ready,
        "reason": reason,
        "has_token": has_token,
        "owner_id_configured": is_owner_id_configured(runtime_config.owner_id),
        "aiogram_available": aiogram_available,
        "hermes_router_available": hermes_available,
        "handle_text_message_available": handler_available,
        "polling_started": False,
    }


def get_diagnostics(config: TelegramConfig | None = None) -> dict[str, Any]:
    """Return safe diagnostics without exposing secrets or starting polling."""

    app = create_app(config)
    return {
        "aiogram_available": app["aiogram_available"],
        "handle_text_message_available": app["handle_text_message_available"],
        "has_token": app["has_token"],
        "owner_id_configured": app["owner_id_configured"],
        "hermes_router_available": app["hermes_router_available"],
        "polling_started": False,
        "ready_for_polling": app["ready"],
        "reason": app["reason"],
    }


def get_runtime_session_store() -> InMemoryModeSessionStore:
    """Return the shared in-memory mode store for a polling process."""

    return _RUNTIME_SESSION_STORE


def resolve_message_user_id(message: Any) -> int:
    """Resolve a stable user id from a Telegram-like message object."""

    user_id = getattr(getattr(message, "from_user", None), "id", None)
    if user_id is None:
        return 0
    return int(user_id)


def build_live_text_response(
    *,
    text: str,
    user_id: int,
    session_store: InMemoryModeSessionStore | None = None,
    config: TelegramConfig | None = None,
    write_obsidian_inbox: bool = False,
    obsidian_inbox_path: str | Path | None = None,
) -> Any:
    """Build a routed text response for live Telegram text handling."""

    from malyarka_telegram.handlers import TelegramTextResponse, handle_text_message_with_router

    runtime_config = TelegramConfig() if config is None else config
    if runtime_config.owner_id is not None and not is_owner(user_id, runtime_config.owner_id):
        _RUNTIME_COREL_ROWS.pop(user_id, None)
        return TelegramTextResponse(format_access_denied_message())

    active_session_store = (
        get_runtime_session_store() if session_store is None else session_store
    )
    response = handle_text_message_with_router(
        text,
        user_id=user_id,
        session_store=active_session_store,
        owner_id=runtime_config.owner_id,
        write_obsidian_inbox=write_obsidian_inbox,
        obsidian_inbox_path=obsidian_inbox_path,
    )
    _remember_corel_excel_rows(user_id=user_id, response=response)
    _remember_engineer_task(user_id=user_id, text=text, response=response)
    return response


def _remember_corel_excel_rows(*, user_id: int, response: Any) -> None:
    copy_keyboard = getattr(response, "copy_keyboard", None)
    buttons = getattr(copy_keyboard, "buttons", ()) if copy_keyboard is not None else ()
    has_excel_action = any(
        getattr(button, "action", None) == COREL_EXCEL_ACTION for button in buttons
    )
    if not has_excel_action:
        _RUNTIME_COREL_ROWS.pop(user_id, None)
        return

    rows = _extract_corel_rows_from_buttons(buttons)
    if not rows:
        rows = _extract_corel_rows_from_text(getattr(response, "text", ""))

    if rows:
        _RUNTIME_COREL_ROWS[user_id] = tuple(rows)
    else:
        _RUNTIME_COREL_ROWS.pop(user_id, None)


def _remember_engineer_task(*, user_id: int, text: str, response: Any) -> None:
    copy_keyboard = getattr(response, "copy_keyboard", None)
    buttons = getattr(copy_keyboard, "buttons", ()) if copy_keyboard is not None else ()
    has_engineer_allow_action = any(
        getattr(button, "action", None) == ENGINEER_TASK_ALLOW_ACTION for button in buttons
    )
    if has_engineer_allow_action:
        _RUNTIME_ENGINEER_TASKS[user_id] = str(text or "").strip()


def split_telegram_text(text: str, *, limit: int = TELEGRAM_MESSAGE_SAFE_LIMIT) -> list[str]:
    """Split long Telegram messages into safe chunks."""

    if len(text) <= limit:
        return [text]

    chunks: list[str] = []
    remaining = text
    while len(remaining) > limit:
        split_at = remaining.rfind("\n\n", 0, limit)
        if split_at <= 0:
            split_at = remaining.rfind("\n", 0, limit)
        if split_at <= 0:
            split_at = limit
        chunks.append(remaining[:split_at].rstrip())
        remaining = remaining[split_at:].lstrip()
    if remaining:
        chunks.append(remaining)
    return chunks


def split_engineer_approval_message(text: str) -> list[str]:
    """Keep the execution prompt and review package as separate Telegram messages."""

    review_marker = "\n\nПАКЕТ ДЛЯ НЕЗАВИСИМОГО РЕВЬЮ"
    if review_marker not in text:
        return split_telegram_text(text)

    assignment, review = text.split(review_marker, 1)
    review = "ПАКЕТ ДЛЯ НЕЗАВИСИМОГО РЕВЬЮ" + review
    chunks: list[str] = []
    for section in (assignment, review):
        chunks.extend(split_telegram_text(section.strip()))
    return chunks


def _extract_corel_rows_from_buttons(buttons: Any) -> list[tuple[int, int, int]]:
    for button in buttons:
        if getattr(button, "action", None) in (COREL_EXCEL_ACTION, MALYARKA_FILE_ACTION):
            continue
        copy_text = getattr(button, "copy_text", None)
        if copy_text:
            rows = _parse_corel_rows(str(copy_text).splitlines(), require_numbered=False)
            if rows:
                return rows
    return []


def _extract_corel_rows_from_text(text: str) -> list[tuple[int, int, int]]:
    return _parse_corel_rows(text.splitlines(), require_numbered=True)


def _parse_corel_rows(
    lines: list[str],
    *,
    require_numbered: bool,
) -> list[tuple[int, int, int]]:
    rows: list[tuple[int, int, int]] = []
    pattern = (
        r"^\d+\.\s+(\d+)\s+(\d+)\s+(\d+)$"
        if require_numbered
        else r"^(?:\d+\.\s+)?(\d+)\s+(\d+)\s+(\d+)$"
    )
    for line in lines:
        match = re.match(pattern, line.strip())
        if match:
            rows.append(tuple(int(value) for value in match.groups()))
    return rows


def prepare_corel_excel_for_user(
    *,
    user_id: int,
    output_dir: str | Path | None = None,
) -> PreparedCorelExcel:
    """Prepare a Corel .xlsx from the last clean live order without sending it."""

    rows = _RUNTIME_COREL_ROWS.get(user_id)
    if not rows:
        raise ValueError("Нет подготовленного чистого заказа для Excel Corel.")

    from malyarka_core.exports.corel import export_corel_xlsx

    target_dir = Path(tempfile.gettempdir()) if output_dir is None else Path(output_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    output_path = target_dir / f"malyarka_corel_{user_id}.xlsx"
    order = SimpleNamespace(
        items=[
            SimpleNamespace(height=height, width=width, quantity=quantity)
            for height, width, quantity in rows
        ],
        disputed_items=[],
    )
    export_corel_xlsx(order, output_path)
    return PreparedCorelExcel(
        action=COREL_EXCEL_ACTION,
        path=output_path,
        rows_count=len(rows),
        sent_to_telegram=False,
    )


def prepare_malyarka_file_for_user(
    *,
    user_id: int,
    output_dir: str | Path | None = None,
) -> PreparedMalyarkaFile:
    """Prepare a Malyarka File .xlsx from the last clean live order."""

    rows = _RUNTIME_COREL_ROWS.get(user_id)
    if not rows:
        raise ValueError("Нет подготовленного чистого заказа для Файла Малярки.")

    from malyarka_core.exports.malyarka_file import export_malyarka_file_xlsx
    from malyarka_core.models import OrderDraft, OrderItem

    target_dir = Path(tempfile.gettempdir()) if output_dir is None else Path(output_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    output_path = target_dir / f"malyarka_file_{user_id}.xlsx"
    order = OrderDraft(
        items=[
            OrderItem(height=height, width=width, quantity=quantity)
            for height, width, quantity in rows
        ],
        disputed_items=[],
    )
    export_malyarka_file_xlsx(order, output_path)
    return PreparedMalyarkaFile(
        action=MALYARKA_FILE_ACTION,
        path=output_path,
        rows_count=len(rows),
        sent_to_telegram=False,
    )

async def handle_corel_excel_callback(
    callback: Any,
    *,
    output_dir: str | Path | None = None,
    document_factory: Any | None = None,
    config: TelegramConfig | None = None,
) -> PreparedCorelExcel | None:
    """Prepare and send the latest clean Corel Excel file via Telegram callback."""

    user_id = resolve_message_user_id(callback)
    runtime_config = TelegramConfig() if config is None else config
    if runtime_config.owner_id is not None and not is_owner(user_id, runtime_config.owner_id):
        await callback.answer(format_access_denied_message(), show_alert=True)
        return None
    try:
        prepared = prepare_corel_excel_for_user(user_id=user_id, output_dir=output_dir)
    except ValueError as error:
        await callback.answer(str(error), show_alert=True)
        return None

    message = getattr(callback, "message", None)
    if message is None or not hasattr(message, "answer_document"):
        await callback.answer("Не могу отправить Excel: нет сообщения callback.", show_alert=True)
        return None

    build_document = _build_telegram_document if document_factory is None else document_factory
    await callback.answer("Excel для Corel готов. Отправляю файл.", show_alert=False)
    await message.answer_document(
        build_document(prepared.path),
        caption="Excel для Corel",
    )
    return replace(prepared, sent_to_telegram=True)


async def handle_malyarka_file_callback(
    callback: Any,
    *,
    output_dir: str | Path | None = None,
    document_factory: Any | None = None,
    config: TelegramConfig | None = None,
) -> PreparedMalyarkaFile | None:
    """Prepare and send the latest clean Malyarka File via Telegram callback."""

    user_id = resolve_message_user_id(callback)
    runtime_config = TelegramConfig() if config is None else config
    if runtime_config.owner_id is not None and not is_owner(user_id, runtime_config.owner_id):
        await callback.answer(format_access_denied_message(), show_alert=True)
        return None
    try:
        prepared = prepare_malyarka_file_for_user(user_id=user_id, output_dir=output_dir)
    except ValueError as error:
        await callback.answer(str(error), show_alert=True)
        return None

    message = getattr(callback, "message", None)
    if message is None or not hasattr(message, "answer_document"):
        await callback.answer("Не могу отправить Файл Малярки: нет сообщения callback.", show_alert=True)
        return None

    build_document = _build_telegram_document if document_factory is None else document_factory
    await callback.answer("Файл Малярки готов. Отправляю файл.", show_alert=False)
    await message.answer_document(
        build_document(prepared.path),
        caption="Файл Малярки",
    )
    return replace(prepared, sent_to_telegram=True)


async def handle_engineer_task_callback(
    callback: Any,
    *,
    config: TelegramConfig | None = None,
) -> str | None:
    """Answer engineer task-card callbacks without launching Hermes or changing files."""

    user_id = resolve_message_user_id(callback)
    runtime_config = TelegramConfig() if config is None else config
    if runtime_config.owner_id is not None and not is_owner(user_id, runtime_config.owner_id):
        await callback.answer(format_access_denied_message(), show_alert=True)
        return None

    action = getattr(callback, "data", None)
    task_text = _RUNTIME_ENGINEER_TASKS.get(user_id)
    message = format_engineer_task_callback_message(action, task_text=task_text)
    show_alert = action not in ENGINEER_TASK_ACTIONS
    if action == ENGINEER_TASK_ALLOW_ACTION:
        await callback.answer(
            "Задание и пакет ревью подготовлены для ручного копирования.",
            show_alert=False,
        )
        telegram_message = getattr(callback, "message", None)
        if telegram_message is not None and hasattr(telegram_message, "answer"):
            for chunk in split_engineer_approval_message(message):
                await telegram_message.answer(chunk)
        else:
            await callback.answer(message, show_alert=False)
        return message

    if action == ENGINEER_TASK_CANCEL_ACTION:
        _RUNTIME_ENGINEER_TASKS.pop(user_id, None)

    await callback.answer(message, show_alert=show_alert)
    return message


async def handle_clarify_intent_callback(
    callback: Any,
    *,
    config: TelegramConfig | None = None,
) -> str | None:
    """Answer Free Entry clarify intent callback buttons safely.

    - free_entry_order → set mode to ORDER
    - free_entry_ideas → set mode to IDEAS
    - free_entry_engineer → set mode to ENGINEER
    - free_entry_cancel → keep NEUTRAL
    """
    user_id = resolve_message_user_id(callback)
    runtime_config = TelegramConfig() if config is None else config
    if runtime_config.owner_id is not None and not is_owner(user_id, runtime_config.owner_id):
        await callback.answer(format_access_denied_message(), show_alert=True)
        return None

    from malyarka_telegram.keyboards import (
        CLARIFY_INTENT_CANCEL,
        CLARIFY_INTENT_ENGINEER,
        CLARIFY_INTENT_IDEAS,
        CLARIFY_INTENT_ORDER,
    )
    from malyarka_telegram.modes import TelegramMode

    data = getattr(callback, "data", None)
    session_store = get_runtime_session_store()

    if data == CLARIFY_INTENT_ORDER:
        session_store.set_mode(user_id, TelegramMode.ORDER)
        await callback.answer("Включён режим /заказ", show_alert=False)
        return "mode_switched_to_order"
    if data == CLARIFY_INTENT_IDEAS:
        session_store.set_mode(user_id, TelegramMode.IDEAS)
        await callback.answer("Включён режим /идеи", show_alert=False)
        return "mode_switched_to_ideas"
    if data == CLARIFY_INTENT_ENGINEER:
        session_store.set_mode(user_id, TelegramMode.ENGINEER)
        await callback.answer("Включён режим /инженер", show_alert=False)
        return "mode_switched_to_engineer"
    if data == CLARIFY_INTENT_CANCEL:
        session_store.set_mode(user_id, TelegramMode.NEUTRAL)
        await callback.answer("Уточнение отменено", show_alert=False)
        return "clarification_cancelled"

    await callback.answer("Неизвестная кнопка", show_alert=True)
    return None


def _build_telegram_document(path: Path) -> Any:
    """Return aiogram FSInputFile in live mode, or a Path for tests without aiogram."""

    try:
        from aiogram.types import FSInputFile
    except ImportError:
        return path
    return FSInputFile(path, filename=path.name)


def run_polling(config: TelegramConfig | None = None) -> int:
    """Run Telegram polling only when explicitly requested by CLI flag."""

    runtime_config = load_config() if config is None else config
    if not runtime_config.bot_token:
        print(
            "Telegram token is not configured. Set MALYARKA_TELEGRAM_BOT_TOKEN.",
            file=sys.stderr,
        )
        return 2

    if not _is_aiogram_available():
        print("aiogram is not installed.", file=sys.stderr)
        return 3

    try:
        asyncio.run(_run_aiogram_polling(runtime_config))
    except Exception as error:
        exit_code, message = _classify_polling_error(error)
        print(message, file=sys.stderr)
        return exit_code
    return 0


def _classify_polling_error(error: Exception) -> tuple[int, str]:
    """Return a stable exit code and secret-free message for polling failures."""

    error_name = error.__class__.__name__
    if error_name == "TelegramUnauthorizedError":
        return (
            POLLING_EXIT_UNAUTHORIZED,
            "Telegram rejected the bot token: Unauthorized. "
            "Check MALYARKA_TELEGRAM_BOT_TOKEN.",
        )
    if error_name == "TelegramConflictError":
        return (
            POLLING_EXIT_CONFLICT,
            "Telegram polling conflict: another bot instance is already running.",
        )
    if error_name in {
        "TelegramNetworkError",
        "TelegramServerError",
        "ClientConnectorError",
        "TimeoutError",
    }:
        return (
            POLLING_EXIT_NETWORK_ERROR,
            f"Telegram polling temporary failure: {error_name}. Try again later.",
        )
    return (
        POLLING_EXIT_UNEXPECTED_ERROR,
        f"Telegram polling failed: {error_name}: {error}",
    )


async def _run_aiogram_polling(config: TelegramConfig) -> None:
    from aiogram import Bot, Dispatcher
    from aiogram.types import (
        CopyTextButton,
        InlineKeyboardButton,
        InlineKeyboardMarkup,
        ReplyKeyboardRemove,
    )

    from malyarka_telegram.handlers import handle_photo_message
    from malyarka_telegram.keyboards import CopyKeyboardSpec

    bot = Bot(token=config.bot_token)
    dispatcher = Dispatcher()
    session_store = get_runtime_session_store()

    def _build_inline_copy_markup(
        copy_keyboard: CopyKeyboardSpec | None,
    ) -> InlineKeyboardMarkup | None:
        if copy_keyboard is None or not copy_keyboard.buttons:
            return None

        inline_keyboard = []
        for button in copy_keyboard.buttons:
            if button.action:
                inline_keyboard.append(
                    [InlineKeyboardButton(text=button.label, callback_data=button.action)]
                )
            elif button.copy_text is not None:
                inline_keyboard.append(
                    [
                        InlineKeyboardButton(
                            text=button.label,
                            copy_text=CopyTextButton(text=button.copy_text),
                        )
                    ]
                )
        if not inline_keyboard:
            return None
        return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    remove_reply_markup = ReplyKeyboardRemove(remove_keyboard=True)

    @dispatcher.message()
    async def _handle_message(message: Any) -> None:
        text = getattr(message, "text", None)
        if text:
            response = build_live_text_response(
                text=text,
                user_id=resolve_message_user_id(message),
                session_store=session_store,
                config=config,
                write_obsidian_inbox=True,
            )
            reply_markup = _build_inline_copy_markup(response.copy_keyboard)
            await message.answer(
                response.text,
                reply_markup=reply_markup or remove_reply_markup,
            )
        elif getattr(message, "voice", None) is not None:
            voice = getattr(message, "voice")
            file_id = getattr(voice, "file_id", None)
            if not file_id:
                await message.answer(
                    format_voice_transcription_failed_message(),
                    reply_markup=remove_reply_markup,
                )
                return
            with tempfile.TemporaryDirectory(prefix="malyarka_voice_") as temp_dir:
                voice_path = Path(temp_dir) / "telegram_voice.ogg"
                telegram_file = await bot.get_file(file_id)
                await bot.download_file(telegram_file.file_path, voice_path)
                try:
                    recognized_text = transcribe_voice_file(
                        voice_path,
                        api_key=config.openai_api_key,
                        model=config.voice_transcribe_model,
                        local_command=config.local_stt_command,
                        local_model_path=config.local_stt_model_path,
                    )
                except VoiceTranscriptionNotConfigured:
                    await message.answer(
                        format_voice_not_configured_message(),
                        reply_markup=remove_reply_markup,
                    )
                    return
                except VoiceTranscriptionFailed:
                    await message.answer(
                        format_voice_transcription_failed_message(),
                        reply_markup=remove_reply_markup,
                    )
                    return
            response = build_live_text_response(
                text=recognized_text,
                user_id=resolve_message_user_id(message),
                session_store=session_store,
                config=config,
                write_obsidian_inbox=True,
            )
            reply_markup = _build_inline_copy_markup(response.copy_keyboard)
            await message.answer(
                "\n\n".join((format_voice_transcribed_message(recognized_text), response.text)),
                reply_markup=reply_markup or remove_reply_markup,
            )
        else:
            await message.answer(handle_photo_message(), reply_markup=remove_reply_markup)

    @dispatcher.callback_query(lambda callback: callback.data == COREL_EXCEL_ACTION)
    async def _handle_corel_excel_callback(callback: Any) -> None:
        await handle_corel_excel_callback(callback, config=config)

    @dispatcher.callback_query(lambda callback: callback.data == MALYARKA_FILE_ACTION)
    async def _handle_malyarka_file_callback(callback: Any) -> None:
        await handle_malyarka_file_callback(callback, config=config)

    @dispatcher.callback_query(lambda callback: callback.data in ENGINEER_TASK_ACTIONS)
    async def _handle_engineer_task_callback(callback: Any) -> None:
        await handle_engineer_task_callback(callback, config=config)

    @dispatcher.callback_query(lambda callback: callback.data in CLARIFY_INTENT_ACTIONS)
    async def _handle_clarify_intent_callback(callback: Any) -> None:
        await handle_clarify_intent_callback(callback, config=config)

    try:
        await bot.get_me()
        await dispatcher.start_polling(bot, polling_timeout=0)
    finally:
        await bot.session.close()


def main(argv: list[str] | None = None) -> int:
    """CLI entry point with explicit safe check and future polling modes."""

    parser = argparse.ArgumentParser(description="Safe Malyarka Telegram app")
    parser.add_argument(
        "--check",
        action="store_true",
        help="print safe diagnostics without starting polling",
    )
    parser.add_argument(
        "--run-polling",
        action="store_true",
        help="start Telegram polling using environment token",
    )
    args = parser.parse_args(argv)

    if args.check and args.run_polling:
        print("Choose only one mode: --check or --run-polling.", file=sys.stderr)
        return 2

    if args.check:
        print(json.dumps(get_diagnostics(), ensure_ascii=False, sort_keys=True))
        return 0

    if args.run_polling:
        return run_polling()

    print("No mode selected. Use --check for diagnostics.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
