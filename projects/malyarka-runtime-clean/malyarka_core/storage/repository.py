"""Repository operations for the new Malyarka SQLite storage layer.

All functions work with a caller-provided ``sqlite3.Connection``. This module
never opens a database path and never references the production database file.
"""

from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict
from typing import Any

from malyarka_core.models import DisputedItem, OrderDraft, OrderItem
from malyarka_core.storage.schema import create_schema


_EXCLUDED_ITEM_STATUSES = ("deleted", "cancelled")


def initialize_database(connection: sqlite3.Connection) -> None:
    """Initialize the SQLite schema on a caller-provided connection."""

    create_schema(connection)


def create_order(connection: sqlite3.Connection, order: OrderDraft) -> int:
    """Create an order row for ``order`` and return its database id."""

    cursor = connection.execute("INSERT INTO orders DEFAULT VALUES")
    order_id = int(cursor.lastrowid)
    _write_audit_log(
        connection,
        order_id=order_id,
        action="create_order",
        entity_type="order",
        entity_id=order_id,
        new_value=_to_json(order),
    )
    connection.commit()
    return order_id


def add_order_item(
    connection: sqlite3.Connection,
    order_id: int,
    item: OrderItem,
) -> int:
    """Store a confirmed order item with all detail properties kept separate."""

    cursor = connection.execute(
        """
        INSERT INTO order_items (
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
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            order_id,
            item.item_type,
            item.height,
            item.width,
            item.quantity,
            item.material,
            item.thickness,
            item.color,
            item.coating,
            item.milling_type,
            item.milling_side,
            item.painting_side,
            item.edge_processing,
            item.group,
            item.subgroup,
            item.status or "active",
            item.note,
            item.source,
            item.confidence,
        ),
    )
    item_id = int(cursor.lastrowid)
    _write_audit_log(
        connection,
        order_id=order_id,
        action="add_order_item",
        entity_type="order_item",
        entity_id=item_id,
        new_value=_to_json(item),
    )
    connection.commit()
    return item_id


def add_disputed_item(
    connection: sqlite3.Connection,
    order_id: int,
    disputed_item: DisputedItem,
) -> int:
    """Store a disputed item line without treating it as confirmed detail data."""

    cursor = connection.execute(
        """
        INSERT INTO disputed_items (order_id, raw, reason, source)
        VALUES (?, ?, ?, ?)
        """,
        (
            order_id,
            disputed_item.raw,
            disputed_item.reason,
            disputed_item.source,
        ),
    )
    disputed_item_id = int(cursor.lastrowid)
    _write_audit_log(
        connection,
        order_id=order_id,
        action="add_disputed_item",
        entity_type="disputed_item",
        entity_id=disputed_item_id,
        new_value=_to_json(disputed_item),
    )
    connection.commit()
    return disputed_item_id


def get_order_items(connection: sqlite3.Connection, order_id: int) -> list[OrderItem]:
    """Return active order items for ``order_id`` as domain models."""

    cursor = connection.execute(
        """
        SELECT
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
        WHERE order_id = ?
          AND status NOT IN (?, ?)
        ORDER BY id
        """,
        (order_id, *_EXCLUDED_ITEM_STATUSES),
    )
    return [
        OrderItem(
            item_type=row[0],
            height=row[1],
            width=row[2],
            quantity=row[3],
            material=row[4],
            thickness=row[5],
            color=row[6],
            coating=row[7],
            milling_type=row[8],
            milling_side=row[9],
            painting_side=row[10],
            edge_processing=row[11],
            group=row[12],
            subgroup=row[13],
            status=row[14],
            note=row[15],
            source=row[16],
            confidence=row[17],
        )
        for row in cursor.fetchall()
    ]


def soft_delete_order_item(connection: sqlite3.Connection, item_id: int) -> None:
    """Mark an order item as deleted without removing its row."""

    row = connection.execute(
        "SELECT order_id, status FROM order_items WHERE id = ?",
        (item_id,),
    ).fetchone()
    order_id = row[0] if row is not None else None
    old_status = row[1] if row is not None else None

    connection.execute(
        """
        UPDATE order_items
        SET status = 'deleted', updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (item_id,),
    )
    _write_audit_log(
        connection,
        order_id=order_id,
        action="soft_delete_order_item",
        entity_type="order_item",
        entity_id=item_id,
        old_value=_to_json({"status": old_status}),
        new_value=_to_json({"status": "deleted"}),
    )
    connection.commit()


def _write_audit_log(
    connection: sqlite3.Connection,
    *,
    order_id: int | None,
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
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (order_id, action, entity_type, entity_id, old_value, new_value),
    )


def _to_json(value: Any) -> str:
    if hasattr(value, "__dataclass_fields__"):
        value = asdict(value)
    return json.dumps(value, ensure_ascii=False, sort_keys=True)
