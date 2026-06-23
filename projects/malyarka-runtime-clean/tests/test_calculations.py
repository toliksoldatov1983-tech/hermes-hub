import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from malyarka_core.calculations import (
    calculate_item_area_m2,
    calculate_total_area_m2,
    calculate_total_quantity,
)
from malyarka_core.models import OrderItem


def test_calculate_row_area_uses_mm_and_quantity():
    item = OrderItem(height=500, width=700, quantity=2)

    assert calculate_item_area_m2(item) == 0.7


def test_calculate_totals_sums_all_items():
    items = [
        OrderItem(height=500, width=700, quantity=2),
        OrderItem(height=1000, width=400, quantity=3),
    ]

    assert calculate_total_area_m2(items) == 1.9
    assert calculate_total_quantity(items) == 5
