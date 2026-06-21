"""Area calculation for confirmed rows only."""


def calculate_area(confirmed_rows, disputed_rows=None):
    """Calculate square meters for confirmed rows and keep disputes excluded."""
    disputed_rows = disputed_rows or []
    calculated_rows = []

    for row in confirmed_rows:
        height_mm = row.get("height_mm", row.get("height"))
        width_mm = row.get("width_mm", row.get("width"))
        quantity = row.get("quantity", 1)
        area_m2 = height_mm * width_mm * quantity / 1_000_000

        calculated_rows.append({
            **row,
            "height_mm": height_mm,
            "width_mm": width_mm,
            "quantity": quantity,
            "area_m2": area_m2,
            "calculation_note": "confirmed_row_only",
        })

    total_area_m2 = sum(row["area_m2"] for row in calculated_rows)
    export_blocked = bool(disputed_rows)

    return {
        "total_area_m2": total_area_m2,
        "calculated_rows": calculated_rows,
        "excluded_disputed_rows": disputed_rows,
        "export_blocked": export_blocked,
        "export_block_reason": "unresolved_disputes" if export_blocked else None,
        "warnings": [],
    }
