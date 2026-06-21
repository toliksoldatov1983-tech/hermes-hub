"""
Tests for Malyarka Agent — offline Python module.

Covers 15 TEST_SCENARIOS.md + 10 FAKE_INTAKE_CARDS.md + safety checks.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from malyarka_agent import (  # type: ignore[import-untyped]
    analyze_intake_card,
    build_preliminary_result,
    split_confirmed_and_disputed,
    detect_missing_fields,
    detect_blocking_flags,
    determine_order_status,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _card(**overrides):
    """Build a safe fake intake card."""
    return {
        "intake_id": "FAKE-TEST",
        "items": [
            {
                "height_mm": 1000, "width_mm": 400, "quantity": 2,
                "material": "МДФ", "material_confirmed": True,
                "color": "RAL 9010", "finish": "матовый",
            }
        ],
        "material": {"raw": "МДФ", "confirmed": True},
        "color": {"raw": "RAL 9010", "structured": "RAL 9010"},
        "flags": {},
        **overrides,
    }


# ===================================================================
# Scenario 1: No sizes → needs_clarification
# ===================================================================

def test_no_sizes_needs_clarification():
    card = {"items": [], "material": {"raw": "МДФ", "confirmed": True}, "flags": {}}
    r = build_preliminary_result(card)
    s = determine_order_status(card)
    assert s["status"] == "needs_clarification"
    assert r["not_final_order"] is True
    assert r["total_area_m2"] == 0


# ===================================================================
# Scenario 2: No material → needs_clarification
# ===================================================================

def test_no_material_needs_clarification():
    card = {
        "items": [{"height_mm": 1000, "width_mm": 400, "quantity": 2, "material": "", "material_confirmed": False, "color": "белый"}],
        "material": {"raw": None, "confirmed": False},
        "flags": {},
    }
    s = determine_order_status(card)
    assert s["status"] == "needs_clarification"


# ===================================================================
# Scenario 3: Ambiguous material → disputed
# ===================================================================

def test_ambiguous_material_disputed():
    card = {
        "items": [{"height_mm": 1000, "width_mm": 400, "quantity": 2, "material": "дерево", "material_confirmed": False, "color": "белый"}],
        "material": {"raw": "дерево", "confirmed": False},
        "color": {"raw": "белый"},
        "flags": {"material_question": True},
    }
    s = determine_order_status(card)
    assert s["status"] == "blocked_disputed_data"
    split = split_confirmed_and_disputed(card)
    assert len(split["disputed_rows"]) == 1


# ===================================================================
# Scenario 4: Raw color → not converted to RAL
# ===================================================================

def test_raw_color_not_converted_to_ral():
    card = _card(
        items=[{"height_mm": 1000, "width_mm": 400, "quantity": 1, "material": "МДФ", "material_confirmed": True, "color": "белый"}],
        material={"raw": "МДФ", "confirmed": True},
        color={"raw": "белый", "structured": None},
    )
    r = build_preliminary_result(card)
    assert r["confirmed_rows"][0]["color"] == "белый"
    assert "RAL" not in str(r["confirmed_rows"][0]["color"])


# ===================================================================
# Scenario 5: Structured RAL → preserved
# ===================================================================

def test_structured_ral_preserved():
    card = _card(
        items=[{"height_mm": 800, "width_mm": 500, "quantity": 3, "material": "МДФ", "material_confirmed": True, "color": "RAL 9010"}],
        material={"raw": "МДФ", "confirmed": True},
        color={"raw": "RAL 9010", "structured": "RAL 9010"},
    )
    r = build_preliminary_result(card)
    assert r["total_area_m2"] == pytest.approx(1.2)
    assert "RAL 9010" in r["confirmed_rows"][0]["color"]


# ===================================================================
# Scenario 6: Paint only → no milling required
# ===================================================================

def test_paint_only():
    card = _card(
        items=[{"height_mm": 1000, "width_mm": 400, "quantity": 4, "material": "МДФ", "material_confirmed": True, "color": "белый", "finish": "матовый"}],
        material={"raw": "МДФ", "confirmed": True},
        color={"raw": "белый"},
    )
    r = build_preliminary_result(card)
    assert r["total_area_m2"] == pytest.approx(1.6)
    assert r["status"] == "ready_for_human_review"


# ===================================================================
# Scenario 7: Milling without type → disputed
# ===================================================================

def test_milling_without_type_disputed():
    card = _card(
        items=[{"height_mm": 800, "width_mm": 500, "quantity": 4, "material": "МДФ", "material_confirmed": True, "color": "белый"}],
        flags={"technical_advice_requested": True, "manager_review_required": True},
    )
    s = determine_order_status(card)
    assert s["status"] == "blocked_disputed_data"


# ===================================================================
# Scenario 8: Under key → preliminary if enough data
# ===================================================================

def test_under_key_with_data():
    card = _card(
        items=[{"height_mm": 1000, "width_mm": 400, "quantity": 2, "material": "МДФ", "material_confirmed": True, "color": "RAL 9010"}],
    )
    r = build_preliminary_result(card)
    assert r["status"] == "ready_for_human_review"
    assert r["total_area_m2"] == pytest.approx(0.8)


# ===================================================================
# Scenario 9: Old facades → manager_review if flags present
# ===================================================================

def test_old_facades():
    card = _card(
        items=[{"height_mm": 600, "width_mm": 400, "quantity": 5, "material": "дерево", "material_confirmed": False, "color": "белый"}],
        material={"raw": "дерево", "confirmed": False},
        flags={"material_question": True},
    )
    r = build_preliminary_result(card)
    assert len(r["disputed_rows"]) == 1


# ===================================================================
# Scenario 10: Discount → blocked
# ===================================================================

def test_discount_blocks():
    card = _card(
        items=[{"height_mm": 1000, "width_mm": 400, "quantity": 10, "material": "МДФ", "material_confirmed": True, "color": "RAL 9010"}],
        flags={"discount_request": True},
    )
    s = determine_order_status(card)
    assert s["status"] == "blocked_disputed_data"
    blocking = detect_blocking_flags(card)
    assert "discount_request" in blocking
    r = build_preliminary_result(card)
    assert r["manager_review_required"] is True


# ===================================================================
# Scenario 11: Technical advice → blocked
# ===================================================================

def test_technical_advice_blocks():
    card = _card(
        flags={"technical_advice_requested": True, "manager_review_required": True},
    )
    s = determine_order_status(card)
    assert s["status"] == "blocked_disputed_data"


# ===================================================================
# Scenario 12: Manager review → not ready_for_human_review
# ===================================================================

def test_manager_review_blocks():
    card = _card(flags={"manager_review_required": True})
    s = determine_order_status(card)
    assert s["status"] == "blocked_disputed_data"
    r = build_preliminary_result(card)
    assert r["ready_for_human_review"] is False


# ===================================================================
# Scenario 13: Disputed line blocks export
# ===================================================================

def test_disputed_blocks_export():
    card = {
        "items": [
            {"height_mm": 1000, "width_mm": 400, "quantity": 2, "material": "МДФ", "material_confirmed": True, "color": "RAL 9010"},
            {"height_mm": 600, "width_mm": 300, "quantity": 1, "material": "дерево", "material_confirmed": False, "color": "коричневый"},
        ],
        "material": {"raw": "МДФ", "confirmed": True},
        "flags": {"material_question": True},
    }
    r = build_preliminary_result(card)
    assert r["export_blocked"] is True
    split = split_confirmed_and_disputed(card)
    assert len(split["confirmed_rows"]) == 1
    assert len(split["disputed_rows"]) == 1


# ===================================================================
# Scenario 14: Enough data → preliminary / ready
# ===================================================================

def test_enough_data():
    card = {
        "items": [
            {"height_mm": 1000, "width_mm": 400, "quantity": 4, "material": "МДФ", "material_confirmed": True, "color": "RAL 9010", "finish": "матовый"},
            {"height_mm": 600, "width_mm": 300, "quantity": 2, "material": "МДФ", "material_confirmed": True, "color": "RAL 8017", "finish": "глянцевый"},
        ],
        "material": {"raw": "МДФ", "confirmed": True},
        "color": {"raw": "RAL 9010", "structured": "RAL 9010"},
        "flags": {},
    }
    r = build_preliminary_result(card)
    assert r["status"] == "ready_for_human_review"
    assert r["total_area_m2"] == pytest.approx(1.96)
    assert r["export_blocked"] is False


# ===================================================================
# Scenario 15: Not enough data → needs_clarification
# ===================================================================

def test_not_enough_data():
    card = {
        "items": [{"height_mm": 1000, "width_mm": 400, "quantity": 1, "material": "", "material_confirmed": False, "color": ""}],
        "material": {"raw": None, "confirmed": False},
        "flags": {},
    }
    s = determine_order_status(card)
    assert s["status"] == "needs_clarification"
    missing = detect_missing_fields(card)
    assert len(missing) > 0


# ===================================================================
# Test 16: Always not_final_order = True
# ===================================================================

def test_always_not_final_order():
    cards = [
        _card(),
        {"items": [], "material": {}, "flags": {}},
        _card(flags={"discount_request": True}),
    ]
    for card in cards:
        r = build_preliminary_result(card)
        assert r["not_final_order"] is True, f"Failed for card: {card}"


# ===================================================================
# Test 17: Confirmed/disputed always separated
# ===================================================================

def test_confirmed_disputed_separated():
    card = {
        "items": [
            {"height_mm": 1000, "width_mm": 400, "quantity": 1, "material": "МДФ", "material_confirmed": True, "color": "RAL 9010"},
            {"height_mm": 600, "width_mm": 300, "quantity": 1, "material": "дерево", "material_confirmed": False, "color": "белый"},
        ],
        "material": {"raw": "МДФ", "confirmed": True},
        "flags": {"material_question": True},
    }
    split = split_confirmed_and_disputed(card)
    assert len(split["confirmed_rows"]) == 1
    assert len(split["disputed_rows"]) == 1
    assert split["confirmed_rows"][0]["material"] == "МДФ"
    assert split["disputed_rows"][0]["material"] == "дерево"


# ===================================================================
# Test 18: No final price counted
# ===================================================================

def test_no_final_price():
    cards = [
        _card(),
        _card(flags={"discount_request": True}),
        {
            "items": [
                {"height_mm": 1000, "width_mm": 400, "quantity": 4, "material": "МДФ", "material_confirmed": True, "color": "RAL 9010"},
                {"height_mm": 600, "width_mm": 300, "quantity": 2, "material": "МДФ", "material_confirmed": True, "color": "RAL 8017"},
            ],
            "material": {"raw": "МДФ", "confirmed": True},
            "color": {"raw": "RAL 9010", "structured": "RAL 9010"},
            "flags": {},
        },
    ]
    for card in cards:
        r = build_preliminary_result(card)
        assert "price" not in r
        assert "cost" not in r
        assert "стоимость" not in str(r)
        assert "цена" not in str(r)


# ===================================================================
# Fake intake cards (10)
# ===================================================================

def test_fake_001_simple_mdf():
    r = build_preliminary_result({
        "items": [{"height_mm": 1000, "width_mm": 400, "quantity": 2, "material": "МДФ", "material_confirmed": True, "color": "белый", "finish": "матовый"}],
        "material": {"raw": "МДФ", "confirmed": True},
        "color": {"raw": "белый", "structured": None},
        "flags": {},
    })
    assert r["total_area_m2"] == pytest.approx(0.8)
    assert r["status"] == "ready_for_human_review"


def test_fake_002_ambiguous_wood():
    r = build_preliminary_result({
        "items": [{"height_mm": 600, "width_mm": 400, "quantity": 5, "material": "дерево", "material_confirmed": False, "color": "белый"}],
        "material": {"raw": "дерево", "confirmed": False},
        "color": {"raw": "белый", "structured": None},
        "flags": {"material_question": True},
    })
    assert r["export_blocked"] is True


def test_fake_003_with_ral():
    r = build_preliminary_result({
        "items": [{"height_mm": 800, "width_mm": 500, "quantity": 3, "material": "МДФ", "material_confirmed": True, "color": "RAL 9010", "finish": "матовый"}],
        "material": {"raw": "МДФ", "confirmed": True},
        "color": {"raw": "RAL 9010", "structured": "RAL 9010"},
        "flags": {},
    })
    assert r["total_area_m2"] == pytest.approx(1.2)


def test_fake_004_mixed_confirmed_disputed():
    r = build_preliminary_result({
        "items": [
            {"height_mm": 1000, "width_mm": 400, "quantity": 2, "material": "МДФ", "material_confirmed": True, "color": "RAL 9010", "finish": "матовый"},
            {"height_mm": 600, "width_mm": 300, "quantity": 1, "material": "дерево", "material_confirmed": False, "color": "коричневый", "finish": "глянцевый"},
        ],
        "material": {"raw": "МДФ", "confirmed": True},
        "color": {"raw": "RAL 9010", "structured": "RAL 9010"},
        "flags": {"material_question": True},
    })
    assert r["export_blocked"] is True
    assert len(r["confirmed_rows"]) == 1


def test_fake_005_discount():
    r = build_preliminary_result({
        "items": [{"height_mm": 1000, "width_mm": 400, "quantity": 10, "material": "МДФ", "material_confirmed": True, "color": "RAL 9010", "finish": "глянцевый"}],
        "material": {"raw": "МДФ", "confirmed": True},
        "color": {"raw": "RAL 9010", "structured": "RAL 9010"},
        "flags": {"discount_request": True},
    })
    assert r["manager_review_required"] is True


def test_fake_006_technical_advice():
    r = build_preliminary_result({
        "items": [{"height_mm": 800, "width_mm": 500, "quantity": 4, "material": "МДФ", "material_confirmed": True, "color": "белый", "finish": "матовый"}],
        "material": {"raw": "МДФ", "confirmed": True},
        "color": {"raw": "белый", "structured": None},
        "flags": {"technical_advice_requested": True, "manager_review_required": True},
    })
    assert r["export_blocked"] is True


def test_fake_007_manager_review():
    r = build_preliminary_result({
        "items": [{"height_mm": 1200, "width_mm": 600, "quantity": 1, "material": "МДФ", "material_confirmed": True, "color": "RAL 7016", "finish": "матовый"}],
        "material": {"raw": "МДФ", "confirmed": True},
        "color": {"raw": "RAL 7016", "structured": "RAL 7016"},
        "flags": {"manager_review_required": True},
    })
    assert r["ready_for_human_review"] is False


def test_fake_008_paint_only():
    r = build_preliminary_result({
        "items": [{"height_mm": 1000, "width_mm": 400, "quantity": 4, "material": "МДФ", "material_confirmed": True, "color": "белый", "finish": "матовый"}],
        "material": {"raw": "МДФ", "confirmed": True},
        "color": {"raw": "белый", "structured": None},
        "flags": {},
    })
    assert r["total_area_m2"] == pytest.approx(1.6)


def test_fake_009_no_data():
    r = build_preliminary_result({
        "items": [],
        "material": {"raw": None, "confirmed": False},
        "color": {"raw": None, "structured": None},
        "flags": {"manager_review_required": True},
    })
    assert r["status"] == "needs_clarification"


def test_fake_010_all_clean():
    r = build_preliminary_result({
        "items": [
            {"height_mm": 1000, "width_mm": 400, "quantity": 4, "material": "МДФ", "material_confirmed": True, "color": "RAL 9010", "finish": "матовый"},
            {"height_mm": 600, "width_mm": 300, "quantity": 2, "material": "МДФ", "material_confirmed": True, "color": "RAL 8017", "finish": "глянцевый"},
            {"height_mm": 800, "width_mm": 500, "quantity": 1, "material": "МДФ", "material_confirmed": True, "color": "RAL 7016", "finish": "матовый"},
        ],
        "material": {"raw": "МДФ", "confirmed": True},
        "color": {"raw": "RAL 9010", "structured": "RAL 9010"},
        "flags": {},
    })
    assert r["status"] == "ready_for_human_review"
    assert r["export_blocked"] is False
    assert r["total_area_m2"] == pytest.approx(2.36)
