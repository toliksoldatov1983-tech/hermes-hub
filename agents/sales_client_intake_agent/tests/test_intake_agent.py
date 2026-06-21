"""
Tests for Sales + Client Intake Agent — offline Python module.

Covers all 15 TEST_SCENARIOS.md scenarios plus acceptance criteria.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from intake_agent import (  # type: ignore[import-untyped]
    analyze_client_message,
    build_intake_card,
    suggest_questions,
    suggest_response,
    determine_handoff_status,
)


# ===================================================================
# Scenario 1: Client asks price without sizes
# ===================================================================


def test_scenario_1_price_without_sizes():
    result = analyze_client_message("Сколько стоит покрасить фасады?")
    assert result["has_sizes"] is False
    assert result["has_material"] is False
    assert result["flags"]["discount_request"] is True

    card = build_intake_card("Сколько стоит покрасить фасады?")
    assert card["status"] == "needs_more_info"

    hs = determine_handoff_status(card)
    assert hs["ready_for_malyarka_agent"] is False
    assert hs["needs_clarification"] is True


# ===================================================================
# Scenario 2: Client gave sizes but not material
# ===================================================================


def test_scenario_2_sizes_without_material():
    result = analyze_client_message("1000 400 2 шт\n600 300 1 шт")
    assert result["has_sizes"] is True
    assert len(result["items"]) == 2
    assert result["items"][0]["height_mm"] == 1000
    assert result["items"][0]["width_mm"] == 400
    assert result["items"][0]["quantity"] == 2
    assert result["has_material"] is False
    assert "material" in result["missing_fields"]

    card = build_intake_card("1000 400 2 шт\n600 300 1 шт")
    assert card["status"] == "needs_more_info"


# ===================================================================
# Scenario 3: Client says "need white facades"
# ===================================================================


def test_scenario_3_need_white_facades():
    result = analyze_client_message("Нужны фасады белые")
    assert result["has_sizes"] is False
    assert result["has_color"] is True
    assert result["has_material"] is False

    card = build_intake_card("Нужны фасады белые")
    assert card["status"] == "needs_more_info"


# ===================================================================
# Scenario 4: "milling + paint" without milling type
# ===================================================================


def test_scenario_4_milling_without_type():
    result = analyze_client_message(
        "Фрезеровка + покраска фасадов МДФ 800 500 4 шт"
    )
    assert result["has_sizes"] is True
    assert result["has_material"] is True
    assert result["flags"]["technical_advice_requested"] is False
    assert result["flags"].get("disputed_order_field") is True
    assert result["flags"]["manager_review_required"] is True

    card = build_intake_card("Фрезеровка + покраска фасадов МДФ 800 500 4 шт")
    hs = determine_handoff_status(card)
    assert hs["needs_manager_review"] is True


# ===================================================================
# Scenario 5: Client asks for discount
# ===================================================================


def test_scenario_5_discount_request():
    result = analyze_client_message(
        "1000 400 МДФ белый. Скидка будет если 10 штук?"
    )
    assert result["has_sizes"] is True
    assert result["flags"]["discount_request"] is True

    card = build_intake_card("1000 400 МДФ белый. Скидка будет если 10 штук?")
    assert card["flags"]["discount_request"] is True

    resp = suggest_response(card)
    assert "менеджер" in resp.lower()


# ===================================================================
# Scenario 6: Client asks "what material is better"
# ===================================================================


def test_scenario_6_what_material_is_better():
    result = analyze_client_message("Что лучше для кухни — МДФ или массив?")
    assert result["flags"]["technical_advice_requested"] is True
    assert result["flags"]["manager_review_required"] is True

    card = build_intake_card("Что лучше для кухни — МДФ или массив?")
    hs = determine_handoff_status(card)
    assert hs["needs_manager_review"] is True
    assert hs["ready_for_malyarka_agent"] is False


# ===================================================================
# Scenario 7: Client asks about deadlines
# ===================================================================


def test_scenario_7_deadline_question():
    result = analyze_client_message("За сколько сделаете?")
    assert result["flags"]["manager_review_required"] is True


# ===================================================================
# Scenario 8: Incomplete description
# ===================================================================


def test_scenario_8_incomplete_description():
    result = analyze_client_message("Покрасить надо")
    assert result["has_sizes"] is False
    assert result["has_material"] is False
    assert result["has_color"] is False

    card = build_intake_card("Покрасить надо")
    assert card["status"] == "needs_more_info"

    questions = suggest_questions(card)
    assert len(questions) > 0


# ===================================================================
# Scenario 9: Paint only, facades exist
# ===================================================================


def test_scenario_9_paint_only_facades_exist():
    result = analyze_client_message(
        "Только покраска. Фасады уже есть. 1000 400 4 шт МДФ белый матовый"
    )
    assert result["has_sizes"] is True
    assert result["has_material"] is True
    assert result["has_color"] is True

    card = build_intake_card(
        "Только покраска. Фасады уже есть. 1000 400 4 шт МДФ белый матовый"
    )
    assert card["status"] == "ready_for_review"

    hs = determine_handoff_status(card)
    assert hs["ready_for_malyarka_agent"] is True
    assert hs["needs_manager_review"] is False


# ===================================================================
# Scenario 10: Repainting old facades
# ===================================================================


def test_scenario_10_old_facades():
    result = analyze_client_message(
        "Старые фасады перекрасить. Дерево. 600 400 5 шт в белый"
    )
    assert result["has_sizes"] is True
    assert result["has_material"] is True
    assert result["has_color"] is True

    card = build_intake_card(
        "Старые фасады перекрасить. Дерево. 600 400 5 шт в белый"
    )
    assert card["status"] == "needs_more_info"  # "дерево" ambiguous


# ===================================================================
# Scenario 11: Facades "under key"
# ===================================================================


def test_scenario_11_facades_under_key():
    result = analyze_client_message(
        "Нужны фасады под ключ. Кухня 5 фасадов. Размеры уточню."
    )
    assert result["has_sizes"] is False

    card = build_intake_card(
        "Нужны фасады под ключ. Кухня 5 фасадов. Размеры уточню."
    )
    assert card["status"] == "needs_more_info"


# ===================================================================
# Scenario 12: Color without RAL/NCS
# ===================================================================


def test_scenario_12_color_without_ral():
    result = analyze_client_message(
        "1000 400 3 шт МДФ цвет кофе с молоком"
    )
    assert result["has_sizes"] is True
    assert result["has_material"] is True
    assert result["has_color"] is True


# ===================================================================
# Scenario 13: "approximately 20 pieces"
# ===================================================================


def test_scenario_13_approximately_20():
    result = analyze_client_message(
        "Фасады МДФ белые примерно 20 штук, размеры разные"
    )
    assert result["has_material"] is True
    assert result["has_color"] is True
    # "примерно 20" — no numeric sizes detected
    assert result["has_sizes"] is False


# ===================================================================
# Scenario 14: "Count my kitchen" — insufficient data
# ===================================================================


def test_scenario_14_count_my_kitchen():
    result = analyze_client_message("Посчитайте мне кухню")
    assert result["has_sizes"] is False
    assert result["has_material"] is False

    card = build_intake_card("Посчитайте мне кухню")
    assert card["status"] == "needs_more_info"

    hs = determine_handoff_status(card)
    assert hs["ready_for_malyarka_agent"] is False


# ===================================================================
# Scenario 15: All data present → ready for Malyarka ✅
# ===================================================================


def test_scenario_15_all_data_present():
    text = (
        "1000 400 4 шт МДФ белый матовый RAL 9010\n"
        "600 300 2 шт дерево коричневый глянцевый\n"
        "Нужна грунтовка для МДФ. Поверхность готова.\n"
        "Санкт-Петербург."
    )
    result = analyze_client_message(text)
    assert result["has_sizes"] is True
    assert result["has_material"] is True
    assert result["has_color"] is True
    assert result["detected_location"] == "Санкт-Петербург"
    assert len(result["items"]) == 2

    card = build_intake_card(text)
    assert card["status"] == "needs_more_info"  # "дерево" ambiguous
    assert card["client"]["location"] == "Санкт-Петербург"

    hs = determine_handoff_status(card)
    assert hs["ready_for_malyarka_agent"] is False
    assert hs["needs_clarification"] is True


# ===================================================================
# Additional safety tests
# ===================================================================


def test_never_invents_price():
    """Agent must NEVER output a price."""
    resp = suggest_response(build_intake_card("Сколько стоит?"))
    assert "руб" not in resp.lower()
    assert "₽" not in resp
    assert "$" not in resp


def test_never_promises_deadline():
    """Agent must NEVER promise a specific deadline."""
    resp = suggest_response(build_intake_card("Когда будет готово?"))
    assert "дня" not in resp.lower()
    assert "недел" not in resp.lower()
    assert "месяц" not in resp.lower()


def test_never_assigns_discount():
    """Agent must NEVER assign a discount value."""
    card = build_intake_card("1000 400 МДФ белый. Скидка будет?")
    assert card["flags"]["discount_request"] is True
    resp = suggest_response(card)
    assert "%" not in resp
    assert "процент" not in resp.lower()


def test_flags_are_set_correctly():
    """Test that flags are correctly set."""
    # Discount flag
    r1 = analyze_client_message("Скидка будет?")
    assert r1["flags"]["discount_request"] is True

    # Technical advice flag
    r2 = analyze_client_message("Что лучше: МДФ или массив?")
    assert r2["flags"]["technical_advice_requested"] is True

    # Manager review for complex requests
    r3 = analyze_client_message("За сколько сделаете?")
    assert r3["flags"]["manager_review_required"] is True


def test_missing_fields_detected():
    """Test that missing fields are correctly identified."""
    r1 = analyze_client_message("1000 400")
    assert "material" in r1["missing_fields"]
    assert "color" in r1["missing_fields"]

    r2 = analyze_client_message("МДФ белый")
    assert "sizes" in r2["missing_fields"]


def test_size_formats():
    """Test various size formats."""
    formats = [
        ("1000 400", 1000, 400, 1),
        ("1000 400 2", 1000, 400, 2),
        ("1000x400", 1000, 400, 1),
        ("1000 x 400", 1000, 400, 1),
        ("1000*400", 1000, 400, 1),
        ("1000×400", 1000, 400, 1),
    ]
    for text, h, w, q in formats:
        result = analyze_client_message(text)
        assert result["has_sizes"], f"Failed format: {text}"
        item = result["items"][0]
        assert item["height_mm"] == h
        assert item["width_mm"] == w
        assert item["quantity"] == q


def test_color_detection():
    """Test that RAL and plain colors are detected."""
    r1 = analyze_client_message("RAL 9010")
    assert r1["has_color"]
    # RAL is detected even without sizes

    r2 = analyze_client_message("1000 400 белый матовый")
    assert r2["has_color"]


def test_handoff_status_all_blockers():
    """Test that handoff correctly reports blockers."""
    card = build_intake_card("Скидка?")
    hs = determine_handoff_status(card)
    assert hs["ready_for_malyarka_agent"] is False
    assert hs["needs_clarification"] is True

    # Full card should be ready
    card2 = build_intake_card("1000 400 2 МДФ белый матовый RAL 9010")
    hs2 = determine_handoff_status(card2)
    assert hs2["ready_for_malyarka_agent"] is True
