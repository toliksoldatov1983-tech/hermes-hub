"""Pure Python adapter for a future Telegram bot integration.

This module intentionally does not import Telegram, aiogram, OpenAI, or Vision
code. It only formats data and delegates business rules to the core services.
"""

from __future__ import annotations

import sqlite3
from typing import Any

from malyarka_core.calculations import calculate_total_area_m2, calculate_total_quantity
from malyarka_core.models import DisputedItem, OrderDraft, OrderItem
from malyarka_core.services.orders import (
    build_order_from_text,
    prepare_corel_rows,
    prepare_malyarka_rows,
    save_order_draft,
)
from malyarka_core.validation import validate_order_for_export


def build_order_preview_from_text(text: str) -> dict[str, Any]:
    """Build a user-facing order preview from plain text."""

    order = build_order_from_text(text)
    confirmed_items = [_confirmed_item_to_preview(item) for item in order.items]
    disputed_items = [_disputed_item_to_preview(item) for item in order.disputed_items]
    export_blocked_reason = _get_export_blocked_reason(order)

    return {
        "confirmed_items": confirmed_items,
        "disputed_items": disputed_items,
        "confirmed_count": len(confirmed_items),
        "disputed_count": len(disputed_items),
        "total_quantity": calculate_total_quantity(order.items),
        "total_area_m2": calculate_total_area_m2(order.items),
        "can_export": export_blocked_reason == "",
        "export_blocked_reason": export_blocked_reason,
    }


def prepare_export_rows_from_text(text: str) -> dict[str, list[list[Any]]]:
    """Return Corel and Malyarka export rows without creating files."""

    order = build_order_from_text(text)
    return {
        "corel_rows": prepare_corel_rows(order),
        "malyarka_rows": prepare_malyarka_rows(order),
    }


def save_order_from_text(connection: sqlite3.Connection, text: str) -> dict[str, Any]:
    """Persist an order draft through the provided SQLite connection."""

    order = build_order_from_text(text)
    order_id = save_order_draft(connection, order)
    export_blocked_reason = _get_export_blocked_reason(order)

    return {
        "order_id": order_id,
        "confirmed_count": len(order.items),
        "disputed_count": len(order.disputed_items),
        "can_export": export_blocked_reason == "",
    }


def build_disputed_lines_message(preview: dict[str, Any]) -> str:
    """Build a simple Telegram-ready block with disputed lines."""

    disputed_items = preview["disputed_items"]
    if not disputed_items:
        return ""

    lines = ["СПОРНЫЕ СТРОКИ:"]
    for number, item in enumerate(disputed_items, start=1):
        lines.append(f"{number}. {item['raw']} — {item['reason']}")
    return "\n".join(lines)


def build_confirmed_lines_message(preview: dict[str, Any]) -> str:
    """Build a simple Telegram-ready block with confirmed size lines only."""

    lines = ["ПОДТВЕРЖДЁННЫЕ СТРОКИ:"]
    for number, item in enumerate(preview["confirmed_items"], start=1):
        lines.append(
            f"{number}. {item['height']} {item['width']} {item['quantity']}"
        )
    return "\n".join(lines)


def build_order_summary_message(preview: dict[str, Any]) -> str:
    """Build a short user-facing order summary."""

    export_status = "да" if preview["can_export"] else "нет"
    return "\n".join(
        [
            f"Подтверждённых строк: {preview['confirmed_count']}",
            f"Спорных строк: {preview['disputed_count']}",
            f"Всего деталей: {preview['total_quantity']}",
            f"Общая площадь: {preview['total_area_m2']:.3f} м²",
            f"Можно делать экспорт: {export_status}",
        ]
    )


def _confirmed_item_to_preview(item: OrderItem) -> dict[str, Any]:
    return {
        "height": item.height,
        "width": item.width,
        "quantity": item.quantity,
    }


def _disputed_item_to_preview(item: DisputedItem) -> dict[str, str]:
    return {
        "raw": item.raw,
        "reason": item.reason,
    }


def _get_export_blocked_reason(order: OrderDraft) -> str:
    try:
        validate_order_for_export(order)
    except ValueError as error:
        return str(error)
    return ""
