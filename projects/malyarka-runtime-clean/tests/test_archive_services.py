import sqlite3
from pathlib import Path

import pytest

from malyarka_core.models import DisputedItem, OrderDraft, OrderItem
from malyarka_core.services.archive import (
    build_archive_snapshot,
    get_next_file_version,
    list_order_files,
    mark_order_file_obsolete,
    register_order_file,
)
from malyarka_core.storage.repository import create_order, initialize_database


def _create_initialized_temp_database(tmp_path: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(tmp_path / "test_orders.db")
    initialize_database(connection)
    return connection


def _create_order_id(connection: sqlite3.Connection) -> int:
    return create_order(connection, OrderDraft())


def test_register_order_file_returns_file_id(tmp_path):
    connection = _create_initialized_temp_database(tmp_path)
    order_id = _create_order_id(connection)

    file_id = register_order_file(connection, order_id, "corel", "archive/order.cdr")

    assert file_id == 1


def test_register_order_file_writes_file_record(tmp_path):
    connection = _create_initialized_temp_database(tmp_path)
    order_id = _create_order_id(connection)

    file_id = register_order_file(
        connection,
        order_id,
        "malyarka",
        "archive/malyarka.xlsx",
        file_version=2,
        status="actual",
    )

    row = connection.execute(
        """
        SELECT order_id, file_type, path, file_version, status
        FROM files
        WHERE id = ?
        """,
        (file_id,),
    ).fetchone()
    assert row == (order_id, "malyarka", "archive/malyarka.xlsx", 2, "actual")


def test_register_order_file_writes_audit_log(tmp_path):
    connection = _create_initialized_temp_database(tmp_path)
    order_id = _create_order_id(connection)

    file_id = register_order_file(connection, order_id, "corel", "archive/order.cdr")

    audit = connection.execute(
        """
        SELECT order_id, action, entity_type, entity_id
        FROM audit_log
        WHERE action = 'register_order_file'
        """
    ).fetchone()
    assert audit == (order_id, "register_order_file", "file", file_id)


def test_list_order_files_returns_files_for_order(tmp_path):
    connection = _create_initialized_temp_database(tmp_path)
    first_order_id = _create_order_id(connection)
    second_order_id = _create_order_id(connection)
    first_file_id = register_order_file(connection, first_order_id, "corel", "1.cdr")
    second_file_id = register_order_file(connection, first_order_id, "malyarka", "1.xlsx")
    register_order_file(connection, second_order_id, "corel", "2.cdr")

    files = list_order_files(connection, first_order_id)

    assert [file["id"] for file in files] == [first_file_id, second_file_id]
    assert [file["order_id"] for file in files] == [first_order_id, first_order_id]


def test_list_order_files_can_filter_actual_status(tmp_path):
    connection = _create_initialized_temp_database(tmp_path)
    order_id = _create_order_id(connection)
    actual_file_id = register_order_file(connection, order_id, "corel", "actual.cdr")
    obsolete_file_id = register_order_file(connection, order_id, "corel", "old.cdr")
    mark_order_file_obsolete(connection, obsolete_file_id)

    files = list_order_files(connection, order_id, status="actual")

    assert [file["id"] for file in files] == [actual_file_id]
    assert all(file["status"] == "actual" for file in files)


def test_mark_order_file_obsolete_changes_status(tmp_path):
    connection = _create_initialized_temp_database(tmp_path)
    order_id = _create_order_id(connection)
    file_id = register_order_file(connection, order_id, "corel", "actual.cdr")

    mark_order_file_obsolete(connection, file_id)

    status = connection.execute(
        "SELECT status FROM files WHERE id = ?",
        (file_id,),
    ).fetchone()[0]
    assert status == "obsolete"


def test_mark_order_file_obsolete_writes_audit_log(tmp_path):
    connection = _create_initialized_temp_database(tmp_path)
    order_id = _create_order_id(connection)
    file_id = register_order_file(connection, order_id, "corel", "actual.cdr")

    mark_order_file_obsolete(connection, file_id)

    audit = connection.execute(
        """
        SELECT order_id, action, entity_type, entity_id
        FROM audit_log
        WHERE action = 'mark_order_file_obsolete'
        """
    ).fetchone()
    assert audit == (order_id, "mark_order_file_obsolete", "file", file_id)


def test_get_next_file_version_returns_one_for_first_file(tmp_path):
    connection = _create_initialized_temp_database(tmp_path)
    order_id = _create_order_id(connection)

    version = get_next_file_version(connection, order_id, "corel")

    assert version == 1


def test_get_next_file_version_increments_existing_versions(tmp_path):
    connection = _create_initialized_temp_database(tmp_path)
    order_id = _create_order_id(connection)
    register_order_file(connection, order_id, "corel", "v1.cdr", file_version=1)
    register_order_file(connection, order_id, "corel", "v2.cdr", file_version=2)
    register_order_file(connection, order_id, "malyarka", "v1.xlsx", file_version=1)

    version = get_next_file_version(connection, order_id, "corel")

    assert version == 3


def test_build_archive_snapshot_excludes_disputed_items():
    order = OrderDraft(
        items=[
            OrderItem(height=500, width=700, quantity=2, material="МДФ"),
            OrderItem(height=300, width=400, quantity=1, color="Белый"),
        ]
    )

    snapshot = build_archive_snapshot(
        order,
        corel_file_path="exports/order.cdr",
        malyarka_file_path="exports/order.xlsx",
    )

    assert "disputed_items" not in snapshot
    assert snapshot["confirmed_items_count"] == 2
    assert snapshot["total_quantity"] == 3
    assert snapshot["total_area_m2"] == pytest.approx(0.82)
    assert snapshot["confirmed_items"] == [
        {
            "height": 500,
            "width": 700,
            "quantity": 2,
            "item_type": None,
            "material": "МДФ",
            "thickness": None,
            "color": None,
            "coating": None,
            "milling_type": None,
            "milling_side": None,
            "painting_side": None,
            "edge_processing": None,
            "group": None,
            "subgroup": None,
            "status": None,
            "note": None,
            "source": None,
            "confidence": None,
            "area_m2": 0.7,
        },
        {
            "height": 300,
            "width": 400,
            "quantity": 1,
            "item_type": None,
            "material": None,
            "thickness": None,
            "color": "Белый",
            "coating": None,
            "milling_type": None,
            "milling_side": None,
            "painting_side": None,
            "edge_processing": None,
            "group": None,
            "subgroup": None,
            "status": None,
            "note": None,
            "source": None,
            "confidence": None,
            "area_m2": 0.12,
        },
    ]
    assert snapshot["file_paths"] == {
        "corel": "exports/order.cdr",
        "malyarka": "exports/order.xlsx",
    }


def test_build_archive_snapshot_rejects_order_with_disputes():
    order = OrderDraft(
        items=[OrderItem(height=500, width=700, quantity=2)],
        disputed_items=[DisputedItem(raw="500 ?", reason="unclear width")],
    )

    with pytest.raises(ValueError):
        build_archive_snapshot(order)


def test_build_archive_snapshot_rejects_empty_order():
    with pytest.raises(ValueError):
        build_archive_snapshot(OrderDraft())


def test_archive_services_use_temporary_database_only(tmp_path, monkeypatch):
    original_connect = sqlite3.connect
    database_path = tmp_path / "test_orders.db"
    connection = original_connect(database_path)
    initialize_database(connection)
    order_id = _create_order_id(connection)

    def fail_if_archive_service_opens_connection(*args, **kwargs):
        raise AssertionError("archive services must use the provided connection only")

    monkeypatch.setattr(sqlite3, "connect", fail_if_archive_service_opens_connection)

    file_id = register_order_file(connection, order_id, "corel", "archive/order.cdr")
    files = list_order_files(connection, order_id)
    mark_order_file_obsolete(connection, file_id)
    next_version = get_next_file_version(connection, order_id, "corel")

    assert database_path.exists()
    assert database_path.name == "test_orders.db"
    assert not (tmp_path / "orders.db").exists()
    assert files[0]["path"] == "archive/order.cdr"
    assert next_version == 2
