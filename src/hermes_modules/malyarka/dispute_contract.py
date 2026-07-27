from __future__ import annotations

from hermes_modules.malyarka.order_contract import MalyarkaOrder, MalyarkaOrderRow, RowStatus


def has_blocking_disputes(order_or_rows: MalyarkaOrder | list[MalyarkaOrderRow]) -> bool:
    if isinstance(order_or_rows, MalyarkaOrder):
        return bool(order_or_rows.disputed_rows)
    return any(row.status is RowStatus.DISPUTED for row in order_or_rows)


def dispute_summary(order: MalyarkaOrder) -> list[str]:
    return [f"{row.raw_text}: {row.dispute_reason}" for row in order.disputed_rows]
