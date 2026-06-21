"""Russian user-facing messages for the safe Telegram layer."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from malyarka_telegram.engineer_tasks import (
    format_engineer_approval_package,
    format_engineer_cancel_message,
    format_engineer_edit_message,
    format_engineer_task_card,
    format_engineer_unknown_action_message,
    sanitize_engineer_task_text,
)
from malyarka_telegram.keyboards import (
    ENGINEER_TASK_ALLOW_ACTION,
    ENGINEER_TASK_CANCEL_ACTION,
    ENGINEER_TASK_EDIT_ACTION,
    MAIN_BUTTONS,
    build_confirmed_copy_text,
    build_copy_keyboard_for_preview,
    build_disputed_copy_text,
)


def format_welcome_message() -> str:
    """Return a short Russian onboarding message."""

    return "\n".join(
        [
            "Здравствуйте.",
            "Выберите дверь личного бота:",
            "🧾 Новый заказ — рабочий режим /заказ.",
            "🛠 Инженер проекта — read-only режим /инженер.",
            "💬 Идеи / разговор — read-only режим /идеи.",
            "Фото-режим пока не подключён.",
        ]
    )


def format_help_message() -> str:
    """Return help text focused on Russian commands and text-first workflow."""

    return "\n".join(
        [
            "Главное меню:",
            ", ".join(MAIN_BUTTONS),
            "🧾 Новый заказ — разбор размеров и Excel для Corel.",
            "🛠 Инженер проекта — безопасный read-only статус и подготовка задач.",
            "💬 Идеи / разговор — обсуждение без создания заказа.",
            "Скрытый админ-режим в меню не показывается.",
            "Экспорт будет заблокирован, если есть спорные строки.",
        ]
    )


def format_order_format_message() -> str:
    """Return an example of the supported text order format."""

    return "\n".join(
        [
            "Формат заказа:",
            "500 700 2",
            "300 400",
            "Первое число — высота, второе — ширина, третье — количество.",
        ]
    )


def format_photo_not_supported_message() -> str:
    """Return the photo placeholder message for the first safe stage."""

    return "Фото-режим ещё не подключён. Пришлите заказ текстом."


def format_voice_not_configured_message() -> str:
    """Return voice placeholder when transcription config is missing."""

    return (
        "Голосовое получил, но распознавание ещё не подключено. "
        "Нужно подключить локальный whisper.cpp или добавить OPENAI_API_KEY на сервер."
    )


def format_voice_transcription_failed_message() -> str:
    """Return a safe message when voice transcription fails."""

    return "Голосовое получил, но не смог распознать. Пришлите текстом или попробуйте ещё раз."


def format_voice_transcribed_message(text: str) -> str:
    """Return the recognized voice text without changing its content."""

    clean_text = " ".join(str(text or "").split())
    return f"Распознал голос:\n{clean_text}"


def format_unknown_text_message() -> str:
    """Return a Russian fallback for text that is not an order or command."""

    return "\n".join(
        [
            "Не выбран режим.",
            "Выберите действие: 🧾 Новый заказ, 🛠 Инженер проекта или 💬 Идеи / разговор.",
        ]
    )


def read_project_state_summary() -> tuple[str | None, str | None]:
    """Read safe project state fields without modifying the state file."""

    state_path = Path(__file__).resolve().parents[1] / "MALYARKA_CURRENT_STATE.md"
    try:
        text = state_path.read_text(encoding="utf-8-sig")
    except OSError:
        return None, None

    state_version: str | None = None
    next_step: str | None = None
    lines = text.splitlines()
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("state_version:"):
            state_version = stripped.split(":", 1)[1].strip()
        if stripped == "## 8. Следующий шаг":
            for candidate in lines[index + 1 : index + 12]:
                candidate = candidate.strip()
                if candidate and not candidate.startswith("#"):
                    next_step = candidate
                    break
            break
    return state_version, next_step


def format_engineer_mode_message() -> str:
    """Return read-only engineer mode status."""

    state_version, next_step = read_project_state_summary()
    lines = [
        "Инженер проекта включён.",
        "Сейчас режим безопасный: могу показать статус, следующий шаг и подготовить задачу, но не меняю файлы без подтверждения.",
        "Hermes из Telegram на этом этапе не запускается.",
    ]
    if state_version:
        lines.append(f"state_version: {state_version}")
    if next_step:
        lines.append(f"Следующий шаг из состояния: {next_step}")
    return "\n".join(lines)


def format_engineer_task_card_message(user_task_text: str | None) -> str:
    """Return a copy-ready manual task for Hermes from user text."""

    return format_engineer_task_card(user_task_text)


def format_engineer_task_callback_message(
    action: str | None,
    *,
    task_text: str | None = None,
) -> str:
    """Return a safe read-only response for engineer task card buttons."""

    if action == ENGINEER_TASK_ALLOW_ACTION:
        return format_engineer_approval_package(task_text)
    if action == ENGINEER_TASK_CANCEL_ACTION:
        return format_engineer_cancel_message()
    if action == ENGINEER_TASK_EDIT_ACTION:
        return format_engineer_edit_message()
    return format_engineer_unknown_action_message()


def _sanitize_engineer_task_text(user_task_text: str | None) -> str:
    return sanitize_engineer_task_text(user_task_text)


def format_ideas_mode_message() -> str:
    """Return read-only ideas mode status."""

    return "\n".join(
        [
            "Режим идей включён.",
            "Можно свободно обсуждать идеи, производство, фасады, Excel, CorelDRAW и Telegram UX.",
            "Размеры здесь не оформляются как заказ автоматически.",
            "Если идея полезная, я подготовлю короткую выжимку для /инженер.",
        ]
    )


def format_admin_diagnostics_message(
    *,
    current_mode: str,
    owner_id_configured: bool,
    polling_started: bool = False,
) -> str:
    """Return safe admin diagnostics without secret values."""

    state_version, _next_step = read_project_state_summary()
    lines = [
        "Админ-диагностика:",
        f"current_mode={current_mode}",
        f"owner_id_configured={str(owner_id_configured).lower()}",
        f"polling_started={str(polling_started).lower()}",
    ]
    lines.append(f"state_version={state_version or 'unknown'}")
    return "\n".join(lines)


def format_access_denied_message() -> str:
    """Return a short private-bot access denial without revealing internals."""

    return "Доступ закрыт. Это личный бот владельца."


def format_preview_message(preview: dict[str, Any]) -> str:
    """Format a parsed order preview in Russian without using core text strings."""

    lines: list[str] = ["Предпросмотр заказа", "", "Подтверждённые строки:"]

    confirmed_items = preview.get("confirmed_items", [])
    if confirmed_items:
        for number, item in enumerate(confirmed_items, start=1):
            lines.append(
                f"{number}. {item['height']} {item['width']} {item['quantity']}"
            )
    else:
        lines.append("нет")

    lines.extend(["", "Спорные строки:"])
    disputed_items = preview.get("disputed_items", [])
    if disputed_items:
        for number, item in enumerate(disputed_items, start=1):
            raw = item.get("raw", "")
            lines.append(f"{number}. {raw}")
    else:
        lines.append("нет")

    can_export = bool(preview.get("can_export"))
    lines.extend(
        [
            "",
            f"Всего деталей: {preview.get('total_quantity', 0)}",
            f"Общая площадь: {preview.get('total_area_m2', 0.0):.3f} м²",
            f"Экспорт: {'доступен' if can_export else 'заблокирован'}",
        ]
    )

    if not can_export:
        lines.append(_format_export_block_reason(preview))

    lines.extend(["", "Скопировать подтверждённые строки:"])
    confirmed_copy_text = build_confirmed_copy_text(preview)
    lines.append(confirmed_copy_text if confirmed_copy_text else "нет")

    lines.extend(["", "Скопировать спорные строки:"])
    disputed_copy_text = build_disputed_copy_text(preview)
    lines.append(disputed_copy_text if disputed_copy_text else "нет")

    copy_keyboard = build_copy_keyboard_for_preview(preview)
    if copy_keyboard is not None:
        lines.extend(copy_keyboard.warnings)

    return "\n".join(lines)


def _format_export_block_reason(preview: dict[str, Any]) -> str:
    if preview.get("disputed_count", 0):
        return "Причина блокировки: есть спорные строки."
    if not preview.get("confirmed_count", 0):
        return "Причина блокировки: нет подтверждённых строк."
    return "Причина блокировки: заказ пока нельзя экспортировать."
