import sys
from pathlib import Path
from zipfile import ZipFile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest

from malyarka_core.exports.corel import build_corel_rows, export_corel_xlsx
from malyarka_core.models import DisputedItem, OrderDraft, OrderItem


def _read_worksheet_xml(path: Path) -> str:
    with ZipFile(path) as archive:
        return archive.read("xl/worksheets/sheet1.xml").decode("utf-8")

def test_corel_rows_start_with_empty_row():
    order = OrderDraft(items=[OrderItem(height=500, width=700, quantity=2)])

    rows = build_corel_rows(order)

    assert rows[0] == []


def test_corel_rows_have_only_height_width_quantity():
    order = OrderDraft(
        items=[
            OrderItem(height=500, width=700, quantity=2),
            OrderItem(height=300, width=400, quantity=1),
        ]
    )

    rows = build_corel_rows(order)

    assert rows[1:] == [[500, 700, 2], [300, 400, 1]]
    assert all(len(row) == 3 for row in rows[1:])


def test_corel_rows_do_not_include_note_or_material():
    order = OrderDraft(
        items=[
            OrderItem(
                height=500,
                width=700,
                quantity=2,
                material="МДФ",
                note="Срочно",
            )
        ]
    )

    rows = build_corel_rows(order)

    assert rows == [[], [500, 700, 2]]
    assert "МДФ" not in rows[1]
    assert "Срочно" not in rows[1]


def test_corel_export_rejects_order_with_disputed_items(tmp_path):
    order = OrderDraft(
        items=[OrderItem(height=500, width=700, quantity=2)],
        disputed_items=[DisputedItem(raw="500 x ?", reason="Неясная ширина")],
    )

    with pytest.raises(ValueError):
        build_corel_rows(order)

    with pytest.raises(ValueError):
        export_corel_xlsx(order, tmp_path / "corel.xlsx")


def test_corel_export_rejects_order_without_items_and_does_not_create_file(tmp_path):
    order = OrderDraft()
    output_path = tmp_path / "corel.xlsx"

    with pytest.raises(ValueError):
        build_corel_rows(order)

    with pytest.raises(ValueError):
        export_corel_xlsx(order, output_path)

    assert not output_path.exists()


def test_corel_xlsx_has_empty_first_row_and_data_from_second_row(tmp_path):
    order = OrderDraft(
        items=[
            OrderItem(height=500, width=700, quantity=2),
            OrderItem(height=300, width=400, quantity=1),
        ]
    )
    output_path = tmp_path / "corel.xlsx"

    export_corel_xlsx(order, output_path)

    worksheet_xml = _read_worksheet_xml(output_path)
    assert '<row r="1"' not in worksheet_xml
    assert '<row r="2"><c r="A2"><v>500</v></c><c r="B2"><v>700</v></c><c r="C2"><v>2</v></c></row>' in worksheet_xml
    assert '<row r="3"><c r="A3"><v>300</v></c><c r="B3"><v>400</v></c><c r="C3"><v>1</v></c></row>' in worksheet_xml
    assert 'D2' not in worksheet_xml


def test_corel_xlsx_has_no_headers_or_extra_item_fields(tmp_path):
    order = OrderDraft(
        items=[
            OrderItem(
                height=500,
                width=700,
                quantity=2,
                material="МДФ",
                color="Белый",
                coating="Матовый",
                milling_type="Ручка J",
                note="Срочно",
            )
        ]
    )
    output_path = tmp_path / "corel.xlsx"

    export_corel_xlsx(order, output_path)

    worksheet_xml = _read_worksheet_xml(output_path)
    assert "Высота" not in worksheet_xml
    assert "Ширина" not in worksheet_xml
    assert "Количество" not in worksheet_xml
    assert "МДФ" not in worksheet_xml
    assert "Белый" not in worksheet_xml
    assert "Срочно" not in worksheet_xml
    assert '<c r="D2"' not in worksheet_xml
    assert '<c r="E2"' not in worksheet_xml


def test_corel_xlsx_is_not_created_when_order_has_disputed_items(tmp_path):
    order = OrderDraft(
        items=[OrderItem(height=500, width=700, quantity=2)],
        disputed_items=[DisputedItem(raw="500 x ?", reason="Неясная ширина")],
    )
    output_path = tmp_path / "corel.xlsx"

    with pytest.raises(ValueError):
        export_corel_xlsx(order, output_path)

    assert not output_path.exists()
