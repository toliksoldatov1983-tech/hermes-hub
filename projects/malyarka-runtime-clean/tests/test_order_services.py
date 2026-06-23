import sqlite3
from pathlib import Path

import pytest

from malyarka_core.exports.corel import build_corel_rows
from malyarka_core.exports.malyarka import build_malyarka_rows
from malyarka_core.models import DisputedItem, OrderDraft, OrderItem
from malyarka_core.services.orders import (
    build_order_from_text,
    order_has_disputes,
    prepare_corel_rows,
    prepare_malyarka_rows,
    save_order_draft,
)
from malyarka_core.storage.repository import initialize_database


def _create_initialized_temp_database(tmp_path: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(tmp_path / "service_orders.db")
    initialize_database(connection)
    return connection


def test_build_order_from_text_creates_confirmed_items():
    order = build_order_from_text("500 700 2\n300 400")

    assert order.items == [
        OrderItem(height=500, width=700, quantity=2, source="500 700 2"),
        OrderItem(height=300, width=400, quantity=1, source="300 400"),
    ]
    assert order.disputed_items == []


def test_build_order_from_text_creates_disputed_items():
    order = build_order_from_text("500 700 2\nтолько фасад")

    assert len(order.items) == 1
    assert len(order.disputed_items) == 1
    assert order.disputed_items[0].raw == "только фасад"


def test_disputed_items_do_not_enter_confirmed_items():
    order = build_order_from_text("500 700 2\nтолько фасад")

    assert [item.source for item in order.items] == ["500 700 2"]
    assert all(item.source != "только фасад" for item in order.items)
    assert [disputed.raw for disputed in order.disputed_items] == ["только фасад"]


def test_order_has_disputes_returns_true_for_disputed_order():
    order = OrderDraft(disputed_items=[DisputedItem(raw="500 ?", reason="unclear")])

    assert order_has_disputes(order) is True


def test_prepare_corel_rows_uses_existing_corel_export():
    order = OrderDraft(items=[OrderItem(height=500, width=700, quantity=2)])

    assert prepare_corel_rows(order) == build_corel_rows(order)


def test_prepare_malyarka_rows_uses_existing_malyarka_export():
    order = OrderDraft(items=[OrderItem(height=500, width=700, quantity=2)])

    assert prepare_malyarka_rows(order) == build_malyarka_rows(order)


def test_prepare_exports_reject_order_with_disputes():
    order = OrderDraft(
        items=[OrderItem(height=500, width=700, quantity=2)],
        disputed_items=[DisputedItem(raw="500 ?", reason="unclear")],
    )

    with pytest.raises(ValueError):
        prepare_corel_rows(order)

    with pytest.raises(ValueError):
        prepare_malyarka_rows(order)


def test_prepare_exports_reject_order_without_items():
    order = OrderDraft()

    with pytest.raises(ValueError):
        prepare_corel_rows(order)

    with pytest.raises(ValueError):
        prepare_malyarka_rows(order)


def test_save_order_draft_persists_confirmed_items(tmp_path):
    connection = _create_initialized_temp_database(tmp_path)
    order = OrderDraft(
        items=[
            OrderItem(height=500, width=700, quantity=2, material="МДФ"),
            OrderItem(height=300, width=400, quantity=1, color="Белый"),
        ]
    )

    order_id = save_order_draft(connection, order)

    rows = connection.execute(
        """
        SELECT order_id, height, width, quantity, material, color
        FROM order_items
        ORDER BY id
        """
    ).fetchall()
    assert order_id == 1
    assert rows == [
        (order_id, 500, 700, 2, "МДФ", None),
        (order_id, 300, 400, 1, None, "Белый"),
    ]


def test_save_order_draft_persists_disputed_items(tmp_path):
    connection = _create_initialized_temp_database(tmp_path)
    order = OrderDraft(
        disputed_items=[
            DisputedItem(raw="500 ?", reason="unclear width"),
            DisputedItem(raw="цвет?", reason="not enough dimensions"),
        ]
    )

    order_id = save_order_draft(connection, order)

    rows = connection.execute(
        """
        SELECT order_id, raw, reason
        FROM disputed_items
        ORDER BY id
        """
    ).fetchall()
    assert rows == [
        (order_id, "500 ?", "unclear width"),
        (order_id, "цвет?", "not enough dimensions"),
    ]


def test_save_order_draft_uses_temporary_database_only(tmp_path, monkeypatch):
    original_connect = sqlite3.connect
    temp_database_path = tmp_path / "service_orders.db"
    connection = original_connect(temp_database_path)
    initialize_database(connection)
    order = OrderDraft(items=[OrderItem(height=500, width=700, quantity=2)])

    def fail_if_service_opens_connection(*args, **kwargs):
        raise AssertionError("service must use the provided sqlite3.Connection only")

    monkeypatch.setattr(sqlite3, "connect", fail_if_service_opens_connection)

    order_id = save_order_draft(connection, order)

    assert order_id == 1
    assert connection.execute("SELECT COUNT(*) FROM order_items").fetchone()[0] == 1
    assert temp_database_path.exists()
