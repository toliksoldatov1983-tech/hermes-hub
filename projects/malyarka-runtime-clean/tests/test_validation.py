import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest

from malyarka_core.models import DisputedItem, OrderDraft, OrderItem
from malyarka_core.validation import can_finalize_order, validate_order_for_export


def test_order_with_disputed_items_cannot_be_finalized():
    order = OrderDraft(
        items=[OrderItem(height=500, width=700, quantity=1)],
        disputed_items=[DisputedItem(raw="неясно", reason="Строка неясна.")],
    )

    assert can_finalize_order(order) is False

    with pytest.raises(ValueError):
        validate_order_for_export(order)


def test_order_without_items_cannot_be_finalized():
    order = OrderDraft()

    assert can_finalize_order(order) is False

    with pytest.raises(ValueError):
        validate_order_for_export(order)


def test_valid_order_can_be_finalized():
    order = OrderDraft(items=[OrderItem(height=500, width=700, quantity=1)])

    assert can_finalize_order(order) is True
    validate_order_for_export(order)
