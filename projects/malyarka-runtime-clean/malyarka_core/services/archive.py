"""Archive snapshot and order file accounting services for Malyarka core.

This module only works with caller-provided objects and connections. It never
opens a database path, never creates physical files, and never removes files from
storage. File history is tracked by rows in SQLite, while archive snapshots are
pure in-memory structures built from confirmed order data.
"""

from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict
from typing import Any

from malyarka_core.calculations import (
    calculate_item_area_m2,
    calculate_total_area_m2,
    calculate_total_quantity,
)
from malyarka_core.models import OrderDraft, OrderItem
from malyarka_core.validation import validate_order_for_export


def register_order_file(
    connection: sqlite3.Connection,
    order_id: int,
    file_type: str,
    path: str,
    file_version: int = 1,
    status: str = "actual",
) -> int:
    """Register an order file in SQLite and return the new file id.

    The caller supplies an existing SQLite connection. This function records
    file metadata only; it does not create, read, or modify a physical file.
    """

    cursor = connection.execute(
        """
        INSERT INTO files (order_id, file_type, path, file_version, status)
        VALUES (?, ?, ?, ?, ?)
        """,
        (order_id, file_type, path, file_version, status),
    )
    file_id = int(cursor.lastrowid)
    _write_audit_log(
        connection,
        order_id=order_id,
        action="register_order_file",
        entity_type="file",
        entity_id=file_id,
        new_value=_to_json(
            {
                "file_type": file_type,
                "path": path,
                "file_version": file_version,
                "status": status,
            }
        ),
    )
    connection.commit()
    return file_id


def list_order_files(
    connection: sqlite3.Connection,
    order_id: int,
    status: str | None = None,
) -> list[dict[str, Any]]:
    """Return file records for an order, optionally filtered by status."""

    if status is None:
        cursor = connection.execute(
            """
            SELECT id, order_id, file_type, path, file_version, status, created_at
            FROM files
            WHERE order_id = ?
            ORDER BY id
            """,
            (order_id,),
        )
    else:
        cursor = connection.execute(
            """
            SELECT id, order_id, file_type, path, file_version, status, created_at
            FROM files
            WHERE order_id = ? AND status = ?
            ORDER BY id
            """,
            (order_id, status),
        )

    return [_file_row_to_dict(row) for row in cursor.fetchall()]


def mark_order_file_obsolete(connection: sqlite3.Connection, file_id: int) -> None:
    """Mark a registered file as obsolete without deleting its row or file."""

    row = connection.execute(
        "SELECT order_id, status FROM files WHERE id = ?",
        (file_id,),
    ).fetchone()
    order_id = row[0] if row is not None else None
    old_status = row[1] if row is not None else None

    connection.execute(
        "UPDATE files SET status = 'obsolete' WHERE id = ?",
        (file_id,),
    )
    _write_audit_log(
        connection,
        order_id=order_id,
        action="mark_order_file_obsolete",
        entity_type="file",
        entity_id=file_id,
        old_value=_to_json({"status": old_status}),
        new_value=_to_json({"status": "obsolete"}),
    )
    connection.commit()


def get_next_file_version(
    connection: sqlite3.Connection,
    order_id: int,
    file_type: str,
) -> int:
    """Return the next version number for an order file type."""

    current_max = connection.execute(
        """
        SELECT MAX(file_version)
        FROM files
        WHERE order_id = ? AND file_type = ?
        """,
        (order_id, file_type),
    ).fetchone()[0]
    return int(current_max or 0) + 1


def build_archive_snapshot(
    order: OrderDraft,
    corel_file_path: str | None = None,
    malyarka_file_path: str | None = None,
) -> dict[str, Any]:
    """Build an in-memory archive snapshot from confirmed order data only.

    The snapshot is safe for later archive creation, but this function does not
    write to SQLite and does not create any physical archive files.
    """

    validate_order_for_export(order)

    confirmed_items = [_confirmed_item_to_snapshot(item) for item in order.items]
    file_paths: dict[str, str] = {}
    if corel_file_path is not None:
        file_paths["corel"] = corel_file_path
    if malyarka_file_path is not None:
        file_paths["malyarka"] = malyarka_file_path

    return {
        "confirmed_items_count": len(order.items),
        "total_quantity": calculate_total_quantity(order.items),
        "total_area_m2": calculate_total_area_m2(order.items),
        "confirmed_items": confirmed_items,
        "file_paths": file_paths,
    }


def _confirmed_item_to_snapshot(item: OrderItem) -> dict[str, Any]:
    data = asdict(item)
    data["area_m2"] = calculate_item_area_m2(item)
    return data


def _file_row_to_dict(row: sqlite3.Row | tuple[Any, ...]) -> dict[str, Any]:
    return {
        "id": row[0],
        "order_id": row[1],
        "file_type": row[2],
        "path": row[3],
        "file_version": row[4],
        "status": row[5],
        "created_at": row[6],
    }


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
    return json.dumps(value, ensure_ascii=False, sort_keys=True)
