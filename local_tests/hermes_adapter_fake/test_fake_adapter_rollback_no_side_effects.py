from pathlib import Path

import pytest

from fake_adapter import FORBIDDEN_ACTIONS, RESPONSE_FIELDS, build_fake_adapter_response


ROLLBACK_SAFE_STATUSES = {"ok", "blocked", "fallback_required"}
ROLLBACK_SAFE_OUTPUT_TYPES = {
    "valid_output",
    "blocked_output",
    "fallback_output",
    "unsafe_output",
}
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
        "payload": payload or {"text": "safe local request"},
        "dry_run": dry_run,
        "feature_flags": flags(enabled=enabled),
    }
    if diagnostics is not None:
        data["diagnostics"] = diagnostics
    return data


def assert_rollback_safe_response(response):
    assert set(response) >= set(RESPONSE_FIELDS)
    assert response["status"] in ROLLBACK_SAFE_STATUSES
    assert response["output_type"] in ROLLBACK_SAFE_OUTPUT_TYPES
    assert isinstance(response["reason"], str)
    assert response["reason"]
    assert isinstance(response["blocked"], bool)
    assert isinstance(response["fallback_required"], bool)
    assert response["side_effects"] == []


def test_side_effects_are_empty_for_representative_paths():
    responses = [
        build_fake_adapter_response(request("answer_text")),
        build_fake_adapter_response(request("answer_text", enabled=False)),
        build_fake_adapter_response(request("create_file")),
        build_fake_adapter_response(request("change_database")),
        build_fake_adapter_response(request("unknown_action")),
        build_fake_adapter_response(request("answer_text", {"fallback_required": True})),
        build_fake_adapter_response(
            request(
                "explain_status",
                {"diagnostics": {"unsafe": "TOKEN=hidden"}},
                diagnostics=True,
            )
        ),
        build_fake_adapter_response(None),
    ]

    for response in responses:
        assert_rollback_safe_response(response)


def test_adapter_off_by_default_is_rollback_safe():
    response = build_fake_adapter_response(request("answer_text", enabled=False))

    assert_rollback_safe_response(response)
    assert response["blocked"] is True
    assert response["fallback_required"] is True
    assert response["reason"] == "adapter_disabled_by_default"


@pytest.mark.parametrize("action", ["create_file", "edit_file", "delete_file"])
def test_write_file_like_actions_do_not_create_side_effects(action):
    response = build_fake_adapter_response(request(action))

    assert_rollback_safe_response(response)
    assert response["blocked"] is True
    assert response["fallback_required"] is True
    assert response["output_type"] == "blocked_output"


@pytest.mark.parametrize("action", ["change_price", "change_rules", "change_database"])
def test_admin_database_like_actions_do_not_create_side_effects(action):
    response = build_fake_adapter_response(request(action))

    assert_rollback_safe_response(response)
    assert response["blocked"] is True
    assert response["fallback_required"] is True
    assert response["output_type"] == "blocked_output"


@pytest.mark.parametrize("action", sorted(FORBIDDEN_ACTIONS))
def test_all_forbidden_actions_are_rollback_safe(action):
    response = build_fake_adapter_response(request(action))

    assert_rollback_safe_response(response)
    assert response["blocked"] is True
    assert response["fallback_required"] is True


def test_malformed_input_is_rollback_safe():
    response = build_fake_adapter_response(
        {
            "action": 123,
            "payload": "bad",
            "dry_run": "bad",
            "feature_flags": "bad",
        }
    )

    assert_rollback_safe_response(response)
    assert response["fallback_required"] is True
    assert response["output_type"] == "fallback_output"


def test_fallback_required_true_is_rollback_safe():
    response = build_fake_adapter_response(request("summarize_project_state", {"fallback_required": True}))

    assert_rollback_safe_response(response)
    assert response["blocked"] is True
    assert response["fallback_required"] is True
    assert response["reason"] == "fallback_required_by_request"


def test_diagnostics_paths_are_rollback_safe():
    response = build_fake_adapter_response(
        request(
            "explain_status",
            {"diagnostics": {"unsafe": "/var/log/malyarka-telegram-bot/live.log"}},
            diagnostics=True,
        )
    )

    assert_rollback_safe_response(response)
    assert response["blocked"] is True
    assert response["diagnostics_safe"] is False


def test_repeated_calls_are_deterministic_and_rollback_safe():
    request_data = request("suggest_next_safe_step")

    first = build_fake_adapter_response(request_data)
    second = build_fake_adapter_response(request_data)
    third = build_fake_adapter_response(request_data)

    assert first == second == third
    assert_rollback_safe_response(first)


def test_fake_adapter_source_has_no_file_log_db_network_or_subprocess_primitives():
    source = Path(__file__).with_name("fake_adapter.py").read_text(encoding="utf-8")

    for marker in FORBIDDEN_SOURCE_MARKERS:
        assert marker not in source
