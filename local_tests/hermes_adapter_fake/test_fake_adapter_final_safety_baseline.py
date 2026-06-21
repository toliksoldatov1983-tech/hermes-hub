from pathlib import Path

import pytest

from fake_adapter import (
    FORBIDDEN_ACTIONS,
    RESPONSE_FIELDS,
    build_fake_adapter_response,
    validate_fake_adapter_response,
)


SAFE_STATUSES = {"ok", "blocked", "fallback_required"}
SAFE_OUTPUT_TYPES = {
    "valid_output",
    "blocked_output",
    "fallback_output",
    "unsafe_output",
}
ALLOWED_ACTIONS = (
    "answer_text",
    "suggest_mode",
    "explain_status",
    "prepare_engineer_task_draft",
    "summarize_project_state",
    "explain_order_result",
    "suggest_next_safe_step",
)
SENSITIVE_RESPONSE_MARKERS = (
    "TOKEN=",
    "TELEGRAM_BOT_TOKEN",
    "BOT_TOKEN",
    "API_KEY=",
    "PASSWORD=",
    "PRIVATE_KEY",
    ".env",
    "config.py",
    "os.environ",
    "/opt/malyarka-telegram-bot",
    "178.104.95.187",
    "orders.db",
    "/var/log",
    "live.log",
    "run-polling",
    "--run-polling",
    "setWebhook",
    "api.telegram.org",
)
FORBIDDEN_SOURCE_MARKERS = (
    "import os",
    "os.environ",
    "import subprocess",
    "subprocess.",
    "import requests",
    "import httpx",
    "import aiohttp",
    "import urllib",
    "import socket",
    "import sqlite3",
    "open(",
    ".write(",
    "Path(",
    "read_text(",
    "write_text(",
    "malyarka_telegram",
    "malyarka_core",
    "aiogram",
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


def request(action="answer_text", payload=None, *, enabled=True, dry_run=True, diagnostics=None):
    data = {
        "action": action,
        "payload": payload or {"text": "safe baseline request"},
        "dry_run": dry_run,
        "feature_flags": flags(enabled=enabled),
    }
    if diagnostics is not None:
        data["diagnostics"] = diagnostics
    return data


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


def assert_final_baseline_response(response):
    assert set(response) >= set(RESPONSE_FIELDS)
    assert isinstance(response["ok"], bool)
    assert response["status"] in SAFE_STATUSES
    assert isinstance(response["action"], str)
    assert isinstance(response["dry_run"], bool)
    assert isinstance(response["blocked"], bool)
    assert isinstance(response["fallback_required"], bool)
    assert isinstance(response["reason"], str)
    assert response["reason"]
    assert isinstance(response["diagnostics_safe"], bool)
    assert response["side_effects"] == []
    assert response["output_type"] in SAFE_OUTPUT_TYPES


def assert_no_sensitive_markers(response):
    response_text = "\n".join(flatten_strings(response))
    for marker in SENSITIVE_RESPONSE_MARKERS:
        assert marker not in response_text


def test_final_baseline_representative_scenarios_are_safe():
    responses = [
        build_fake_adapter_response(request("answer_text")),
        build_fake_adapter_response(request("answer_text", enabled=False)),
        build_fake_adapter_response(request("create_file")),
        build_fake_adapter_response(request("change_price")),
        build_fake_adapter_response(request("unknown_future_action")),
        build_fake_adapter_response(request("answer_text", {"fallback_required": True})),
        build_fake_adapter_response(
            request(
                "explain_status",
                {"diagnostics": {"unsafe": "TOKEN=hidden"}},
                diagnostics=True,
            )
        ),
        build_fake_adapter_response(None),
        validate_fake_adapter_response({}),
    ]

    for response in responses:
        assert_final_baseline_response(response)
        assert_no_sensitive_markers(response)


@pytest.mark.parametrize("action", ALLOWED_ACTIONS)
def test_final_baseline_allowed_actions_require_enabled_adapter(action):
    disabled = build_fake_adapter_response(request(action, enabled=False))
    enabled = build_fake_adapter_response(request(action, enabled=True))

    assert_final_baseline_response(disabled)
    assert disabled["blocked"] is True
    assert disabled["fallback_required"] is True
    assert disabled["reason"] == "adapter_disabled_by_default"

    assert_final_baseline_response(enabled)
    assert enabled["ok"] is True
    assert enabled["blocked"] is False
    assert enabled["fallback_required"] is False
    assert enabled["output_type"] == "valid_output"


@pytest.mark.parametrize("action", sorted(FORBIDDEN_ACTIONS))
def test_final_baseline_forbidden_actions_are_always_blocked(action):
    response = build_fake_adapter_response(request(action, enabled=True))

    assert_final_baseline_response(response)
    assert response["blocked"] is True
    assert response["fallback_required"] is True
    assert response["output_type"] == "blocked_output"
    assert_no_sensitive_markers(response)


def test_final_baseline_dry_run_is_preserved_across_outcomes():
    safe_response = build_fake_adapter_response(request("answer_text", dry_run=False))
    blocked_response = build_fake_adapter_response(request("create_file", dry_run=False))
    fallback_response = build_fake_adapter_response(
        request("answer_text", {"fallback_required": True}, dry_run=False)
    )

    for response in (safe_response, blocked_response, fallback_response):
        assert_final_baseline_response(response)
        assert response["dry_run"] is False


def test_final_baseline_malformed_input_is_controlled():
    response = build_fake_adapter_response(
        {
            "action": [],
            "payload": "not-a-dict",
            "dry_run": "not-a-bool",
            "feature_flags": "not-a-dict",
        }
    )

    assert_final_baseline_response(response)
    assert response["blocked"] is True
    assert response["fallback_required"] is True
    assert response["output_type"] == "fallback_output"
    assert "wrong_field_types" in response["reason"]
    assert_no_sensitive_markers(response)


def test_final_baseline_unsafe_diagnostics_are_blocked_without_leakage():
    response = build_fake_adapter_response(
        request(
            "explain_status",
            {
                "diagnostics": {
                    "token": "TOKEN=abc",
                    "env": ".env",
                    "server": "/opt/malyarka-telegram-bot",
                    "db": "orders.db",
                    "live": "python -m malyarka_telegram.app --run-polling",
                }
            },
            diagnostics=True,
        )
    )

    assert_final_baseline_response(response)
    assert response["blocked"] is True
    assert response["diagnostics_safe"] is False
    assert response["output_type"] == "unsafe_output"
    assert_no_sensitive_markers(response)


def test_final_baseline_repeated_calls_are_deterministic():
    data = request("suggest_next_safe_step", {"text": "same input"})

    responses = [build_fake_adapter_response(data) for _ in range(5)]

    assert all(response == responses[0] for response in responses)
    assert_final_baseline_response(responses[0])


def test_final_baseline_source_has_no_live_or_side_effect_primitives():
    source = Path(__file__).with_name("fake_adapter.py").read_text(encoding="utf-8")

    for marker in FORBIDDEN_SOURCE_MARKERS:
        assert marker not in source
