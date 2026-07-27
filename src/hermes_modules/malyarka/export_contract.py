from __future__ import annotations

from hermes_modules.malyarka.dispute_contract import has_blocking_disputes
from hermes_modules.malyarka.export_source_policy import classify_export_source
from hermes_modules.malyarka.order_contract import MalyarkaOrder


def export_blocked_until_confirmed(
    order: MalyarkaOrder | None = None,
    approved: bool = False,
    *,
    source_type: str = "synthetic",
) -> str:
    source = classify_export_source(source_type)
    if source.blocked:
        return f"BLOCKED: {source.reason}."
    if order is None:
        return "BLOCKED: export requires an order preview."
    if has_blocking_disputes(order):
        return "BLOCKED: disputed rows must be resolved before export."
    if not approved:
        return "BLOCKED: export requires explicit user approval."
    return "READY: export contract can proceed in a future approved block."
