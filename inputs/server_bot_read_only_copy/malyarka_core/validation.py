"""Validation rules for Malyarka order finalization and export."""

from __future__ import annotations

from .models import OrderDraft


def can_finalize_order(order: OrderDraft) -> bool:
    """Return whether a draft can be finalized safely."""

    return bool(order.items) and not order.disputed_items


def validate_order_for_export(order: OrderDraft) -> None:
    """Validate that an order can be used for final exports."""

    if order.disputed_items:
        raise ValueError("Нельзя создать финальные файлы, пока есть спорные строки.")

    if not order.items:
        raise ValueError("Нельзя создать финальные файлы без подтверждённых деталей.")
