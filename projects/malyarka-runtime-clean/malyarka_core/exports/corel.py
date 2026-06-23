"""Corel export for confirmed Malyarka order items."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from zipfile import ZIP_DEFLATED, ZipFile

from malyarka_core.models import OrderDraft
from malyarka_core.validation import validate_order_for_export


def build_corel_rows(order: OrderDraft) -> list[list[Any]]:
    """Build rows for Corel export: empty first row, then height/width/quantity."""

    validate_order_for_export(order)

    rows: list[list[Any]] = [[]]
    rows.extend([item.height, item.width, item.quantity] for item in order.items)
    return rows


def export_corel_xlsx(order: OrderDraft, path: str | Path) -> Path:
    """Create a Corel .xlsx file without headers, starting data on the second row."""

    rows = build_corel_rows(order)
    output_path = Path(path)

    with ZipFile(output_path, "w", compression=ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", _build_content_types_xml())
        archive.writestr("_rels/.rels", _build_root_relationships_xml())
        archive.writestr("xl/workbook.xml", _build_workbook_xml())
        archive.writestr("xl/_rels/workbook.xml.rels", _build_workbook_relationships_xml())
        archive.writestr("xl/worksheets/sheet1.xml", _build_worksheet_xml(rows))

    return output_path


def _build_worksheet_xml(rows: list[list[Any]]) -> str:
    data_rows: list[str] = []
    for row_index, row in enumerate(rows[1:], start=2):
        cells = []
        for column_index, value in enumerate(row, start=1):
            cell_ref = f"{_column_name(column_index)}{row_index}"
            cells.append(f'<c r="{cell_ref}"><v>{value}</v></c>')
        data_rows.append(f'<row r="{row_index}">{"".join(cells)}</row>')

    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        f'<sheetData>{"".join(data_rows)}</sheetData>'
        '</worksheet>'
    )


def _column_name(column_index: int) -> str:
    name = ""
    while column_index:
        column_index, remainder = divmod(column_index - 1, 26)
        name = chr(65 + remainder) + name
    return name


def _build_content_types_xml() -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
        '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        '</Types>'
    )


def _build_root_relationships_xml() -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
        '</Relationships>'
    )


def _build_workbook_xml() -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        '<sheets><sheet name="Corel" sheetId="1" r:id="rId1"/></sheets>'
        '</workbook>'
    )


def _build_workbook_relationships_xml() -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>'
        '</Relationships>'
    )
