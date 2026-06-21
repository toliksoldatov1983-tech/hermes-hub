"""Neutral Corel data model for clean order results only."""


def build_corel_export_model(order_result):
    """Build neutral Corel rows from a clean order result, without file export."""
    status = order_result.get("status")
    disputed_rows = order_result.get("disputed_rows", [])

    if status == "empty_or_invalid":
        return _blocked(status, "empty_or_invalid")
    if disputed_rows:
        return _blocked(status, "disputed_rows_present")
    if order_result.get("export_blocked"):
        return _blocked(status, "export_blocked")
    if status != "clean":
        return _blocked(status, "source_not_clean")

    return {
        "corel_rows": [_corel_row(row) for row in order_result.get("confirmed_rows", [])],
        "export_blocked": False,
        "reason": "ready",
        "source_status": status,
    }


def _corel_row(row):
    return {
        "height_mm": row.get("height_mm", row.get("height")),
        "width_mm": row.get("width_mm", row.get("width")),
        "quantity": row.get("quantity", 1),
    }


def _blocked(status, reason):
    return {
        "corel_rows": [],
        "export_blocked": True,
        "reason": reason,
        "source_status": status,
    }
