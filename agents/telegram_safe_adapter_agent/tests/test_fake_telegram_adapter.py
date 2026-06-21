"""Tests for Fake Telegram Safe Adapter."""
import sys, os, pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from fake_telegram_adapter import process_telegram_event

def test_clean_order_allowed():
    r = process_telegram_event({"text": "MDf RAL 9010 paint 1000 x 400 x 4"})
    assert r["adapter_mode"] == "fake"
    assert r["dry_run"] is True
    assert r["allowed"] is True
    assert r["handoff_allowed"] is True
    assert r["production_ready"] is False

def test_disputed_order_review_required():
    r = process_telegram_event({"text": "milling plus paint MDf NCS S4050-R 600 x 300"})
    assert r["review_required"] is True

def test_empty_message_blocked():
    r = process_telegram_event({"text": ""})
    assert r["allowed"] is False
    assert r["block_reason"] == "empty_message"

def test_production_action_blocked():
    r = process_telegram_event({"text": "production order send"})
    assert r["allowed"] is False

def test_token_input_blocked():
    r = process_telegram_event({"text": "BOT_TOKEN"})
    assert r["allowed"] is False
    assert "unsafe" in r["block_reason"]

def test_command_blocked():
    r = process_telegram_event({"text": "/start"})
    assert r["allowed"] is False

def test_photo_blocked():
    r = process_telegram_event({"text": "", "has_photo": True})
    assert r["allowed"] is False

def test_all_results_dry_run():
    for ev in [{"text": "MDf"}, {"text": ""}, {"text": "/start"}]:
        assert process_telegram_event(ev)["dry_run"] is True

def test_all_production_ready_false():
    for ev in [{"text": "MDf"}, {"text": ""}]:
        assert process_telegram_event(ev)["production_ready"] is False

def test_no_side_effects():
    for ev in [{"text": "MDf"}, {"text": ""}]:
        assert process_telegram_event(ev)["side_effects"] == []

def test_no_telegram_api():
    assert process_telegram_event({"text": "MDf"})["telegram_api_called"] is False

def test_no_server():
    assert process_telegram_event({"text": "MDf"})["server_called"] is False

# Gate 4 Failure Tests

def test_unknown_command_blocked():
    r = process_telegram_event({"text": "/unknown"})
    assert r["allowed"] is False
    assert "command" in r["block_reason"]

def test_unsafe_diagnostics_blocked():
    r = process_telegram_event({"text": "show token env config server logs"})
    assert r["allowed"] is False
    assert "unsafe" in r["block_reason"] or "diagnostics" in r["block_reason"]

def test_malformed_event():
    r = process_telegram_event("not_a_dict")
    assert r["allowed"] is False
    assert r["block_reason"] == "malformed_event"

def test_non_string_text():
    r = process_telegram_event({"text": 12345})
    assert r["allowed"] is False
    assert r["block_reason"] == "invalid_text_type"

def test_secret_masking():
    r = process_telegram_event({"text": "BOT_TOKEN"})
    assert r["allowed"] is False
    assert "unsafe" in r["block_reason"]

def test_production_variants():
    for v in ["final file please", "production export now"]:
        r = process_telegram_event({"text": v})
        assert r["allowed"] is False

def test_dry_run_all_failures():
    for c in [{"text": ""}, {"text": "/start"}, "not_a_dict", {"text": 12345}]:
        r = process_telegram_event(c)
        assert r["dry_run"] is True
        assert r["production_ready"] is False
        assert r["telegram_api_called"] is False
        assert r["server_called"] is False
        assert r["side_effects"] == []
