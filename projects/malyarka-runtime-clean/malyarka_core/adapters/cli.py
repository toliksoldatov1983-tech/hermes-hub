"""Pure Python CLI adapter for order preview and reporting.

This module intentionally does not import Telegram, aiogram, OpenAI, or Vision
code. It only formats data and delegates business rules to the core services.
"""

from __future__ import annotations

from typing import Any

from malyarka_core.calculations import calculate_total_area_m2, calculate_total_quantity
from malyarka_core.exports.corel import build_corel_rows
from malyarka_core.exports.malyarka import build_malyarka_rows
from malyarka_core.models import DisputedItem, OrderDraft, OrderItem
from malyarka_core.services.archive import build_archive_snapshot
from malyarka_core.services.orders import build_order_from_text
from malyarka_core.validation import validate_order_for_export


def build_cli_report_from_text(text: str) -> dict[str, Any]:
    """Build a full CLI report from plain text order input."""

    order = build_order_from_text(text)

    confirmed_items = [
        {
            "number": index,
            "height": item.height,
            "width": item.width,
            "quantity": item.quantity,
        }
        for index, item in enumerate(order.items, start=1)
    ]
    disputed_items = [
        {"raw": item.raw, "reason": item.reason}
        for item in order.disputed_items
    ]

    export_blocked_reason = _get_export_blocked_reason(order)
    can_export = export_blocked_reason == ""

    if can_export:
        corel_rows = build_corel_rows(order)
        malyarka_rows = build_malyarka_rows(order)
        archive_snapshot = build_archive_snapshot(order)
    else:
        corel_rows = None
        malyarka_rows = None
        archive_snapshot = None

    return {
        "confirmed_items": confirmed_items,
        "disputed_items": disputed_items,
        "confirmed_count": len(confirmed_items),
        "disputed_count": len(disputed_items),
        "total_quantity": calculate_total_quantity(order.items),
        "total_area_m2": calculate_total_area_m2(order.items),
        "can_export": can_export,
        "export_blocked_reason": export_blocked_reason,
        "corel_rows": corel_rows,
        "malyarka_rows": malyarka_rows,
        "archive_snapshot": archive_snapshot,
    }


def format_cli_report(report: dict[str, Any]) -> str:
    """Format a CLI report dict into human-readable text."""

    lines: list[str] = []

    lines.append("ИТОГ")
    lines.append(f"Подтверждённых строк: {report['confirmed_count']}")
    lines.append(f"Спорных строк: {report['disputed_count']}")
    lines.append(f"Всего деталей: {report['total_quantity']}")
    lines.append(f"Общая площадь: {report['total_area_m2']:.3f} м²")

    if report["confirmed_items"]:
        lines.append("")
        lines.append("ПОДТВЕРЖДЁННЫЕ СТРОКИ")
        for item in report["confirmed_items"]:
            lines.append(
                f"{item['number']}. {item['height']} {item['width']} {item['quantity']}"
            )

    if report["disputed_items"]:
        lines.append("")
        lines.append("СПОРНЫЕ СТРОКИ")
        for index, item in enumerate(report["disputed_items"], start=1):
            lines.append(f"{index}. {item['raw']} | {item['reason']}")

    if report["export_blocked_reason"]:
        lines.append("")
        lines.append(f"Причина блокировки: {report['export_blocked_reason']}")

    return "\n".join(lines)


def preview_text_order(text: str) -> str:
    """Build a human-readable preview with Corel rows."""

    report = build_cli_report_from_text(text)
    formatted = format_cli_report(report)

    if report["corel_rows"] is not None:
        corel_text = "\n".join(str(row) for row in report["corel_rows"])
        return f"{formatted}\n\nCOREL ROWS\n{corel_text}"

    return formatted


def _get_export_blocked_reason(order: OrderDraft) -> str:
    try:
        validate_order_for_export(order)
    except ValueError as error:
        return str(error)
    return ""
