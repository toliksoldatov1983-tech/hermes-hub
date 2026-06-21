from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ADAPTER_PATH = ROOT / "adapter_boundary_fix_candidate" / "hermes_adapter.py"
FORBIDDEN_ENGLISH = (
    "What is 700 x 500 for?",
    "Image dimensions",
    "Canvas size",
    "Window size",
)


def load_adapter():
    spec = importlib.util.spec_from_file_location("candidate_hermes_adapter", ADAPTER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def assert_fallback_response(result):
    assert result["fallback_required"] is True
    assert result["blocked"] is False
    assert result["telegram_api_called"] is False
    assert result["server_called"] is False
    assert result["side_effects"] == []


def assert_no_english_clarification(result):
    rendered = repr(result)
    for phrase in FORBIDDEN_ENGLISH:
        assert phrase not in rendered


def test_700_x_500_outside_order_mode_fallback_not_english():
    adapter = load_adapter()
    result = adapter.check_hermes_safety("700 x 500")
    assert_fallback_response(result)
    assert result["block_reason"] == "order_like_input_fallback"
    assert_no_english_clarification(result)


def test_700_x_500_inside_order_mode_fallback_not_parser_replacement():
    adapter = load_adapter()
    result = adapter.check_hermes_safety("700 x 500")
    assert_fallback_response(result)
    assert_no_english_clarification(result)


def test_cyrillic_x_order_like_fallback():
    adapter = load_adapter()
    result = adapter.check_hermes_safety("700х500")
    assert_fallback_response(result)
    assert_no_english_clarification(result)


def test_multiplication_sign_order_like_fallback():
    adapter = load_adapter()
    result = adapter.check_hermes_safety("700 × 500")
    assert_fallback_response(result)
    assert_no_english_clarification(result)


def test_asterisk_order_like_fallback():
    adapter = load_adapter()
    result = adapter.check_hermes_safety("700*500")
    assert_fallback_response(result)
    assert_no_english_clarification(result)


def test_three_dimension_order_like_fallback():
    adapter = load_adapter()
    result = adapter.check_hermes_safety("700 x 500 x 2")
    assert_fallback_response(result)
    assert_no_english_clarification(result)


def test_start_command_falls_back_to_existing_router():
    adapter = load_adapter()
    result = adapter.check_hermes_safety("/start")
    assert_fallback_response(result)
    assert result["block_reason"] == "command_fallback"


def test_safe_generic_text_can_continue_adapter_path():
    adapter = load_adapter()
    result = adapter.check_hermes_safety("тест")
    assert result["blocked"] is False
    assert result["fallback_required"] is False
    assert result["review_required"] is False
    assert result["side_effects"] == []


def test_unknown_generic_question_can_continue_adapter_path():
    adapter = load_adapter()
    result = adapter.check_hermes_safety("How should we name this idea?")
    assert result["blocked"] is False
    assert result["fallback_required"] is False
    assert result["review_required"] is False
    assert result["side_effects"] == []


def test_guard_forbidden_english_phrases_absent_for_order_like_input():
    adapter = load_adapter()
    for text in ("700 x 500", "700х500", "700 × 500", "700*500", "700 x 500 x 2"):
        result = adapter.check_hermes_safety(text)
        assert_fallback_response(result)
        assert_no_english_clarification(result)

