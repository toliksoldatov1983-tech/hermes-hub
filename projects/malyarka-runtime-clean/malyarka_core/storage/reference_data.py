"""Reference data and settings operations for the new Malyarka core.

All functions operate on a caller-provided ``sqlite3.Connection``. This module
never opens a database path and never references the production database file.
"""

from __future__ import annotations

import json
import sqlite3
from typing import Any


_ACTIVE_STATUS = "active"


def add_material(
    connection: sqlite3.Connection,
    name: str,
    thickness: str | None = None,
    unit: str | None = None,
    status: str = _ACTIVE_STATUS,
) -> int:
    """Add a material reference row and return its id."""

    cursor = connection.execute(
        """
        INSERT INTO materials (name, thickness, unit, status)
        VALUES (?, ?, ?, ?)
        """,
        (name, thickness, unit, status),
    )
    material_id = int(cursor.lastrowid)
    _write_audit_log(
        connection,
        action="add_material",
        entity_type="materials",
        entity_id=material_id,
        new_value=_to_json(
            {"name": name, "thickness": thickness, "unit": unit, "status": status}
        ),
    )
    connection.commit()
    return material_id


def list_active_materials(connection: sqlite3.Connection) -> list[dict[str, Any]]:
    """Return active materials ordered by creation id."""

    rows = connection.execute(
        """
        SELECT id, name, thickness, unit, status
        FROM materials
        WHERE status = ?
        ORDER BY id
        """,
        (_ACTIVE_STATUS,),
    ).fetchall()
    return [
        {
            "id": row[0],
            "name": row[1],
            "thickness": row[2],
            "unit": row[3],
            "status": row[4],
        }
        for row in rows
    ]


def add_color(
    connection: sqlite3.Connection,
    name: str,
    code: str | None = None,
    status: str = _ACTIVE_STATUS,
) -> int:
    """Add a color reference row and return its id."""

    cursor = connection.execute(
        """
        INSERT INTO colors (name, code, status)
        VALUES (?, ?, ?)
        """,
        (name, code, status),
    )
    color_id = int(cursor.lastrowid)
    _write_audit_log(
        connection,
        action="add_color",
        entity_type="colors",
        entity_id=color_id,
        new_value=_to_json({"name": name, "code": code, "status": status}),
    )
    connection.commit()
    return color_id


def list_active_colors(connection: sqlite3.Connection) -> list[dict[str, Any]]:
    """Return active colors ordered by creation id."""

    rows = connection.execute(
        """
        SELECT id, name, code, status
        FROM colors
        WHERE status = ?
        ORDER BY id
        """,
        (_ACTIVE_STATUS,),
    ).fetchall()
    return [
        {"id": row[0], "name": row[1], "code": row[2], "status": row[3]}
        for row in rows
    ]


def add_coating(
    connection: sqlite3.Connection,
    name: str,
    status: str = _ACTIVE_STATUS,
) -> int:
    """Add a coating reference row and return its id."""

    cursor = connection.execute(
        """
        INSERT INTO coatings (name, status)
        VALUES (?, ?)
        """,
        (name, status),
    )
    coating_id = int(cursor.lastrowid)
    _write_audit_log(
        connection,
        action="add_coating",
        entity_type="coatings",
        entity_id=coating_id,
        new_value=_to_json({"name": name, "status": status}),
    )
    connection.commit()
    return coating_id


def list_active_coatings(connection: sqlite3.Connection) -> list[dict[str, Any]]:
    """Return active coatings ordered by creation id."""

    rows = connection.execute(
        """
        SELECT id, name, status
        FROM coatings
        WHERE status = ?
        ORDER BY id
        """,
        (_ACTIVE_STATUS,),
    ).fetchall()
    return [{"id": row[0], "name": row[1], "status": row[2]} for row in rows]


def add_milling_type(
    connection: sqlite3.Connection,
    name: str,
    status: str = _ACTIVE_STATUS,
) -> int:
    """Add a milling type reference row and return its id."""

    cursor = connection.execute(
        """
        INSERT INTO milling_types (name, status)
        VALUES (?, ?)
        """,
        (name, status),
    )
    milling_type_id = int(cursor.lastrowid)
    _write_audit_log(
        connection,
        action="add_milling_type",
        entity_type="milling_types",
        entity_id=milling_type_id,
        new_value=_to_json({"name": name, "status": status}),
    )
    connection.commit()
    return milling_type_id


def list_active_milling_types(connection: sqlite3.Connection) -> list[dict[str, Any]]:
    """Return active milling types ordered by creation id."""

    rows = connection.execute(
        """
        SELECT id, name, status
        FROM milling_types
        WHERE status = ?
        ORDER BY id
        """,
        (_ACTIVE_STATUS,),
    ).fetchall()
    return [{"id": row[0], "name": row[1], "status": row[2]} for row in rows]


