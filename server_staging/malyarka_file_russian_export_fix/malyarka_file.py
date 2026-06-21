"""Minimal Malyarka File export separate from the Corel export."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from malyarka_core.models import DisputedItem, OrderDraft, OrderItem
from malyarka_core.validation import validate_order_for_export

MALYARKA_FILE_HEADERS = [
    "№",
    "Высота",
    "Ширина",
    "Количество",
    "Площадь детали, м²",
    "Площадь строки, м²",
    "Статус",
    "Исходный текст",
    "Причина спора",
]


@dataclass(frozen=True, slots=True)
class MalyarkaFileRow:
    row_number: int
    height: int | None
    width: int | None
    quantity: int | None
    item_area_m2: float | None
    row_area_m2: float | None
    row_status: str
    raw_text: str
    dispute_reason: str | None = None

    def as_list(self) -> list[Any]:
        return [
            self.row_number,
            self.height,
            self.width,
            self.quantity,
            self.item_area_m2,
            self.row_area_m2,
            _translate_row_status(self.row_status),
            self.raw_text,
            self.dispute_reason,
        ]


@dataclass(frozen=True, slots=True)
class MalyarkaFileSummary:
    total_confirmed_quantity: int
    total_confirmed_area_m2: float
    confirmed_count: int
    disputed_count: int
    can_export_final_file: bool


def calculate_single_item_area_m2(item: OrderItem) -> float:
    """Area of one detail in square meters, independent from quantity."""

    return item.height * item.width / 1_000_000


def calculate_row_area_m2(item: OrderItem) -> float:
    """Area of a whole row in square meters, including quantity."""

    return calculate_single_item_area_m2(item) * item.quantity


def build_malyarka_file_rows(order: OrderDraft) -> list[MalyarkaFileRow]:
    """Build preview rows with confirmed and disputed lines."""

    rows: list[MalyarkaFileRow] = []
    row_number = 1

    for item in order.items:
        rows.append(_build_confirmed_row(row_number, item))
        row_number += 1

    for disputed_item in order.disputed_items:
        rows.append(_build_disputed_row(row_number, disputed_item))
        row_number += 1

    return rows


def build_malyarka_file_summary(order: OrderDraft) -> MalyarkaFileSummary:
    """Build totals from confirmed rows only."""

    total_quantity = sum(item.quantity for item in order.items)
    total_area_m2 = sum(calculate_row_area_m2(item) for item in order.items)
    return MalyarkaFileSummary(
        total_confirmed_quantity=total_quantity,
        total_confirmed_area_m2=total_area_m2,
        confirmed_count=len(order.items),
        disputed_count=len(order.disputed_items),
        can_export_final_file=bool(order.items) and not order.disputed_items,
    )


def build_malyarka_file_table(order: OrderDraft) -> list[list[Any]]:
    """Build a table with headers, preview rows, and confirmed totals."""

    summary = build_malyarka_file_summary(order)
    rows = [MALYARKA_FILE_HEADERS.copy()]
    rows.extend(row.as_list() for row in build_malyarka_file_rows(order))
    rows.append(
        [
            "ИТОГО ПОДТВЕРЖДЕНО",
            None,
            None,
            summary.total_confirmed_quantity,
            None,
            summary.total_confirmed_area_m2,
            "итого подтверждено",
            "",
            None,
        ]
    )
    return rows


def export_malyarka_file_xlsx(order: OrderDraft, path: str | Path) -> Path:
    """Create a final Malyarka File .xlsx for clean confirmed orders only."""

    validate_order_for_export(order)
    output_path = Path(path)
    rows = build_malyarka_file_table(order)

    from openpyxl import Workbook

    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Malyarka File"

    for row_index, row in enumerate(rows, start=1):
        for column_index, value in enumerate(row, start=1):
            worksheet.cell(row=row_index, column=column_index, value=value)

    workbook.save(output_path)
    return output_path


def _build_confirmed_row(row_number: int, item: OrderItem) -> MalyarkaFileRow:
    item_area_m2 = calculate_single_item_area_m2(item)
    return MalyarkaFileRow(
        row_number=row_number,
        height=item.height,
        width=item.width,
        quantity=item.quantity,
        item_area_m2=item_area_m2,
        row_area_m2=item_area_m2 * item.quantity,
        row_status="confirmed",
        raw_text=item.source or "",
    )


def _build_disputed_row(row_number: int, item: DisputedItem) -> MalyarkaFileRow:
    return MalyarkaFileRow(
        row_number=row_number,
        height=None,
        width=None,
        quantity=None,
        item_area_m2=None,
        row_area_m2=None,
        row_status="disputed",
        raw_text=item.raw,
        dispute_reason=item.reason,
    )


def _translate_row_status(status: str) -> str:
    return {
        "confirmed": "подтверждено",
        "disputed": "спорно",
        "confirmed_total": "итого подтверждено",
    }.get(status, status)
