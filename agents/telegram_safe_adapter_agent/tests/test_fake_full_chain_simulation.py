"""Full-chain simulation tests."""
import sys, os, pytest

BASE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(BASE, "..", "src"))
from fake_full_chain_simulation import run_full_chain

def test_clean_full_chain():
    r = run_full_chain({"text": "MDf RAL 9010 paint 1000 x 400 x 4"})
    assert r["adapter"]["allowed"] is True
    assert r["stages_reached"] == ["adapter", "sales", "malyarka", "corel"]
    assert r["corel"]["ready_for_corel"] is True

def test_disputed_blocked():
    r = run_full_chain({"text": "фрезеровка покраска МДФ NCS S4050-R 600 x 300"})
    assert "sales_blocked" in r["stages_reached"]

def test_production_blocked():
    r = run_full_chain({"text": "production order send"})
    assert r["stages_reached"] == ["adapter_blocked"]

def test_token_blocked():
    r = run_full_chain({"text": "BOT_TOKEN"})
    assert r["stages_reached"] == ["adapter_blocked"]

def test_empty_blocked():
    r = run_full_chain({"text": ""})
    assert r["stages_reached"] == ["adapter_blocked"]

def test_photo_blocked():
    r = run_full_chain({"text": "", "has_photo": True})
    assert r["stages_reached"] == ["adapter_blocked"]

def test_all_dry_run():
    for ev in [{"text": "MDf"}, {"text": ""}, {"text": "/start"}]:
        r = run_full_chain(ev)
        assert r["adapter"]["dry_run"] is True

def test_all_production_ready_false():
    for ev in [{"text": "MDf"}, {"text": ""}]:
        r = run_full_chain(ev)
        assert r["adapter"]["production_ready"] is False
        if r.get("corel"):
            assert r["corel"]["not_final_export"] is True