def add_price(
    connection: sqlite3.Connection,
    price_type: str,
    item_name: str,
    price: float,
    unit: str,
    valid_from: str | None = None,
    valid_to: str | None = None,
    status: str = _ACTIVE_STATUS,
) -> int:
    """Add a price reference row and return its id.

    ``unit`` is mandatory because the numeric price is stored separately from
    code and must always have an explicit unit of measurement.
    """

    if not unit:
        raise ValueError("unit is required for price")

    cursor = connection.execute(
        """
        INSERT INTO prices (
            price_type,
            item_name,
            price,
            unit,
            valid_from,
            valid_to,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (price_type, item_name, price, unit, valid_from, valid_to, status),
    )
    price_id = int(cursor.lastrowid)
    _write_audit_log(
        connection,
        action="add_price",
        entity_type="prices",
        entity_id=price_id,
        new_value=_to_json(
            {
                "price_type": price_type,
                "item_name": item_name,
                "price": price,
                "unit": unit,
                "valid_from": valid_from,
                "valid_to": valid_to,
                "status": status,
            }
        ),
    )
    connection.commit()
    return price_id


def list_active_prices(connection: sqlite3.Connection) -> list[dict[str, Any]]:
    """Return active prices ordered by creation id."""

    rows = connection.execute(
        """
        SELECT id, price_type, item_name, price, unit, valid_from, valid_to, status
        FROM prices
        WHERE status = ?
        ORDER BY id
        """,
        (_ACTIVE_STATUS,),
    ).fetchall()
    return [_price_row_to_dict(row) for row in rows]


def get_active_price(
    connection: sqlite3.Connection,
    price_type: str,
    item_name: str,
) -> dict[str, Any] | None:
    """Return the latest active price for an item or ``None`` when missing."""

    row = connection.execute(
        """
        SELECT id, price_type, item_name, price, unit, valid_from, valid_to, status
        FROM prices
        WHERE status = ?
          AND price_type = ?
          AND item_name = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (_ACTIVE_STATUS, price_type, item_name),
    ).fetchone()
    if row is None:
        return None
    return _price_row_to_dict(row)


def set_setting(
    connection: sqlite3.Connection,
    key: str,
    value: str,
    description: str | None = None,
) -> int:
    """Create or update a setting value stored as TEXT and return its id."""

    text_value = str(value)
    old_row = connection.execute(
        "SELECT id, value, description FROM settings WHERE key = ?",
        (key,),
    ).fetchone()
    old_value = None
    if old_row is not None:
        old_value = _to_json(
            {"key": key, "value": old_row[1], "description": old_row[2]}
        )

    connection.execute(
        """
        INSERT INTO settings (key, value, description)
        VALUES (?, ?, ?)
        ON CONFLICT(key) DO UPDATE SET
            value = excluded.value,
            description = excluded.description
        """,
        (key, text_value, description),
    )
    setting_id = int(
        connection.execute("SELECT id FROM settings WHERE key = ?", (key,)).fetchone()[0]
    )
    _write_audit_log(
        connection,
        action="set_setting",
        entity_type="settings",
        entity_id=setting_id,
        old_value=old_value,
        new_value=_to_json(
            {"key": key, "value": text_value, "description": description}
        ),
    )
    connection.commit()
    return setting_id


def get_setting(
    connection: sqlite3.Connection,
    key: str,
    default: str | None = None,
) -> str | None:
    """Return a setting value or ``default`` when the key is missing."""

    row = connection.execute(
        "SELECT value FROM settings WHERE key = ?",
        (key,),
    ).fetchone()
    if row is None:
        return default
    return row[0]


def add_command_alias(
    connection: sqlite3.Connection,
    command: str,
    alias: str,
    status: str = _ACTIVE_STATUS,
) -> int:
    """Add a command alias for buttons, text commands, or voice commands."""

    cursor = connection.execute(
        """
        INSERT INTO command_aliases (command, alias, status)
        VALUES (?, ?, ?)
        """,
        (command, alias, status),
    )
    alias_id = int(cursor.lastrowid)
    _write_audit_log(
        connection,
        action="add_command_alias",
        entity_type="command_aliases",
        entity_id=alias_id,
        new_value=_to_json({"command": command, "alias": alias, "status": status}),
    )
    connection.commit()
    return alias_id


def list_active_command_aliases(
    connection: sqlite3.Connection,
    command: str | None = None,
) -> list[dict[str, Any]]:
    """Return active command aliases, optionally filtered by command."""

    if command is None:
        rows = connection.execute(
            """
            SELECT id, command, alias, status
            FROM command_aliases
            WHERE status = ?
            ORDER BY id
            """,
            (_ACTIVE_STATUS,),
        ).fetchall()
    else:
        rows = connection.execute(
            """
            SELECT id, command, alias, status
            FROM command_aliases
            WHERE status = ?
              AND command = ?
            ORDER BY id
            """,
            (_ACTIVE_STATUS, command),
        ).fetchall()
    return [
        {"id": row[0], "command": row[1], "alias": row[2], "status": row[3]}
        for row in rows
    ]


def _price_row_to_dict(row: sqlite3.Row | tuple[Any, ...]) -> dict[str, Any]:
    return {
        "id": row[0],
        "price_type": row[1],
        "item_name": row[2],
        "price": row[3],
        "unit": row[4],
        "valid_from": row[5],
        "valid_to": row[6],
        "status": row[7],
    }


def _write_audit_log(
    connection: sqlite3.Connection,
    *,
    action: str,
    entity_type: str,
    entity_id: int | None,
    old_value: str | None = None,
    new_value: str | None = None,
) -> None:
    connection.execute(
        """
        INSERT INTO audit_log (
            order_id,
            action,
            entity_type,
            entity_id,
            old_value,
            new_value
        )
        VALUES (NULL, ?, ?, ?, ?, ?)
        """,
        (action, entity_type, entity_id, old_value, new_value),
    )


def _to_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)
