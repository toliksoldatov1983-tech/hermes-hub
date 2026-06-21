"""
Tests for Corel Export Agent — offline Python module.
15 scenarios + safety checks.
"""

import sys, os, pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from corel_export_agent import (
    validate_preliminary_result,
    build_export_contract,
    extract_corel_rows,
    detect_export_blockers,
    determine_export_status,
    build_corel_preview,
)


def _result(**overrides):
    """Build a safe preliminary result."""
    return {
        "confirmed_rows": [
            {"height_mm": 1000, "width_mm": 400, "quantity": 2, "material": "МДФ", "color": "RAL 9010", "finish": "матовый"},
        ],
        "disputed_rows": [],
        "total_area_m2": 0.8,
        "export_blocked": False,
        "not_final_order": True,
        "manager_review_required": False,
        "flags": {},
        **overrides,
    }


# ===================================================================
# Scenario 1: Clean result → export ready
# ===================================================================

def test_clean_result_export_ready():
    r = _result()
    c = build_export_contract(r)
    assert c["ready_for_corel"] is True
    assert c["status"] == "ready"
    assert len(c["corel_rows"]) == 1
    assert c["not_final_export"] is True


# ===================================================================
# Scenario 2: Disputed lines → export blocked
# ===================================================================

def test_disputed_blocks_export():
    r = _result(disputed_rows=[{"height_mm": 600, "width_mm": 300, "quantity": 1, "material": "дерево", "dispute_reason": "material_ambiguous"}])
    c = build_export_contract(r)
    assert c["ready_for_corel"] is False
    assert "disputed_rows_present" in c["export_blockers"]


# ===================================================================
# Scenario 3: export_blocked=true → blocked
# ===================================================================

def test_export_blocked_flag():
    r = _result(export_blocked=True)
    c = build_export_contract(r)
    assert c["ready_for_corel"] is False


# ===================================================================
# Scenario 4: Missing height → blocked
# ===================================================================

def test_missing_height():
    r = _result(confirmed_rows=[{"width_mm": 400, "quantity": 1, "material": "МДФ", "color": "белый"}])
    blockers = detect_export_blockers(r)
    assert "incomplete_dimensions" in blockers


# ===================================================================
# Scenario 5: Missing width → blocked
# ===================================================================

def test_missing_width():
    r = _result(confirmed_rows=[{"height_mm": 1000, "quantity": 1, "material": "МДФ", "color": "белый"}])
    blockers = detect_export_blockers(r)
    assert "incomplete_dimensions" in blockers


# ===================================================================
# Scenario 6: Missing quantity → blocked
# ===================================================================

def test_missing_quantity():
    r = _result(confirmed_rows=[{"height_mm": 1000, "width_mm": 400, "material": "МДФ", "color": "белый"}])
    blockers = detect_export_blockers(r)
    assert "missing_quantity" in blockers


# ===================================================================
# Scenario 7: Zero quantity → still extracted as 0 (blocked)
# ===================================================================

def test_zero_quantity_blocked():
    r = _result(confirmed_rows=[{"height_mm": 1000, "width_mm": 400, "quantity": 0, "material": "МДФ", "color": "белый"}])
    blockers = detect_export_blockers(r)
    assert len(blockers) > 0


# ===================================================================
# Scenario 8: Only confirmed exported
# ===================================================================

def test_only_confirmed_exported():
    r = _result(
        confirmed_rows=[{"height_mm": 1000, "width_mm": 400, "quantity": 2, "material": "МДФ", "color": "RAL 9010"}],
        disputed_rows=[{"height_mm": 600, "width_mm": 300, "quantity": 1, "material": "дерево"}],
    )
    rows = extract_corel_rows(r)
    assert len(rows) == 1
    assert rows[0]["material"] == "МДФ"


# ===================================================================
# Scenario 9: Disputed never exported
# ===================================================================

def test_disputed_not_in_corel_rows():
    r = _result(disputed_rows=[{"height_mm": 600, "width_mm": 300, "quantity": 1, "material": "дерево"}])
    c = build_export_contract(r)
    assert c["ready_for_corel"] is False
    assert len(c["corel_rows"]) == 0


# ===================================================================
# Scenario 10: not_final_order=true preserved
# ===================================================================

def test_not_final_order_preserved():
    r = _result()
    c = build_export_contract(r)
    assert c["not_final_export"] is True
    v = validate_preliminary_result(r)
    assert v["valid"] is True


# ===================================================================
# Scenario 11: No final price
# ===================================================================

def test_no_final_price():
    r = _result()
    c = build_export_contract(r)
    assert "price" not in c
    assert "cost" not in c
    assert "стоимость" not in str(c)


# ===================================================================
# Scenario 12: Manager review → blocked
# ===================================================================

def test_manager_review_blocks():
    r = _result(manager_review_required=True)
    c = build_export_contract(r)
    assert c["ready_for_corel"] is False


# ===================================================================
# Scenario 13: Clean → contract ready
# ===================================================================

def test_clean_contract_ready():
    r = _result(
        confirmed_rows=[
            {"height_mm": 1000, "width_mm": 400, "quantity": 4, "material": "МДФ", "color": "RAL 9010", "finish": "матовый"},
            {"height_mm": 600, "width_mm": 300, "quantity": 2, "material": "МДФ", "color": "RAL 8017", "finish": "глянцевый"},
        ],
        total_area_m2=1.96,
    )
    c = build_export_contract(r)
    assert c["ready_for_corel"] is True
    assert len(c["corel_rows"]) == 2


# ===================================================================
# Scenario 14: Blocked disputed → contract blocked
# ===================================================================

def test_blocked_disputed():
    r = _result(
        disputed_rows=[{"height_mm": 600, "width_mm": 300, "quantity": 1, "material": "дерево"}],
        export_blocked=True,
    )
    s = determine_export_status(r)
    assert s["can_export"] is False


# ===================================================================
# Scenario 15: Preview contains only H/W/Q
# ===================================================================

def test_preview_format():
    r = _result()
    c = build_export_contract(r)
    preview = c["preview"]
    assert "Corel Export Preview" in preview
    assert "not_final_export" in preview
    # Preview uses H×W order
    assert "1000×400" in preview


# ===================================================================
# Additional tests
# ===================================================================

def test_corel_row_format():
    """Corel rows use order: height_mm, width_mm, quantity."""
    r = _result()
    rows = extract_corel_rows(r)
    # Verify order: height first, width second, quantity third
    assert rows[0]["height_mm"] == 1000
    assert rows[0]["width_mm"] == 400
    assert rows[0]["quantity"] == 2
    # Verify keys order
    keys = list(rows[0].keys())
    assert keys[1] == "height_mm", f"Expected height_mm at position 1, got {keys}"
    assert keys[2] == "width_mm", f"Expected width_mm at position 2, got {keys}"
    assert keys[3] == "quantity", f"Expected quantity at position 3, got {keys}"


def test_empty_result():
    r = {"confirmed_rows": [], "disputed_rows": [], "not_final_order": True}
    c = build_export_contract(r)
    assert c["ready_for_corel"] is False
    assert len(c["corel_rows"]) == 0


def test_multiple_positions():
    r = _result(confirmed_rows=[
        {"height_mm": 1000, "width_mm": 400, "quantity": 4, "material": "МДФ", "color": "RAL 9010"},
        {"height_mm": 600, "width_mm": 300, "quantity": 2, "material": "МДФ", "color": "RAL 8017"},
        {"height_mm": 800, "width_mm": 500, "quantity": 1, "material": "МДФ", "color": "RAL 7016"},
    ])
    rows = extract_corel_rows(r)
    assert len(rows) == 3
