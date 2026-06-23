import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest

from malyarka_core.exports.malyarka import (
    PAINTING_HEADERS,
    build_malyarka_rows,
    export_malyarka_xlsx,
)
from malyarka_core.models import DisputedItem, OrderDraft, OrderItem


def test_malyarka_rows_have_expected_headers():
    order = OrderDraft(items=[OrderItem(height=500, width=700, quantity=2)])

    rows = build_malyarka_rows(order)

    assert rows[0] == [
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
    assert rows[0] == PAINTING_HEADERS


def test_malyarka_rows_include_all_16_columns():
    order = OrderDraft(
        items=[
            OrderItem(height=500, width=700, quantity=2),
            OrderItem(height=300, width=400, quantity=1),
        ]
    )

    rows = build_malyarka_rows(order)

    assert all(len(row) == 16 for row in rows)


def test_malyarka_rows_include_item_area_m2():
    order = OrderDraft(items=[OrderItem(height=500, width=700, quantity=2)])

    rows = build_malyarka_rows(order)

    assert rows[1][4] == 0.7


def test_malyarka_rows_include_separate_item_properties():
    order = OrderDraft(
        items=[
            OrderItem(
                height=500,
                width=700,
                quantity=2,
                item_type="Фасад",
                material="МДФ",
                thickness="19",
                color="Белый",
                coating="Матовый",
                milling_type="Ручка J",
                painting_side="Две стороны",
                edge_processing="Покрасить торец",
                group="Кухня",
                subgroup="Верх",
                note="Срочно",
            )
        ]
    )

    rows = build_malyarka_rows(order)

    assert rows[1] == [
        1,
        500,
        700,
        2,
        0.7,
        "Фасад",
        "МДФ",
        "19",
        "Белый",
        "Матовый",
        "Ручка J",
        "Две стороны",
        "Покрасить торец",
        "Кухня",
        "Верх",
        "Срочно",
    ]


def test_malyarka_export_rejects_order_with_disputed_items(tmp_path):
    order = OrderDraft(
        items=[OrderItem(height=500, width=700, quantity=2)],
        disputed_items=[DisputedItem(raw="500 x ?", reason="Неясная ширина")],
    )

    with pytest.raises(ValueError):
        build_malyarka_rows(order)

    with pytest.raises(ValueError):
        export_malyarka_xlsx(order, tmp_path / "malyarka.xlsx")


def test_malyarka_export_rejects_order_without_items(tmp_path):
    order = OrderDraft()

    with pytest.raises(ValueError):
        build_malyarka_rows(order)

    with pytest.raises(ValueError):
        export_malyarka_xlsx(order, tmp_path / "malyarka.xlsx")


def test_malyarka_rows_include_total_quantity_and_total_area():
    order = OrderDraft(
        items=[
            OrderItem(height=500, width=700, quantity=2),
            OrderItem(height=1000, width=400, quantity=3),
        ]
    )

    rows = build_malyarka_rows(order)

    assert rows[-1] == [
        "Итого",
        None,
        None,
        5,
        1.9,
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


def test_malyarka_xlsx_has_headers_items_and_totals(tmp_path):
    order = OrderDraft(
        items=[
            OrderItem(
                height=500,
                width=700,
                quantity=2,
                item_type="Фасад",
                material="МДФ",
                thickness="19",
                color="Белый",
                coating="Матовый",
                milling_type="Ручка J",
                painting_side="Две стороны",
                edge_processing="Покрасить торец",
                group="Кухня",
                subgroup="Верх",
                note="Срочно",
            ),
            OrderItem(height=1000, width=400, quantity=3),
        ]
    )
    output_path = tmp_path / "malyarka.xlsx"
    openpyxl = pytest.importorskip("openpyxl")

    export_malyarka_xlsx(order, output_path)

    workbook = openpyxl.load_workbook(output_path)
    worksheet = workbook.active

    assert [
        worksheet.cell(row=1, column=column).value for column in range(1, 17)
    ] == PAINTING_HEADERS
    assert [worksheet.cell(row=2, column=column).value for column in range(1, 17)] == [
        1,
        500,
        700,
        2,
        0.7,
        "Фасад",
        "МДФ",
        "19",
        "Белый",
        "Матовый",
        "Ручка J",
        "Две стороны",
        "Покрасить торец",
        "Кухня",
        "Верх",
        "Срочно",
    ]
    assert [worksheet.cell(row=4, column=column).value for column in range(1, 6)] == [
        "Итого",
        None,
        None,
        5,
        1.9,
    ]
    assert worksheet.cell(row=1, column=17).value is None
