"""
Corel Export Dry-Run Tests.
"""

import sys, os, pytest, json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from corel_export_agent import build_export_contract

OUT = os.path.join(os.path.dirname(__file__), "out")

CLEAN = {"confirmed_rows": [{"height_mm":1000,"width_mm":400,"quantity":4,"material":"МДФ","color":"RAL 9010","finish":"матовый"}], "disputed_rows":[], "export_blocked":False, "manager_review_required":False, "not_final_order":True}
DISPUTED = {"confirmed_rows": [{"height_mm":1000,"width_mm":400,"quantity":2,"material":"МДФ","color":"RAL 9010"}], "disputed_rows":[{"height_mm":600,"width_mm":300,"quantity":1,"material":"дерево"}], "export_blocked":True, "not_final_order":True}


def test_row_order_height_first():
    """Row dict order: height_mm, width_mm, quantity."""
    c = build_export_contract(CLEAN)
    assert c["ready_for_corel"]
    r = c["corel_rows"][0]
    keys = list(r.keys())
    assert keys[1] == "height_mm"
    assert keys[2] == "width_mm"
    assert keys[3] == "quantity"
    assert r["height_mm"] == 1000
    assert r["width_mm"] == 400


def test_preview_hxw():
    """Preview shows H×W not W×H."""
    c = build_export_contract(CLEAN)
    assert "1000×400" in c["preview"]


def test_disputed_not_exported():
    """Disputed rows never in corel_rows."""
    c = build_export_contract(DISPUTED)
    assert not c["ready_for_corel"]


def test_export_blocked_blocks():
    """export_blocked=true blocks output."""
    r = dict(DISPUTED, export_blocked=True)
    c = build_export_contract(r)
    assert not c["ready_for_corel"]


def test_manager_review_blocks():
    """manager_review_required blocks output."""
    r = dict(CLEAN, manager_review_required=True)
    c = build_export_contract(r)
    assert not c["ready_for_corel"]


def test_not_final_export_preserved():
    c = build_export_contract(CLEAN)
    assert c["not_final_export"] is True


def test_no_price():
    c = build_export_contract(CLEAN)
    assert "price" not in c


def test_output_files_exist():
    assert os.path.exists(os.path.join(OUT, "fake_corel_preview.txt"))
    assert os.path.exists(os.path.join(OUT, "fake_corel_rows.csv"))
    assert os.path.exists(os.path.join(OUT, "fake_export_contract.json"))
