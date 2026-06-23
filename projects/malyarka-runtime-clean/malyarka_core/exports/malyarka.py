"""Painting workshop export for confirmed Malyarka order items."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from malyarka_core.calculations import calculate_item_area_m2
from malyarka_core.models import OrderDraft
from malyarka_core.validation import validate_order_for_export

PAINTING_HEADERS = [
    "№",
    "Высота",
    "Ширина",
    "Количество",
    "м²",
    "Тип детали",
    "Материал",
    "Толщина",
    "Цвет",
    "Покрытие",
    "Тип фрезеровки",
    "Сторона покраски",
    "Обработка торца",
    "Группа",
    "Подгруппа",
    "Примечание",
]


def build_malyarka_rows(order: OrderDraft) -> list[list[Any]]:
    """Build painting workshop rows with headers, confirmed items, and totals."""

    validate_order_for_export(order)

    rows: list[list[Any]] = [PAINTING_HEADERS.copy()]
    total_quantity = 0
    total_area_m2 = 0.0

    for item_number, item in enumerate(order.items, start=1):
        item_area_m2 = calculate_item_area_m2(item)
        total_quantity += item.quantity
        total_area_m2 += item_area_m2

        rows.append(
            [
                item_number,
                item.height,
                item.width,
                item.quantity,
                item_area_m2,
                item.item_type,
                item.material,
                item.thickness,
                item.color,
                item.coating,
                item.milling_type,
                item.painting_side,
                item.edge_processing,
                item.group,
                item.subgroup,
                item.note,
            ]
        )

    rows.append(
        [
            "Итого",
            None,
            None,
            total_quantity,
            total_area_m2,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ]
    )
    return rows


def export_malyarka_xlsx(order: OrderDraft, path: str | Path) -> Path:
    """Create a painting workshop .xlsx file with headers, items, and totals."""

    rows = build_malyarka_rows(order)
    output_path = Path(path)

    from openpyxl import Workbook

    workbook = Workbook()
    worksheet = workbook.active

    for row_index, row in enumerate(rows, start=1):
        for column_index, value in enumerate(row, start=1):
            worksheet.cell(row=row_index, column=column_index, value=value)

    workbook.save(output_path)
    return output_path
