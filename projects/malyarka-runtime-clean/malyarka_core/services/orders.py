"""Order service layer for the new Malyarka core.

The service layer coordinates parsing, validation, exports, and repository
operations. It does not duplicate business rules and never opens database paths;
all persistence works only through a caller-provided ``sqlite3.Connection``.
"""

from __future__ import annotations

import sqlite3
from typing import Any

from malyarka_core.exports.corel import build_corel_rows
from malyarka_core.exports.malyarka import build_malyarka_rows
from malyarka_core.models import OrderDraft
from malyarka_core.parsing import parse_sizes_text
from malyarka_core.storage import repository
from malyarka_core.validation import validate_order_for_export


def build_order_from_text(text: str) -> OrderDraft:
    """Build an order draft from multiline text using the existing parser."""

    return parse_sizes_text(text)


def order_has_disputes(order: OrderDraft) -> bool:
    """Return whether an order draft contains disputed item lines."""

    return bool(order.disputed_items)


def ensure_order_can_be_exported(order: OrderDraft) -> None:
    """Raise ``ValueError`` if an order cannot be exported safely."""

    validate_order_for_export(order)


def prepare_corel_rows(order: OrderDraft) -> list[list[Any]]:
    """Prepare Corel rows through the existing Corel export builder."""

    ensure_order_can_be_exported(order)
    return build_corel_rows(order)


def prepare_malyarka_rows(order: OrderDraft) -> list[list[Any]]:
    """Prepare painting workshop rows through the existing Malyarka export builder."""

    ensure_order_can_be_exported(order)
    return build_malyarka_rows(order)


def save_order_draft(connection: sqlite3.Connection, order: OrderDraft) -> int:
    """Persist an order draft and all its confirmed and disputed items."""

    order_id = repository.create_order(connection, order)

    for item in order.items:
        repository.add_order_item(connection, order_id, item)

    for disputed_item in order.disputed_items:
        repository.add_disputed_item(connection, order_id, disputed_item)

    return order_id
