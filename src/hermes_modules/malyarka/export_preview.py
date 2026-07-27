from __future__ import annotations

from dataclasses import dataclass

from hermes_modules.malyarka.export_source_policy import classify_export_source
from hermes_modules.malyarka.order_contract import MalyarkaOrder
from hermes_modules.malyarka.schema_contract import export_preview_columns
from hermes_modules.malyarka.synthetic_pricing import build_synthetic_pricing_preview


@dataclass(frozen=True)
class ExportPreview:
    columns: list[str]
    rows: list[dict[str, object]]
    can_write_file: bool
    blocked_reason: str
    source_type: str = "synthetic"


def build_export_preview(order: MalyarkaOrder, *, source_type: str = "synthetic") -> ExportPreview:
    source = classify_export_source(source_type)
    pricing = build_synthetic_pricing_preview(order)
    priced_by_item = {line.item_name: line for line in pricing.lines}
    rows = []
    for index, row in enumerate(order.rows, start=1):
        priced = priced_by_item.get(row.item_name)
        rows.append(
            {
                "row_number": index,
                "item_name": row.item_name,
                "quantity": row.quantity,
                "unit": row.unit,
                "unit_price": priced.unit_price if priced else None,
                "line_total": priced.line_total if priced else None,
                "customer_label": priced.customer_label if priced else "",
                "order_reference": priced.order_reference if priced else "",
                "row_status": row.status.value,
                "dispute_reason": row.dispute_reason,
            }
        )
    return ExportPreview(
        columns=export_preview_columns(),
        rows=rows,
        can_write_file=False,
        blocked_reason=source.reason if source.blocked else "Real Excel/file export requires future explicit approval.",
        source_type=source.source_type,
    )
