from pathlib import Path

import pytest

from fake_adapter import RESPONSE_FIELDS, build_fake_adapter_response


SENSITIVE_INPUTS = {
    "token": "TOKEN=123456:ABC-secret",
    "env_file": ".env contains TELEGRAM_BOT_TOKEN",
    "config_file": "/opt/malyarka-telegram-bot/malyarka_telegram/config.py",
    "environment": "os.environ['BOT_TOKEN']",
    "server_path": "/opt/malyarka-telegram-bot/.venv/bin/python",
    "database_path": "/opt/malyarka-telegram-bot/orders.db",
    "live_logs_path": "/var/log/malyarka-telegram-bot/live.log",
    "polling_identifier": "python -m malyarka_telegram.app --run-polling",
    "webhook_identifier": "https://api.telegram.org/botTOKEN/setWebhook",
}

SENSITIVE_RESPONSE_MARKERS = (
    "TOKEN=",
    "TELEGRAM_BOT_TOKEN",
    "BOT_TOKEN",
    "123456:ABC",
    ".env",
    "config.py",
    "os.environ",
    "/opt/malyarka-telegram-bot",
    ".venv/bin/python",
    "orders.db",
    "/var/log",
    "live.log",
    "run-polling",
    "--run-polling",
    "setWebhook",
    "api.telegram.org",
)


def flags(enabled=True):
    return {
        "HERMES_ADAPTER_ENABLED": enabled,
        "HERMES_SAFE_MODE": True,
        "HERMES_ASSISTANT_MODE_ENABLED": False,
        "HERMES_ENGINEER_MODE_ENABLED": False,
        "HERMES_ADMIN_CHANGES_ENABLED": False,
        "HERMES_EXPORT_CALLBACKS_ENABLED": False,
    }


def diagnostics_request(payload, *, enabled=True, dry_run=True, diagnostics=True):
    return {
        "action": "explain_status",
        "payload": payload,
        "dry_run": dry_run,
        "feature_flags": flags(enabled=enabled),
        "diagnostics": diagnostics,
    }


def flatten_strings(value):
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        result = []
        for key, item in value.items():
            result.extend(flatten_strings(key))
            result.extend(flatten_strings(item))
        return result
    if isinstance(value, (list, tuple, set)):
        result = []
        for item in value:
            result.extend(flatten_strings(item))
        return result
    return []


def assert_response_contract(response):
    assert set(response) >= set(RESPONSE_FIELDS)
    assert isinstance(response["ok"], bool)
    assert isinstance(response["status"], str)
    assert isinstance(response["action"], str)
    assert isinstance(response["dry_run"], bool)
    assert isinstance(response["blocked"], bool)
    assert isinstance(response["fallback_required"], bool)
    assert isinstance(response["reason"], str)
    assert isinstance(response["diagnostics_safe"], bool)
    assert response["side_effects"] == []
    assert isinstance(response["output_type"], str)


def assert_no_sensitive_markers(response):
    response_text = "\n".join(flatten_strings(response))
    for marker in SENSITIVE_RESPONSE_MARKERS:
        assert marker not in response_text


@pytest.mark.parametrize("sensitive_value", SENSITIVE_INPUTS.values(), ids=SENSITIVE_INPUTS.keys())
def test_unsafe_diagnostics_inputs_are_blocked_without_leaking_values(sensitive_value):
    response = build_fake_adapter_response(
        diagnostics_request({"diagnostics": {"unsafe": sensitive_value}})
    )

    assert_response_contract(response)
    assert response["blocked"] is True
    assert response["fallback_required"] is True
    assert response["diagnostics_safe"] is False
    assert response["output_type"] == "unsafe_output"
    assert response["reason"] == "unsafe_diagnostics_blocked"
    assert_no_sensitive_markers(response)


def test_safe_diagnostics_are_safe_only_when_adapter_enabled():
    response = build_fake_adapter_response(
        diagnostics_request(
            {
                "diagnostics": {
                    "adapter": "enabled",
                    "safe_mode": True,
                    "fallback": "not_required",
                }
            }
        )
    )

    assert_response_contract(response)
    assert response["ok"] is True
    assert response["blocked"] is False
    assert response["fallback_required"] is False
    assert response["diagnostics_safe"] is True
    assert response["output_type"] == "valid_output"
    assert_no_sensitive_markers(response)


def test_diagnostics_without_needed_adapter_flag_are_blocked_by_default():
    response = build_fake_adapter_response(
        diagnostics_request(
            {"diagnostics": {"adapter": "disabled", "safe_mode": True}},
            enabled=False,
        )
    )

    assert_response_contract(response)
    assert response["blocked"] is True
    assert response["fallback_required"] is True
    assert response["diagnostics_safe"] is True
    assert response["output_type"] == "fallback_output"
    assert response["reason"] == "adapter_disabled_by_default"
    assert_no_sensitive_markers(response)


def test_diagnostics_response_preserves_dry_run_flag():
    response = build_fake_adapter_response(
        diagnostics_request(
            {"diagnostics": {"adapter": "enabled"}},
            dry_run=False,
        )
    )

    assert_response_contract(response)
    assert response["dry_run"] is False
    assert response["side_effects"] == []
    assert_no_sensitive_markers(response)


def test_unsafe_diagnostics_response_has_no_side_effects():
    response = build_fake_adapter_response(
        diagnostics_request({"diagnostics": {"unsafe": "PRIVATE_KEY=hidden"}})
    )

    assert_response_contract(response)
    assert response["side_effects"] == []
    assert response["blocked"] is True
    assert response["diagnostics_safe"] is False
    assert_no_sensitive_markers(response)


def test_diagnostics_do_not_make_network_or_api_calls():
    response = build_fake_adapter_response(
        diagnostics_request({"diagnostics": {"adapter": "enabled"}})
    )

    assert_response_contract(response)
    assert response["side_effects"] == []
    assert_no_sensitive_markers(response)


def test_fake_adapter_source_has_no_live_or_network_imports_for_diagnostics():
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
    assert "api.telegram.org" not in source
