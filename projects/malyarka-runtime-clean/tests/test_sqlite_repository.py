import sqlite3
from pathlib import Path

from malyarka_core.models import DisputedItem, OrderDraft, OrderItem
from malyarka_core.storage.repository import (
    add_disputed_item,
    add_order_item,
    create_order,
    get_order_items,
    initialize_database,
    soft_delete_order_item,
)


def _connect_temp_database(tmp_path: Path) -> sqlite3.Connection:
    return sqlite3.connect(tmp_path / "test_orders.db")


def _create_initialized_temp_database(tmp_path: Path) -> sqlite3.Connection:
    connection = _connect_temp_database(tmp_path)
    initialize_database(connection)
    return connection


def test_initialize_database_creates_schema(tmp_path):
    connection = _connect_temp_database(tmp_path)

    initialize_database(connection)

    tables = {
        row[0]
        for row in connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        ).fetchall()
    }
    assert "orders" in tables
    assert "order_items" in tables
    assert "disputed_items" in tables
    assert "audit_log" in tables


def test_create_order_returns_order_id(tmp_path):
    connection = _create_initialized_temp_database(tmp_path)

    order_id = create_order(connection, OrderDraft())

    assert order_id == 1
    assert connection.execute("SELECT COUNT(*) FROM orders").fetchone()[0] == 1


def test_create_order_writes_audit_log(tmp_path):
    connection = _create_initialized_temp_database(tmp_path)

    order_id = create_order(connection, OrderDraft())

    audit = connection.execute(
        "SELECT order_id, action, entity_type, entity_id FROM audit_log"
    ).fetchone()
    assert audit == (order_id, "create_order", "order", order_id)


def test_add_order_item_stores_separate_detail_fields(tmp_path):
    connection = _create_initialized_temp_database(tmp_path)
    order_id = create_order(connection, OrderDraft())
    item = OrderItem(
        height=720,
        width=450,
        quantity=3,
        item_type="facade",
        material="MDF",
        thickness="19",
        color="RAL 9010",
        coating="matte",
        milling_type="frame",
        milling_side="front",
        painting_side="both",
        edge_processing="radius",
        group="kitchen",
        subgroup="upper",
        status="active",
        note="separate fields",
        source="manual",
        confidence=0.98,
    )

    item_id = add_order_item(connection, order_id, item)

    row = connection.execute(
        """
        SELECT
            order_id,
            item_type,
            height,
            width,
            quantity,
            material,
            thickness,
            color,
            coating,
            milling_type,
            milling_side,
            painting_side,
            edge_processing,
            group_name,
            subgroup,
            status,
            note,
            source,
            confidence
        FROM order_items
        WHERE id = ?
        """,
        (item_id,),
    ).fetchone()
    assert row == (
        order_id,
        "facade",
        720,
        450,
        3,
        "MDF",
        "19",
        "RAL 9010",
        "matte",
        "frame",
        "front",
        "both",
        "radius",
        "kitchen",
        "upper",
        "active",
        "separate fields",
        "manual",
        0.98,
    )


def test_add_order_item_writes_audit_log(tmp_path):
    connection = _create_initialized_temp_database(tmp_path)
    order_id = create_order(connection, OrderDraft())

    item_id = add_order_item(connection, order_id, OrderItem(height=720, width=450))

    audit = connection.execute(
        """
        SELECT action, entity_type, entity_id
        FROM audit_log
        WHERE action = 'add_order_item'
        """
    ).fetchone()
    assert audit == ("add_order_item", "order_item", item_id)


def test_add_disputed_item_stores_raw_and_reason(tmp_path):
    connection = _create_initialized_temp_database(tmp_path)
    order_id = create_order(connection, OrderDraft())
    disputed = DisputedItem(
        raw="720 maybe 450 unclear",
        reason="unclear quantity",
        source="manual",
    )

    disputed_item_id = add_disputed_item(connection, order_id, disputed)

    row = connection.execute(
        "SELECT order_id, raw, reason, source FROM disputed_items WHERE id = ?",
        (disputed_item_id,),
    ).fetchone()
    assert row == (order_id, "720 maybe 450 unclear", "unclear quantity", "manual")
    audit = connection.execute(
        "SELECT action, entity_type, entity_id FROM audit_log WHERE entity_id = ?",
        (disputed_item_id,),
    ).fetchall()
    assert ("add_disputed_item", "disputed_item", disputed_item_id) in audit


def test_get_order_items_returns_active_items(tmp_path):
    connection = _create_initialized_temp_database(tmp_path)
    order_id = create_order(connection, OrderDraft())
    add_order_item(connection, order_id, OrderItem(height=720, width=450, status="active"))
    add_order_item(connection, order_id, OrderItem(height=800, width=500, status="cancelled"))

    items = get_order_items(connection, order_id)

    assert items == [OrderItem(height=720, width=450, status="active")]


def test_soft_delete_order_item_marks_item_deleted(tmp_path):
    connection = _create_initialized_temp_database(tmp_path)
    order_id = create_order(connection, OrderDraft())
    item_id = add_order_item(connection, order_id, OrderItem(height=720, width=450))

    soft_delete_order_item(connection, item_id)

    status = connection.execute(
        "SELECT status FROM order_items WHERE id = ?",
        (item_id,),
    ).fetchone()[0]
    assert status == "deleted"
    audit = connection.execute(
        """
        SELECT action, entity_type, entity_id
        FROM audit_log
        WHERE action = 'soft_delete_order_item'
        """
    ).fetchone()
    assert audit == ("soft_delete_order_item", "order_item", item_id)


def test_soft_deleted_items_are_not_returned(tmp_path):
    connection = _create_initialized_temp_database(tmp_path)
    order_id = create_order(connection, OrderDraft())
    deleted_item_id = add_order_item(
        connection,
        order_id,
        OrderItem(height=720, width=450),
    )
    add_order_item(connection, order_id, OrderItem(height=800, width=500))

    soft_delete_order_item(connection, deleted_item_id)

    items = get_order_items(connection, order_id)
    assert items == [OrderItem(height=800, width=500, status="active")]


def test_repository_uses_temporary_database_only(tmp_path):
    database_path = tmp_path / "test_orders.db"
    connection = sqlite3.connect(database_path)

    initialize_database(connection)
    order_id = create_order(connection, OrderDraft())
    add_order_item(connection, order_id, OrderItem(height=720, width=450))

    assert database_path.exists()
    assert database_path.name == "test_orders.db"
    assert not (tmp_path / "orders.db").exists()
