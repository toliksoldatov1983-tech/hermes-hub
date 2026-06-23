import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from malyarka_core.storage.schema import create_schema


REQUIRED_TABLES = {
    "orders",
    "order_items",
    "disputed_items",
    "materials",
    "colors",
    "coatings",
    "milling_types",
    "prices",
    "files",
    "audit_log",
    "settings",
    "command_aliases",
}


def table_names(connection):
    rows = connection.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table'"
    ).fetchall()
    return {row[0] for row in rows}


def table_columns(connection, table_name):
    rows = connection.execute(f"PRAGMA table_info({table_name})").fetchall()
    return {row[1]: row for row in rows}


def create_temp_schema(tmp_path):
    db_path = tmp_path / "test_orders.db"
    connection = sqlite3.connect(db_path)
    create_schema(connection)
    return connection, db_path


def test_create_schema_creates_required_tables(tmp_path):
    connection, _ = create_temp_schema(tmp_path)

    assert REQUIRED_TABLES <= table_names(connection)

    connection.close()


def test_create_schema_uses_temporary_database(tmp_path):
    connection, db_path = create_temp_schema(tmp_path)

    assert db_path.exists()
    assert db_path.name == "test_orders.db"
    assert db_path.parent == tmp_path

    connection.close()


def test_orders_table_has_order_version_and_status(tmp_path):
    connection, _ = create_temp_schema(tmp_path)
    columns = table_columns(connection, "orders")

    assert columns["status"][2] == "TEXT"
    assert columns["status"][3] == 1
    assert columns["status"][4] == "'draft'"
    assert columns["order_version"][2] == "INTEGER"
    assert columns["order_version"][3] == 1
    assert columns["order_version"][4] == "1"

    connection.close()


def test_order_items_table_has_separate_detail_fields(tmp_path):
    connection, _ = create_temp_schema(tmp_path)
    columns = table_columns(connection, "order_items")

    expected_columns = {
        "item_type",
        "height",
        "width",
        "quantity",
        "material",
        "thickness",
        "color",
        "coating",
        "milling_type",
        "milling_side",
        "painting_side",
        "edge_processing",
        "group_name",
        "subgroup",
        "note",
        "source",
        "confidence",
    }
    assert expected_columns <= columns.keys()
    assert columns["height"][3] == 1
    assert columns["width"][3] == 1
    assert columns["quantity"][4] == "1"

    connection.close()


def test_order_items_table_has_status_for_soft_delete(tmp_path):
    connection, _ = create_temp_schema(tmp_path)
    columns = table_columns(connection, "order_items")

    assert columns["status"][2] == "TEXT"
    assert columns["status"][3] == 1
    assert columns["status"][4] == "'active'"

    connection.close()


def test_disputed_items_table_exists_and_stores_reason(tmp_path):
    connection, _ = create_temp_schema(tmp_path)
    columns = table_columns(connection, "disputed_items")

    assert "disputed_items" in table_names(connection)
    assert columns["raw"][3] == 1
    assert columns["reason"][3] == 1
    assert columns["source"][2] == "TEXT"

    connection.close()


def test_audit_log_table_exists(tmp_path):
    connection, _ = create_temp_schema(tmp_path)
    columns = table_columns(connection, "audit_log")

    assert "audit_log" in table_names(connection)
    assert {"action", "entity_type", "entity_id", "old_value", "new_value"} <= columns.keys()
    assert columns["action"][3] == 1

    connection.close()


def test_prices_table_has_unit_and_valid_dates(tmp_path):
    connection, _ = create_temp_schema(tmp_path)
    columns = table_columns(connection, "prices")

    assert columns["unit"][2] == "TEXT"
    assert columns["unit"][3] == 1
    assert columns["valid_from"][2] == "TEXT"
    assert columns["valid_to"][2] == "TEXT"
    assert columns["status"][4] == "'active'"

    connection.close()


def test_files_table_has_version_and_status(tmp_path):
    connection, _ = create_temp_schema(tmp_path)
    columns = table_columns(connection, "files")

    assert columns["file_version"][2] == "INTEGER"
    assert columns["file_version"][3] == 1
    assert columns["file_version"][4] == "1"
    assert columns["status"][2] == "TEXT"
    assert columns["status"][4] == "'actual'"

    connection.close()


def test_settings_and_command_aliases_tables_exist(tmp_path):
    connection, _ = create_temp_schema(tmp_path)
    settings_columns = table_columns(connection, "settings")
    aliases_columns = table_columns(connection, "command_aliases")

    assert {"key", "value", "description"} <= settings_columns.keys()
    assert settings_columns["key"][3] == 1
    assert settings_columns["value"][3] == 1
    assert {"command", "alias", "status"} <= aliases_columns.keys()
    assert aliases_columns["command"][3] == 1
    assert aliases_columns["alias"][3] == 1
    assert aliases_columns["status"][4] == "'active'"

    connection.close()
