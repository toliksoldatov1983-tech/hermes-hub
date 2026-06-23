import sqlite3
from pathlib import Path

from malyarka_core.storage.reference_data import (
    add_color,
    add_coating,
    add_command_alias,
    add_material,
    add_milling_type,
    add_price,
    get_active_price,
    get_setting,
    list_active_colors,
    list_active_coatings,
    list_active_command_aliases,
    list_active_materials,
    list_active_milling_types,
    list_active_prices,
    set_setting,
)
from malyarka_core.storage.schema import create_schema


def _connect_temp_database(tmp_path: Path) -> sqlite3.Connection:
    return sqlite3.connect(tmp_path / "test_orders.db")


def _create_initialized_temp_database(tmp_path: Path) -> sqlite3.Connection:
    connection = _connect_temp_database(tmp_path)
    create_schema(connection)
    return connection


def test_add_material_and_list_active_materials(tmp_path):
    connection = _create_initialized_temp_database(tmp_path)

    material_id = add_material(connection, "MDF", thickness="19", unit="sheet")

    assert list_active_materials(connection) == [
        {
            "id": material_id,
            "name": "MDF",
            "thickness": "19",
            "unit": "sheet",
            "status": "active",
        }
    ]


def test_inactive_material_is_not_listed(tmp_path):
    connection = _create_initialized_temp_database(tmp_path)

    add_material(connection, "MDF", status="inactive")

    assert list_active_materials(connection) == []


def test_add_color_and_list_active_colors(tmp_path):
    connection = _create_initialized_temp_database(tmp_path)

    color_id = add_color(connection, "White", code="RAL 9010")
    add_color(connection, "Old color", status="inactive")

    assert list_active_colors(connection) == [
        {"id": color_id, "name": "White", "code": "RAL 9010", "status": "active"}
    ]


def test_add_coating_and_milling_type(tmp_path):
    connection = _create_initialized_temp_database(tmp_path)

    coating_id = add_coating(connection, "matte")
    milling_type_id = add_milling_type(connection, "frame")

    assert list_active_coatings(connection) == [
        {"id": coating_id, "name": "matte", "status": "active"}
    ]
    assert list_active_milling_types(connection) == [
        {"id": milling_type_id, "name": "frame", "status": "active"}
    ]


def test_add_price_and_get_active_price(tmp_path):
    connection = _create_initialized_temp_database(tmp_path)

    price_id = add_price(connection, "material", "MDF", 1200.5, "m2")

    assert get_active_price(connection, "material", "MDF") == {
        "id": price_id,
        "price_type": "material",
        "item_name": "MDF",
        "price": 1200.5,
        "unit": "m2",
        "valid_from": None,
        "valid_to": None,
        "status": "active",
    }


def test_get_active_price_returns_none_when_missing(tmp_path):
    connection = _create_initialized_temp_database(tmp_path)

    assert get_active_price(connection, "material", "MDF") is None


def test_price_has_unit_and_valid_dates(tmp_path):
    connection = _create_initialized_temp_database(tmp_path)

    price_id = add_price(
        connection,
        "coating",
        "matte",
        250.0,
        "m2",
        valid_from="2026-01-01",
        valid_to="2026-12-31",
    )

    assert list_active_prices(connection) == [
        {
            "id": price_id,
            "price_type": "coating",
            "item_name": "matte",
            "price": 250.0,
            "unit": "m2",
            "valid_from": "2026-01-01",
            "valid_to": "2026-12-31",
            "status": "active",
        }
    ]


def test_set_and_get_setting(tmp_path):
    connection = _create_initialized_temp_database(tmp_path)

    setting_id = set_setting(
        connection,
        "required_order_fields",
        "height,width,quantity",
        description="Required fields for confirmed order items",
    )
    updated_setting_id = set_setting(connection, "required_order_fields", "height,width")

    assert setting_id == updated_setting_id
    assert get_setting(connection, "required_order_fields") == "height,width"


def test_get_setting_returns_default_when_missing(tmp_path):
    connection = _create_initialized_temp_database(tmp_path)

    assert get_setting(connection, "mode", default="manual") == "manual"


def test_add_command_alias_and_list_by_command(tmp_path):
    connection = _create_initialized_temp_database(tmp_path)

    alias_id = add_command_alias(connection, "create_order", "new order")
    add_command_alias(connection, "archive", "archive order")

    assert list_active_command_aliases(connection, command="create_order") == [
        {
            "id": alias_id,
            "command": "create_order",
            "alias": "new order",
            "status": "active",
        }
    ]


def test_list_all_active_command_aliases(tmp_path):
    connection = _create_initialized_temp_database(tmp_path)

    first_alias_id = add_command_alias(connection, "create_order", "new order")
    second_alias_id = add_command_alias(connection, "archive", "archive order")
    add_command_alias(connection, "delete", "remove", status="inactive")

    assert list_active_command_aliases(connection) == [
        {
            "id": first_alias_id,
            "command": "create_order",
            "alias": "new order",
            "status": "active",
        },
        {
            "id": second_alias_id,
            "command": "archive",
            "alias": "archive order",
            "status": "active",
        },
    ]


def test_reference_data_writes_audit_log(tmp_path):
    connection = _create_initialized_temp_database(tmp_path)

    material_id = add_material(connection, "MDF")
    color_id = add_color(connection, "White")
    coating_id = add_coating(connection, "matte")
    milling_type_id = add_milling_type(connection, "frame")
    price_id = add_price(connection, "material", "MDF", 1200.0, "m2")
    setting_id = set_setting(connection, "mode", "manual")
    alias_id = add_command_alias(connection, "create_order", "new order")

    audit_rows = connection.execute(
        """
        SELECT order_id, action, entity_type, entity_id
        FROM audit_log
        ORDER BY id
        """
    ).fetchall()
    assert audit_rows == [
        (None, "add_material", "materials", material_id),
        (None, "add_color", "colors", color_id),
        (None, "add_coating", "coatings", coating_id),
        (None, "add_milling_type", "milling_types", milling_type_id),
        (None, "add_price", "prices", price_id),
        (None, "set_setting", "settings", setting_id),
        (None, "add_command_alias", "command_aliases", alias_id),
    ]


def test_reference_data_uses_temporary_database_only(tmp_path):
    database_path = tmp_path / "test_orders.db"
    connection = sqlite3.connect(database_path)
    create_schema(connection)

    add_material(connection, "MDF")
    add_color(connection, "White")
    add_price(connection, "material", "MDF", 1200.0, "m2")
    set_setting(connection, "mode", "manual")
    add_command_alias(connection, "create_order", "new order")

    assert database_path.exists()
    assert database_path.name == "test_orders.db"
    assert not (tmp_path / "orders.db").exists()
