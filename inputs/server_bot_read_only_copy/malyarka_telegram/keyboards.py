"""Pure descriptions of Russian Telegram buttons for the safe layer."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

MAX_COPY_TEXT_LENGTH = 256
COREL_EXCEL_ACTION = "download_corel_excel"
MALYARKA_FILE_ACTION = "download_malyarka_file"

MAIN_BUTTONS = (
    "🧾 Новый заказ",
    "🛠 Инженер проекта",
    "💬 Идеи / разговор",
)

ENGINEER_TASK_ALLOW_ACTION = "engineer_task_allow_read_only"
ENGINEER_TASK_CANCEL_ACTION = "engineer_task_cancel_read_only"
ENGINEER_TASK_EDIT_ACTION = "engineer_task_edit_read_only"
ENGINEER_TASK_ACTIONS = frozenset(
    (
        ENGINEER_TASK_ALLOW_ACTION,
        ENGINEER_TASK_CANCEL_ACTION,
        ENGINEER_TASK_EDIT_ACTION,
    )
)

# --- Free Entry clarify intent callback data constants ---

CLARIFY_INTENT_ORDER = "free_entry_order"
CLARIFY_INTENT_IDEAS = "free_entry_ideas"
CLARIFY_INTENT_ENGINEER = "free_entry_engineer"
CLARIFY_INTENT_CANCEL = "free_entry_cancel"

CLARIFY_INTENT_ACTIONS = frozenset((
    CLARIFY_INTENT_ORDER,
    CLARIFY_INTENT_IDEAS,
    CLARIFY_INTENT_ENGINEER,
    CLARIFY_INTENT_CANCEL,
))


@dataclass(frozen=True)
class CopyTextButtonSpec:
    """Framework-free description of a Telegram inline button."""

    label: str
    copy_text: str | None = None
    action: str | None = None


@dataclass(frozen=True)
class CopyKeyboardSpec:
    """Framework-free inline keyboard plus warnings for skipped copy buttons."""

    buttons: tuple[CopyTextButtonSpec, ...]
    warnings: tuple[str, ...] = ()


def get_main_keyboard_labels() -> list[str]:
    """Return labels for the future Telegram reply keyboard."""

    return list(MAIN_BUTTONS)


def build_engineer_task_keyboard(task_copy_text: str | None = None) -> CopyKeyboardSpec:
    """Build safe button specs for an engineer task card."""

    buttons: list[CopyTextButtonSpec] = []
    if task_copy_text and len(task_copy_text) <= MAX_COPY_TEXT_LENGTH:
        buttons.append(CopyTextButtonSpec("Скопировать для Hermes", task_copy_text))
    buttons.extend(
        (
            CopyTextButtonSpec("Разрешаю", action=ENGINEER_TASK_ALLOW_ACTION),
            CopyTextButtonSpec("Отмена", action=ENGINEER_TASK_CANCEL_ACTION),
            CopyTextButtonSpec("Исправить задачу", action=ENGINEER_TASK_EDIT_ACTION),
        )
    )
    return CopyKeyboardSpec(buttons=tuple(buttons))


def build_copy_keyboard_for_preview(preview: dict[str, Any]) -> CopyKeyboardSpec | None:
    """Build copy_text button specs for a parsed order preview."""

    confirmed_text = build_confirmed_copy_text(preview)
    disputed_text = build_disputed_copy_text(preview)
    editable_text = build_editable_copy_text(preview)
    has_disputes = bool(preview.get("disputed_items", []))

    specs: list[CopyTextButtonSpec] = []
    if has_disputes:
        if editable_text:
            specs.append(CopyTextButtonSpec(" Скопировать для исправления", editable_text))
        if disputed_text:
            specs.append(CopyTextButtonSpec(" Скопировать спорные", disputed_text))
    elif confirmed_text:
        specs.append(
            CopyTextButtonSpec(
                label="Скачать Excel для Corel",
                action=COREL_EXCEL_ACTION,
            )
        )
        specs.append(
            CopyTextButtonSpec(
                label="Скачать Файл Малярки",
                action=MALYARKA_FILE_ACTION,
            )
        )
        specs.append(CopyTextButtonSpec(" Скопировать для Corel", confirmed_text))

    buttons: list[CopyTextButtonSpec] = []
    warnings: list[str] = []
    for spec in specs:
        if spec.copy_text is not None and len(spec.copy_text) > MAX_COPY_TEXT_LENGTH:
            warnings.append("Блок слишком длинный для кнопки копирования")
            continue
        buttons.append(spec)

    if not buttons and not warnings:
        return None
    return CopyKeyboardSpec(buttons=tuple(buttons), warnings=tuple(warnings))


def build_confirmed_copy_text(preview: dict[str, Any]) -> str:
    """Return only confirmed Corel rows: height width quantity."""

    return "\n".join(
        f"{item['height']} {item['width']} {item['quantity']}"
        for item in preview.get("confirmed_items", [])
    )


def build_disputed_copy_text(preview: dict[str, Any]) -> str:
    """Return only raw disputed rows."""

    return "\n".join(
        str(item.get("raw", "")) for item in preview.get("disputed_items", [])
    )


def build_clarify_intent_keyboard() -> CopyKeyboardSpec:
    """Build inline keyboard for Free Entry intent clarification.

    Returns 4 buttons: Новый заказ, Идея / обсуждение, Инженер, Отмена.
    Does NOT include an admin button.
    """
    return CopyKeyboardSpec(
        buttons=(
            CopyTextButtonSpec("🧾 Новый заказ", action=CLARIFY_INTENT_ORDER),
            CopyTextButtonSpec("💬 Идея / обсуждение", action=CLARIFY_INTENT_IDEAS),
            CopyTextButtonSpec("🛠 Инженер", action=CLARIFY_INTENT_ENGINEER),
            CopyTextButtonSpec("← Отмена", action=CLARIFY_INTENT_CANCEL),
        )
    )


def build_editable_copy_text(preview: dict[str, Any]) -> str:
    """Return an editable order text for fixing disputed orders."""

    explicit_text = preview.get("editable_copy_text")
    if explicit_text:
        return str(explicit_text)

    lines: list[str] = []
    confirmed_text = build_confirmed_copy_text(preview)
    disputed_text = build_disputed_copy_text(preview)
    if confirmed_text:
        lines.append(confirmed_text)
    if disputed_text:
        lines.append(disputed_text)
    return "\n".join(lines)
