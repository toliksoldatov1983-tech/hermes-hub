from __future__ import annotations

from hermes_modules.malyarka.order_contract import MalyarkaOrder


def build_preview(order: MalyarkaOrder) -> dict[str, object]:
    return {
        "confirmed": [
            {"item_name": row.item_name, "quantity": row.quantity, "unit": row.unit, "raw_text": row.raw_text}
            for row in order.confirmed_rows
        ],
        "disputed": [
            {"raw_text": row.raw_text, "reason": row.dispute_reason}
            for row in order.disputed_rows
        ],
        "confirmed_count": len(order.confirmed_rows),
        "disputed_count": len(order.disputed_rows),
        "final_ready": order.final_ready,
    }
