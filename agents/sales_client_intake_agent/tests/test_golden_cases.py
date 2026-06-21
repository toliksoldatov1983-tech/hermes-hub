"""
Golden case tests — strict expected-output verification.

Each test verifies that the agent produces exactly the expected
result for a known input (from demo_outputs.md).

No Telegram. No API. No network.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from intake_agent import (  # type: ignore[import-untyped]
    analyze_client_message,
    build_intake_card,
    suggest_response,
    determine_handoff_status,
)


# ===================================================================
# Golden Case 1: Price without sizes
# ===================================================================

def test_golden_1_price_without_sizes():
    text = "Сколько стоит покрасить фасады?"
    a = analyze_client_message(text)
    c = build_intake_card(text)
    h = determine_handoff_status(c)
    r = suggest_response(c)

    assert a["has_sizes"] is False
    assert a["has_material"] is False
    assert a["has_color"] is False
    assert a["flags"]["discount_request"] is True
    assert c["status"] == "needs_more_info"
    assert h["ready_for_malyarka_agent"] is False
    assert h["needs_manager_review"] is True  # discount_request → manager
    # Agent must NOT output a price
    assert "руб" not in r.lower()
    assert "₽" not in r


# ===================================================================
# Golden Case 2: Sizes without material
# ===================================================================

def test_golden_2_sizes_without_material():
    text = "1000 400 2 шт\n600 300 1 шт"
    a = analyze_client_message(text)
    c = build_intake_card(text)
    h = determine_handoff_status(c)

    assert a["has_sizes"] is True
    assert len(a["items"]) == 2
    assert a["items"][0]["height_mm"] == 1000
    assert a["items"][0]["width_mm"] == 400
    assert a["items"][0]["quantity"] == 2
    assert a["has_material"] is False
    assert c["status"] == "needs_more_info"
    assert h["ready_for_malyarka_agent"] is False


# ===================================================================
# Golden Case 3: White facades
# ===================================================================

def test_golden_3_white_facades():
    text = "Нужны фасады белые"
    a = analyze_client_message(text)
    c = build_intake_card(text)
    h = determine_handoff_status(c)

    assert a["has_sizes"] is False
    assert a["has_color"] is True
    assert c["status"] == "needs_more_info"
    assert h["ready_for_malyarka_agent"] is False


# ===================================================================
# Golden Case 4: Milling without type
# ===================================================================

def test_golden_4_milling_without_type():
    text = "Фрезеровка + покраска фасадов МДФ 800 500 4 шт"
    a = analyze_client_message(text)
    c = build_intake_card(text)
    h = determine_handoff_status(c)

    assert a["has_sizes"] is True
    assert a["has_material"] is True
    assert a["flags"]["technical_advice_requested"] is False
    assert a["flags"].get("disputed_order_field") is True
    assert a["flags"]["manager_review_required"] is True
    assert h["needs_manager_review"] is True
    assert h["ready_for_malyarka_agent"] is False


# ===================================================================
# Golden Case 5: Discount
# ===================================================================

def test_golden_5_discount():
    text = "1000 400 МДФ белый. Скидка будет если 10 штук?"
    a = analyze_client_message(text)
    c = build_intake_card(text)
    r = suggest_response(c)

    assert a["flags"]["discount_request"] is True
    assert c["flags"]["discount_request"] is True
    assert "менеджер" in r.lower()
    # Agent must NOT offer a specific discount
    assert "%" not in r


# ===================================================================
# Golden Case 6: What material is better
# ===================================================================

def test_golden_6_what_material():
    text = "Что лучше для кухни — МДФ или массив?"
    a = analyze_client_message(text)
    h = determine_handoff_status(build_intake_card(text))

    assert a["flags"]["technical_advice_requested"] is True
    assert a["flags"]["manager_review_required"] is True
    assert h["needs_manager_review"] is True


# ===================================================================
# Golden Case 7: Deadlines
# ===================================================================

def test_golden_7_deadlines():
    text = "За сколько сделаете?"
    a = analyze_client_message(text)
    r = suggest_response(build_intake_card(text))

    assert a["flags"]["manager_review_required"] is True
    # Must NOT promise a deadline
    assert "дня" not in r.lower()
    assert "недел" not in r.lower()


# ===================================================================
# Golden Case 8: Incomplete
# ===================================================================

def test_golden_8_incomplete():
    text = "Покрасить надо"
    a = analyze_client_message(text)
    c = build_intake_card(text)

    assert a["has_sizes"] is False
    assert a["has_material"] is False
    assert c["status"] == "needs_more_info"


# ===================================================================
# Golden Case 9: Paint only — FULL DATA
# ===================================================================

def test_golden_9_paint_only():
    text = "Только покраска. Фасады уже есть. 1000 400 4 шт МДФ белый матовый"
    a = analyze_client_message(text)
    c = build_intake_card(text)
    h = determine_handoff_status(c)

    assert a["has_sizes"] is True
    assert a["has_material"] is True
    assert a["has_color"] is True
    assert c["status"] == "ready_for_review"
    assert h["ready_for_malyarka_agent"] is True
    assert h["needs_manager_review"] is False


# ===================================================================
# Golden Case 10: Old facades
# ===================================================================

def test_golden_10_old_facades():
    text = "Старые фасады перекрасить. Дерево. 600 400 5 шт в белый"
    a = analyze_client_message(text)
    c = build_intake_card(text)
    h = determine_handoff_status(c)

    assert a["has_sizes"] is True
    assert a["has_material"] is True
    assert a["has_color"] is True
    assert a["material_confirmed"] is False  # "дерево" → ambiguous
    assert c["status"] == "needs_more_info"  # material not confirmed
    assert h["ready_for_malyarka_agent"] is False


# ===================================================================
# Golden Case 11: Under key
# ===================================================================

def test_golden_11_under_key():
    text = "Нужны фасады под ключ. Кухня 5 фасадов. Размеры уточню."
    a = analyze_client_message(text)
    c = build_intake_card(text)

    assert a["has_sizes"] is False
    assert c["status"] == "needs_more_info"


# ===================================================================
# Golden Case 12: Color without RAL
# ===================================================================

def test_golden_12_color_without_ral():
    text = "1000 400 3 шт МДФ цвет кофе с молоком"
    a = analyze_client_message(text)
    c = build_intake_card(text)
    h = determine_handoff_status(c)

    assert a["has_sizes"] is True
    assert a["has_material"] is True
    assert a["has_color"] is True
    assert c["status"] == "ready_for_review"
    assert h["ready_for_malyarka_agent"] is True


# ===================================================================
# Golden Case 13: Approximately 20
# ===================================================================

def test_golden_13_approximately_20():
    text = "Фасады МДФ белые примерно 20 штук, размеры разные"
    a = analyze_client_message(text)
    c = build_intake_card(text)

    assert a["has_material"] is True
    assert a["has_color"] is True
    assert a["has_sizes"] is False  # "примерно 20" — not numeric sizes
    assert c["status"] == "needs_more_info"


# ===================================================================
# Golden Case 14: Count my kitchen
# ===================================================================

def test_golden_14_count_kitchen():
    text = "Посчитайте мне кухню"
    a = analyze_client_message(text)
    c = build_intake_card(text)
    h = determine_handoff_status(c)

    assert a["has_sizes"] is False
    assert c["status"] == "needs_more_info"
    assert h["ready_for_malyarka_agent"] is False


# ===================================================================
# Golden Case 15: ALL DATA — perfect case
# ===================================================================

def test_golden_15_all_data():
    text = (
        "1000 400 4 шт МДФ белый матовый RAL 9010\n"
        "600 300 2 шт дерево коричневый глянцевый\n"
        "Нужна грунтовка для МДФ. Поверхность готова.\n"
        "Санкт-Петербург."
    )
    a = analyze_client_message(text)
    c = build_intake_card(text)
    h = determine_handoff_status(c)
    r = suggest_response(c)

    assert a["has_sizes"] is True
    assert a["has_material"] is True
    assert a["has_color"] is True
    assert a["detected_location"] == "Санкт-Петербург"
    assert len(a["items"]) == 2
    assert a["material_confirmed"] is False  # "дерево" → ambiguous
    assert c["status"] == "needs_more_info"  # material not confirmed
    assert c["client"]["location"] == "Санкт-Петербург"
    assert h["ready_for_malyarka_agent"] is False
    assert h["needs_clarification"] is True


# ===================================================================
# Golden: Safety — never invents price
# ===================================================================

def test_golden_safety_price():
    texts = [
        "Сколько стоит?",
        "Цена?",
        "Почём покраска?",
        "1000 400 МДФ, сколько будет стоить?",
    ]
    for t in texts:
        r = suggest_response(build_intake_card(t))
        assert "руб" not in r.lower(), f"Price leaked in response to: {t}"
        assert "₽" not in r


# ===================================================================
# Golden: Safety — never promises deadline
# ===================================================================

def test_golden_safety_deadline():
    texts = ["Когда будет готово?", "За сколько сделаете?", "Сроки?"]
    for t in texts:
        r = suggest_response(build_intake_card(t))
        assert "дня" not in r.lower(), f"Deadline in response to: {t}"
        assert "недел" not in r.lower()


# ===================================================================
# Golden: Safety — never assigns discount
# ===================================================================

def test_golden_safety_discount():
    texts = ["Скидка будет?", "Сделайте подешевле", "10 штук — скидка?"]
    for t in texts:
        r = suggest_response(build_intake_card(t))
        assert "%" not in r, f"Discount % in response to: {t}"


# ===================================================================
# New: Edge-case tests
# ===================================================================


def test_edge_material_derevo_ambiguous():
    """'дерево' is ambiguous — not confirmed, needs clarification."""
    text = "1000 400 дерево белый"
    a = analyze_client_message(text)
    c = build_intake_card(text)
    h = determine_handoff_status(c)

    assert a["has_material"] is True
    assert a["material_confirmed"] is False
    assert a["material_raw"] == "дерево"
    assert a["flags"]["material_question"] is True
    assert c["status"] == "needs_more_info"  # material not confirmed
    assert h["ready_for_malyarka_agent"] is False
    assert h["needs_clarification"] is True


def test_edge_spb_location_preserved():
    """'СПб' detected and preserved as location."""
    text = "1000 400 МДФ белый матовый RAL 9010. СПб."
    a = analyze_client_message(text)
    c = build_intake_card(text)

    assert a["has_location"] is True
    assert a["detected_location"] == "Санкт-Петербург"
    assert c["client"]["location"] == "Санкт-Петербург"


def test_edge_color_bely_ne_ral():
    """'белый' is color_raw, NOT color_structured (no RAL invented)."""
    text = "1000 400 МДФ белый матовый"
    a = analyze_client_message(text)

    assert a["has_color"] is True
    assert a["color_raw"] == "белый"
    assert a["color_structured"] is None  # NOT invented
    assert "RAL" not in str(a["color_structured"])


def test_edge_ral_as_structured():
    """'RAL 9010' detected as structured color."""
    text = "1000 400 МДФ RAL 9010 матовый"
    a = analyze_client_message(text)

    assert a["has_color"] is True
    assert a["color_structured"] == "RAL 9010"
    assert "RAL 9010" in str(a["color_structured"])


def test_edge_finish_not_technical_decision():
    """'матовый' captured as finish, not as technical_advice."""
    text = "1000 400 МДФ белый матовый"
    a = analyze_client_message(text)

    assert a["surface_finish_raw"] == "матовый"
    assert a["flags"]["technical_advice_requested"] is False
    # finish is descriptive, not a tech recommendation


def test_edge_discount_blocks_malyarka():
    """discount_request → NOT ready_for_malyarka, needs manager."""
    text = "1000 400 МДФ белый матовый RAL 9010. Скидка будет?"
    a = analyze_client_message(text)
    c = build_intake_card(text)
    h = determine_handoff_status(c)

    assert a["flags"]["discount_request"] is True
    assert c["status"] == "ready_for_review"  # data is complete
    assert h["ready_for_malyarka_agent"] is False  # discount blocks
    assert h["needs_manager_review"] is True


def test_edge_almaty_location():
    """'Алматы' detected as location."""
    text = "1000 400 МДФ белый. Алматы."
    a = analyze_client_message(text)
    c = build_intake_card(text)

    assert a["detected_location"] == "Алматы"
    assert c["client"]["location"] == "Алматы"
