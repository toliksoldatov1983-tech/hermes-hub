"""Area and quantity calculations for Malyarka order items."""

from __future__ import annotations

from collections.abc import Iterable

from .models import OrderItem


def calculate_item_area_m2(item: OrderItem) -> float:
    """Calculate item area in square meters from millimeters and quantity."""

    return item.height * item.width * item.quantity / 1_000_000


def calculate_total_area_m2(items: Iterable[OrderItem]) -> float:
    """Calculate total area in square meters for confirmed items."""

    return sum(calculate_item_area_m2(item) for item in items)


def calculate_total_quantity(items: Iterable[OrderItem]) -> int:
    """Calculate total confirmed item quantity."""

    return sum(item.quantity for item in items)
