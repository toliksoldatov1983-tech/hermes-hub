"""
Sales → Malyarka Integration Tests.

Verifies the chain without modifying existing modules.
"""

import sys, os, pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "sales_client_intake_agent", "src"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "malyarka_agent", "src"))

from intake_agent import build_intake_card, determine_handoff_status
from malyarka_agent import build_preliminary_result


def simulate(msg):
    """Run full chain: message → Sales → Malyarka."""
    card = build_intake_card(msg)
    handoff = determine_handoff_status(card)
    if handoff["ready_for_malyarka_agent"]:
        return build_preliminary_result(card)
    return None


# ===================================================================
# Happy path tests
# ===================================================================

def test_chain_all_clear():
    msg = "1000 400 4 шт МДФ белый матовый RAL 9010. Санкт-Петербург."
    r = simulate(msg)
    assert r is not None, "Should pass to Malyarka"
    assert r["status"] == "ready_for_human_review"
    assert r["total_area_m2"] == pytest.approx(1.6)
    assert r["not_final_order"] is True


def test_chain_two_positions():
    msg = "1000 400 2 шт МДФ RAL 9010 матовый\n600 300 1 шт МДФ RAL 8017 глянцевый\nМосква."
    r = simulate(msg)
    assert r is not None
    assert r["total_area_m2"] == pytest.approx(0.98)
    assert len(r["confirmed_rows"]) == 2


def test_chain_paint_only():
    msg = "Только покраска. Фасады уже есть. 1000 400 4 шт МДФ белый матовый"
    r = simulate(msg)
    assert r is not None
    assert r["status"] == "ready_for_human_review"


def test_chain_three_positions():
    msg = "1000 400 4 шт МДФ RAL 9010 матовый\n600 300 2 шт МДФ RAL 8017 глянцевый\n800 500 1 шт МДФ RAL 7016 матовый\nСПб."
    r = simulate(msg)
    assert r is not None
    assert r["total_area_m2"] == pytest.approx(2.36)
    assert len(r["confirmed_rows"]) == 3


# ===================================================================
# Blocked path tests
# ===================================================================

def test_blocked_discount():
    msg = "1000 400 МДФ белый. Скидка будет если 10 штук?"
    r = simulate(msg)
    assert r is None, "Discount should block handoff"


def test_blocked_technical_advice():
    msg = "Фрезеровка + покраска фасадов МДФ 800 500 4 шт"
    r = simulate(msg)
    assert r is None, "Technical advice should block handoff"


def test_blocked_no_sizes():
    msg = "Сколько стоит покрасить фасады?"
    r = simulate(msg)
    assert r is None, "No sizes should block handoff"


def test_blocked_incomplete():
    msg = "Покрасить надо"
    r = simulate(msg)
    assert r is None, "Incomplete should block handoff"


def test_blocked_ambiguous_wood():
    msg = "600 400 5 шт дерево белый"
    r = simulate(msg)
    assert r is None, "Ambiguous wood should block handoff"


def test_blocked_old_facades():
    msg = "Старые фасады перекрасить. Дерево. 600 400 5 шт в белый"
    r = simulate(msg)
    assert r is None, "Old facades with ambiguous wood should block"


# ===================================================================
# Safety invariants
# ===================================================================

def test_all_results_not_final():
    msgs = [
        "1000 400 4 шт МДФ белый матовый RAL 9010. Санкт-Петербург.",
        "1000 400 2 шт МДФ RAL 9010 матовый\n600 300 1 шт МДФ RAL 8017 глянцевый\nМосква.",
        "Только покраска. Фасады уже есть. 1000 400 4 шт МДФ белый матовый",
    ]
    for msg in msgs:
        r = simulate(msg)
        assert r is not None
        assert r["not_final_order"] is True


def test_no_price_in_results():
    msgs = [
        "1000 400 4 шт МДФ белый матовый RAL 9010. Санкт-Петербург.",
        "Только покраска. Фасады уже есть. 1000 400 4 шт МДФ белый матовый",
    ]
    for msg in msgs:
        r = simulate(msg)
        assert r is not None
        assert "price" not in r
        assert "cost" not in r
