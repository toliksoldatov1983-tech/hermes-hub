from pathlib import Path

import pytest

from fake_adapter import (
    FORBIDDEN_ACTIONS,
    RESPONSE_FIELDS,
    build_fake_adapter_response,
    validate_fake_adapter_response,
)


def enabled_request(action="answer_text", payload=None, dry_run=True):
    return {
        "action": action,
        "payload": payload or {"text": "status"},
        "dry_run": dry_run,
        "feature_flags": {
            "HERMES_ADAPTER_ENABLED": True,
            "HERMES_SAFE_MODE": True,
            "HERMES_EXPORT_CALLBACKS_ENABLED": False,
            "HERMES_ADMIN_CHANGES_ENABLED": False,
            "HERMES_ENGINEER_MODE_ENABLED": False,
        },
    }


def assert_safe_response_contract(response):
    assert set(RESPONSE_FIELDS) <= set(response)
    assert response["side_effects"] == []
    assert isinstance(response["ok"], bool)
    assert isinstance(response["status"], str)
    assert isinstance(response["action"], str)
    assert isinstance(response["dry_run"], bool)
    assert isinstance(response["blocked"], bool)
    assert isinstance(response["fallback_required"], bool)
    assert isinstance(response["reason"], str)
    assert isinstance(response["diagnostics_safe"], bool)
    assert isinstance(response["output_type"], str)


def test_safe_allowed_action_returns_valid_output():
    response = build_fake_adapter_response(enabled_request("answer_text", dry_run=False))

    assert_safe_response_contract(response)
    assert response["ok"] is True
    assert response["status"] == "ok"
    assert response["action"] == "answer_text"
    assert response["dry_run"] is False
    assert response["blocked"] is False
    assert response["fallback_required"] is False
    assert response["output_type"] == "valid_output"


@pytest.mark.parametrize("action", sorted(FORBIDDEN_ACTIONS))
def test_forbidden_actions_are_blocked(action):
    response = build_fake_adapter_response(enabled_request(action))

    assert_safe_response_contract(response)
    assert response["ok"] is False
    assert response["blocked"] is True
    assert response["fallback_required"] is True
    assert response["output_type"] == "blocked_output"
    assert "forbidden_action" in response["reason"]


def test_unknown_action_is_blocked():
    response = build_fake_adapter_response(enabled_request("unknown_future_action"))

    assert_safe_response_contract(response)
    assert response["blocked"] is True
    assert response["fallback_required"] is True
    assert response["output_type"] == "blocked_output"
    assert "unknown_action" in response["reason"]


def test_missing_required_fields_returns_fallback():
    response = build_fake_adapter_response({"action": "answer_text", "dry_run": True})

    assert_safe_response_contract(response)
    assert response["fallback_required"] is True
    assert response["output_type"] == "fallback_output"
    assert "missing_required_fields" in response["reason"]


def test_wrong_field_types_return_fallback():
    response = build_fake_adapter_response(
        {
            "action": 123,
            "payload": "not-a-dict",
            "dry_run": "yes",
            "feature_flags": [],
            "diagnostics": "yes",
        }
    )

    assert_safe_response_contract(response)
    assert response["fallback_required"] is True
    assert response["output_type"] == "fallback_output"
    assert "wrong_field_types" in response["reason"]


@pytest.mark.parametrize("bad_output", [{}, None, ""])
def test_empty_or_malformed_output_validation_returns_fallback(bad_output):
    response = validate_fake_adapter_response(bad_output)

    assert_safe_response_contract(response)
    assert response["fallback_required"] is True
    assert response["output_type"] == "fallback_output"


def test_unsafe_diagnostics_are_blocked():
    request = enabled_request(
        "explain_status",
        payload={"diagnostics": {"debug": "TOKEN=abc123 and restart polling"}},
    )
    request["diagnostics"] = True

    response = build_fake_adapter_response(request)

    assert_safe_response_contract(response)
    assert response["blocked"] is True
    assert response["fallback_required"] is True
    assert response["diagnostics_safe"] is False
    assert response["output_type"] == "unsafe_output"


def test_fallback_required_true_returns_fallback_output():
    response = build_fake_adapter_response(
        enabled_request("summarize_project_state", payload={"fallback_required": True})
    )

    assert_safe_response_contract(response)
    assert response["fallback_required"] is True
    assert response["output_type"] == "fallback_output"
    assert response["reason"] == "fallback_required_by_request"


def test_adapter_off_by_default_returns_fallback():
    response = build_fake_adapter_response(
        {
            "action": "answer_text",
            "payload": {"text": "hello"},
            "dry_run": True,
            "feature_flags": {},
        }
    )

    assert_safe_response_contract(response)
    assert response["fallback_required"] is True
    assert response["output_type"] == "fallback_output"
    assert response["reason"] == "adapter_disabled_by_default"


@pytest.mark.parametrize(
    "action",
    [
        "create_file",
        "edit_file",
        "delete_file",
        "change_price",
        "change_rules",
        "change_database",
        "process_real_order_files",
    ],
)
def test_feature_flags_block_export_admin_and_write_actions(action):
    response = build_fake_adapter_response(enabled_request(action))

    assert_safe_response_contract(response)
    assert response["blocked"] is True
    assert response["fallback_required"] is True
    assert response["side_effects"] == []


def test_unsafe_output_with_side_effects_is_replaced_by_fallback():
    unsafe_output = {
        "ok": True,
        "status": "ok",
        "action": "answer_text",
        "dry_run": True,
        "blocked": False,
        "fallback_required": False,
        "reason": "unsafe",
        "diagnostics_safe": True,
        "side_effects": ["created_file"],
        "output_type": "valid_output",
    }

    response = validate_fake_adapter_response(unsafe_output)

    assert_safe_response_contract(response)
    assert response["fallback_required"] is True
    assert response["output_type"] == "fallback_output"
    assert "side_effects" in response["reason"]


def test_malformed_request_object_does_not_crash():
    response = build_fake_adapter_response(None)

    assert_safe_response_contract(response)
    assert response["fallback_required"] is True
    assert response["output_type"] == "fallback_output"


def test_fake_adapter_source_has_no_forbidden_runtime_imports():
    source = Path(__file__).with_name("fake_adapter.py").read_text(encoding="utf-8")

    assert "import os" not in source
    assert "os.environ" not in source
    assert "import subprocess" not in source
    assert "import requests" not in source
    assert "import httpx" not in source
    assert "import aiohttp" not in source
    assert "aiogram" not in source
    assert "malyarka_telegram" not in source
    assert "malyarka_core" not in source
