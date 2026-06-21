"""
Full-Chain Integration Tests: Sales → Malyarka → Corel Export.
"""

import sys, os, pytest

BASE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(BASE, "..", "..", "sales_client_intake_agent", "src"))
sys.path.insert(0, os.path.join(BASE, "..", "..", "malyarka_agent", "src"))
sys.path.insert(0, os.path.join(BASE, "..", "..", "corel_export_agent", "src"))

from intake_agent import build_intake_card, determine_handoff_status
from malyarka_agent import build_preliminary_result
from corel_export_agent import build_export_contract, extract_corel_rows


def run_chain(msg):
    """Run full chain. Returns (stage, result) or (blocked_stage, None)."""
    card = build_intake_card(msg)
    handoff = determine_handoff_status(card)
    if not handoff["ready_for_malyarka_agent"]:
        return ("sales_blocked", None)

    malyarka_result = build_preliminary_result(card)
    if malyarka_result["status"] != "ready_for_human_review" or malyarka_result["export_blocked"]:
        return ("malyarka_blocked", malyarka_result)

    corel_contract = build_export_contract(malyarka_result)
    return ("corel", corel_contract)


# ===================================================================
# Happy path
# ===================================================================

def test_full_chain_single_position():
    msg = "1000 400 4 шт МДФ белый матовый RAL 9010. Санкт-Петербург."
    stage, result = run_chain(msg)
    assert stage == "corel"
    assert result["ready_for_corel"] is True
    assert result["not_final_export"] is True
    rows = result["corel_rows"]
    assert len(rows) == 1
    assert rows[0]["height_mm"] == 1000
    assert rows[0]["width_mm"] == 400


def test_full_chain_two_positions():
    msg = "1000 400 2 шт МДФ RAL 9010 матовый\n600 300 1 шт МДФ RAL 8017 глянцевый\nМосква."
    stage, result = run_chain(msg)
    assert stage == "corel"
    assert len(result["corel_rows"]) == 2


def test_full_chain_three_positions():
    msg = "1000 400 4 шт МДФ RAL 9010 матовый\n600 300 2 шт МДФ RAL 8017 глянцевый\n800 500 1 шт МДФ RAL 7016 матовый\nСПб."
    stage, result = run_chain(msg)
    assert stage == "corel"
    assert len(result["corel_rows"]) == 3


def test_full_chain_paint_only():
    msg = "Только покраска. Фасады уже есть. 1000 400 4 шт МДФ белый матовый"
    stage, result = run_chain(msg)
    assert stage == "corel"


# ===================================================================
# Blocked at Sales
# ===================================================================

def test_blocked_sales_discount():
    stage, _ = run_chain("1000 400 МДФ белый. Скидка будет если 10 штук?")
    assert stage == "sales_blocked"


def test_blocked_sales_tech_advice():
    stage, _ = run_chain("Фрезеровка + покраска фасадов МДФ 800 500 4 шт")
    assert stage == "sales_blocked"


def test_blocked_sales_no_sizes():
    stage, _ = run_chain("Сколько стоит покрасить фасады?")
    assert stage == "sales_blocked"


def test_blocked_sales_ambiguous_wood():
    stage, _ = run_chain("600 400 5 шт дерево белый")
    assert stage == "sales_blocked"


def test_blocked_sales_incomplete():
    stage, _ = run_chain("Покрасить надо")
    assert stage == "sales_blocked"


# ===================================================================
# Row order verification
# ===================================================================

def test_row_order_height_first():
    msg = "1000 400 4 шт МДФ белый матовый RAL 9010. Санкт-Петербург."
    stage, result = run_chain(msg)
    assert stage == "corel"
    row = result["corel_rows"][0]
    keys = list(row.keys())
    assert keys[1] == "height_mm", f"height_mm at pos 1, got {keys}"
    assert keys[2] == "width_mm", f"width_mm at pos 2, got {keys}"
    assert keys[3] == "quantity", f"quantity at pos 3, got {keys}"
    assert row["height_mm"] == 1000
    assert row["width_mm"] == 400


# ===================================================================
# Safety invariants
# ===================================================================

def test_all_results_not_final():
    msgs = [
        "1000 400 4 шт МДФ белый матовый RAL 9010. Санкт-Петербург.",
        "Только покраска. Фасады уже есть. 1000 400 4 шт МДФ белый матовый",
    ]
    for msg in msgs:
        stage, result = run_chain(msg)
        assert stage == "corel"
        assert result["not_final_export"] is True


def test_no_price_in_chain():
    msg = "1000 400 4 шт МДФ белый матовый RAL 9010. Санкт-Петербург."
    stage, result = run_chain(msg)
    assert stage == "corel"
    assert "price" not in result
    assert "cost" not in result
