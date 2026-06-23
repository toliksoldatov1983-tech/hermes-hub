import sqlite3
from pathlib import Path

import pytest

from malyarka_core.exports.corel import export_corel_xlsx
from malyarka_core.exports.malyarka import export_malyarka_xlsx
from malyarka_core.security.permissions import (
    action_requires_confirmation,
    can_perform_action,
    is_sensitive_action,
)
from malyarka_core.services.archive import (
    build_archive_snapshot,
    get_next_file_version,
    list_order_files,
    mark_order_file_obsolete,
    register_order_file,
)
from malyarka_core.services.orders import (
    build_order_from_text,
    prepare_corel_rows,
    prepare_malyarka_rows,
    save_order_draft,
)
from malyarka_core.storage.reference_data import (
    add_color,
    add_command_alias,
    add_material,
    add_price,
    get_active_price,
    get_setting,
    list_active_command_aliases,
    list_active_colors,
    list_active_materials,
    set_setting,
)
from malyarka_core.storage.repository import get_order_items, initialize_database


def _create_initialized_temp_database(tmp_path: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(tmp_path / "test_orders.db")
    initialize_database(connection)
    return connection


def _audit_actions(connection: sqlite3.Connection) -> list[str]:
    return [
        row[0]
        for row in connection.execute(
            "SELECT action FROM audit_log ORDER BY id"
        ).fetchall()
    ]


def test_full_core_flow_from_text_to_exports_storage_and_archive(tmp_path):
    connection = _create_initialized_temp_database(tmp_path)
    order = build_order_from_text("500 700 2\n300 400\n1000 400 3")

    assert len(order.items) == 3
    assert order.disputed_items == []

    corel_rows = prepare_corel_rows(order)
    assert corel_rows == [[], [500, 700, 2], [300, 400, 1], [1000, 400, 3]]

    malyarka_rows = prepare_malyarka_rows(order)
    assert all(len(row) == 16 for row in malyarka_rows)
    assert malyarka_rows[1][4] == pytest.approx(0.7)
    assert malyarka_rows[2][4] == pytest.approx(0.12)
    assert malyarka_rows[3][4] == pytest.approx(1.2)
    assert malyarka_rows[-1][3] == 6
    assert malyarka_rows[-1][4] == pytest.approx(2.02)

    order_id = save_order_draft(connection, order)

    confirmed_items = get_order_items(connection, order_id)
    assert [(item.height, item.width, item.quantity) for item in confirmed_items] == [
        (500, 700, 2),
        (300, 400, 1),
        (1000, 400, 3),
    ]
    assert connection.execute("SELECT COUNT(*) FROM disputed_items").fetchone()[0] == 0
    assert "create_order" in _audit_actions(connection)
    assert _audit_actions(connection).count("add_order_item") == 3

    corel_path = tmp_path / "corel.xlsx"
    malyarka_path = tmp_path / "malyarka.xlsx"
    assert export_corel_xlsx(order, corel_path) == corel_path
    assert export_malyarka_xlsx(order, malyarka_path) == malyarka_path
    assert corel_path.exists()
    assert malyarka_path.exists()

    corel_version = get_next_file_version(connection, order_id, "corel")
    corel_file_id = register_order_file(
        connection,
        order_id,
        "corel",
        str(corel_path),
        file_version=corel_version,
    )
    malyarka_version = get_next_file_version(connection, order_id, "malyarka")
    malyarka_file_id = register_order_file(
        connection,
        order_id,
        "malyarka",
        str(malyarka_path),
        file_version=malyarka_version,
    )

    assert corel_version == 1
    assert malyarka_version == 1
    assert get_next_file_version(connection, order_id, "corel") == 2
    assert [file["id"] for file in list_order_files(connection, order_id)] == [
        corel_file_id,
        malyarka_file_id,
    ]

    snapshot = build_archive_snapshot(
        order,
        corel_file_path=str(corel_path),
        malyarka_file_path=str(malyarka_path),
    )
    assert snapshot["confirmed_items_count"] == 3
    assert snapshot["total_quantity"] == 6
    assert snapshot["total_area_m2"] == pytest.approx(2.02)
    assert len(snapshot["confirmed_items"]) == 3
    assert "disputed_items" not in snapshot
    assert snapshot["file_paths"] == {
        "corel": str(corel_path),
        "malyarka": str(malyarka_path),
    }


def test_core_flow_with_disputed_items_blocks_exports_and_archive(tmp_path):
    connection = _create_initialized_temp_database(tmp_path)
    order = build_order_from_text("500 700 2\nonly facade")

    assert [(item.height, item.width, item.quantity) for item in order.items] == [
        (500, 700, 2)
    ]
    assert len(order.disputed_items) == 1
    assert order.disputed_items[0].raw == "only facade"

    with pytest.raises(ValueError):
        prepare_corel_rows(order)
    with pytest.raises(ValueError):
        prepare_malyarka_rows(order)
    with pytest.raises(ValueError):
        build_archive_snapshot(order)

    order_id = save_order_draft(connection, order)

    assert connection.execute("SELECT COUNT(*) FROM order_items").fetchone()[0] == 1
    disputed_rows = connection.execute(
        "SELECT order_id, raw FROM disputed_items ORDER BY id"
    ).fetchall()
    assert disputed_rows == [(order_id, "only facade")]


def test_permissions_are_enforced_for_safe_and_sensitive_actions():
    assert can_perform_action("agent", "run_tests") is True
    assert can_perform_action("agent", "finalize_order") is False
    assert can_perform_action("agent", "resolve_disputed_item") is False

    assert can_perform_action("manager", "export_corel") is True
    assert can_perform_action("manager", "export_malyarka") is True

    assert can_perform_action("viewer", "view_order") is True
    assert can_perform_action("viewer", "update_order") is False

    for action in (
        "resolve_disputed_item",
        "finalize_order",
        "archive_order",
        "add_price",
        "set_setting",
        "access_env",
        "access_orders_db",
    ):
        assert is_sensitive_action(action) is True
        assert action_requires_confirmation(action) is True


def test_reference_data_and_settings_integrate_with_temp_database(tmp_path):
    connection = _create_initialized_temp_database(tmp_path)

    material_id = add_material(connection, "MDF", thickness="19", unit="sheet")
    color_id = add_color(connection, "White", code="RAL 9010")
    price_id = add_price(connection, "material", "MDF", 1200.0, "m2")
    setting_id = set_setting(connection, "mode", "manual")
    alias_id = add_command_alias(connection, "create_order", "new order")

    assert list_active_materials(connection) == [
        {
            "id": material_id,
            "name": "MDF",
            "thickness": "19",
            "unit": "sheet",
            "status": "active",
        }
    ]
    assert list_active_colors(connection) == [
        {"id": color_id, "name": "White", "code": "RAL 9010", "status": "active"}
    ]
    assert get_active_price(connection, "material", "MDF") == {
        "id": price_id,
        "price_type": "material",
        "item_name": "MDF",
        "price": 1200.0,
        "unit": "m2",
        "valid_from": None,
        "valid_to": None,
        "status": "active",
    }
    assert get_active_price(connection, "material", "Plywood") is None
    assert get_setting(connection, "mode") == "manual"
    assert list_active_command_aliases(connection, command="create_order") == [
        {
            "id": alias_id,
            "command": "create_order",
            "alias": "new order",
            "status": "active",
        }
    ]

    assert connection.execute(
        "SELECT value FROM settings WHERE id = ?",
        (setting_id,),
    ).fetchone()[0] == "manual"
    assert _audit_actions(connection) == [
        "add_material",
        "add_color",
        "add_price",
        "set_setting",
        "add_command_alias",
    ]


def test_file_accounting_marks_old_files_obsolete(tmp_path):
    connection = _create_initialized_temp_database(tmp_path)
    order = build_order_from_text("500 700 2")
    order_id = save_order_draft(connection, order)

    first_file_id = register_order_file(
        connection,
        order_id,
        "corel",
        str(tmp_path / "corel-v1.xlsx"),
    )
    second_file_id = register_order_file(
        connection,
        order_id,
        "corel",
        str(tmp_path / "corel-v2.xlsx"),
        file_version=2,
    )

    assert [file["id"] for file in list_order_files(connection, order_id)] == [
        first_file_id,
        second_file_id,
    ]

    mark_order_file_obsolete(connection, first_file_id)

    assert connection.execute(
        "SELECT status FROM files WHERE id = ?",
        (first_file_id,),
    ).fetchone()[0] == "obsolete"
    actual_files = list_order_files(connection, order_id, status="actual")
    assert [file["id"] for file in actual_files] == [second_file_id]
    assert all(file["status"] == "actual" for file in actual_files)
