import pytest

from fake_adapter import (
    FORBIDDEN_ACTIONS,
    RESPONSE_FIELDS,
    build_fake_adapter_response,
    validate_fake_adapter_response,
)


BOUNDARY_FIELDS = set(RESPONSE_FIELDS)
SAFE_STATUSES = {"ok", "blocked", "fallback_required"}
SAFE_OUTPUT_TYPES = {
    "valid_output",
    "blocked_output",
    "fallback_output",
    "unsafe_output",
}
SENSITIVE_RESPONSE_MARKERS = (
    "TOKEN=",
    "BOT_TOKEN",
    "API_KEY=",
    "PASSWORD=",
    "PRIVATE_KEY",
    "/opt/malyarka-telegram-bot",
    "178.104.95.187",
    "orders.db",
    "config.py",
    "E:\\Заказы 2026",
    "run-polling",
    "--run-polling",
    "restart polling",
)


def enabled_request(action="answer_text", payload=None, dry_run=True):
    return {
        "action": action,
        "payload": payload or {"text": "safe dry-run input"},
        "dry_run": dry_run,
        "feature_flags": {
            "HERMES_ADAPTER_ENABLED": True,
            "HERMES_SAFE_MODE": True,
            "HERMES_EXPORT_CALLBACKS_ENABLED": False,
            "HERMES_ADMIN_CHANGES_ENABLED": False,
            "HERMES_ENGINEER_MODE_ENABLED": False,
        },
    }


def assert_dry_run_boundary(response):
    assert set(response) >= BOUNDARY_FIELDS
    assert isinstance(response["ok"], bool)
    assert response["status"] in SAFE_STATUSES
    assert isinstance(response["action"], str)
    assert isinstance(response["dry_run"], bool)
    assert isinstance(response["blocked"], bool)
    assert isinstance(response["fallback_required"], bool)
    assert isinstance(response["reason"], str)
    assert isinstance(response["diagnostics_safe"], bool)
    assert response["side_effects"] == []
    assert response["output_type"] in SAFE_OUTPUT_TYPES


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


def assert_no_sensitive_response_data(response):
    response_text = "\n".join(flatten_strings(response))
    for marker in SENSITIVE_RESPONSE_MARKERS:
        assert marker not in response_text


def test_valid_response_contains_required_dry_run_boundary_fields():
    response = build_fake_adapter_response(enabled_request("answer_text"))

    assert_dry_run_boundary(response)
    assert response["ok"] is True
    assert response["output_type"] == "valid_output"
    assert_no_sensitive_response_data(response)


def test_dry_run_true_is_preserved_in_response():
    response = build_fake_adapter_response(enabled_request("suggest_next_safe_step", dry_run=True))

    assert_dry_run_boundary(response)
    assert response["dry_run"] is True
    assert_no_sensitive_response_data(response)


def test_side_effects_are_empty_for_all_boundary_output_types():
    responses = [
        build_fake_adapter_response(enabled_request("answer_text")),
        build_fake_adapter_response(enabled_request("create_file")),
        build_fake_adapter_response(
            {
                "action": "answer_text",
                "payload": {"text": "adapter disabled"},
                "dry_run": True,
                "feature_flags": {},
            }
        ),
        validate_fake_adapter_response({}),
        build_fake_adapter_response(
            {
                "action": "explain_status",
                "payload": {"diagnostics": {"debug": "TOKEN=hidden"}},
                "dry_run": True,
                "feature_flags": {
                    "HERMES_ADAPTER_ENABLED": True,
                    "HERMES_SAFE_MODE": True,
                },
                "diagnostics": True,
            }
        ),
    ]

    for response in responses:
        assert_dry_run_boundary(response)
        assert response["side_effects"] == []


@pytest.mark.parametrize("action", ["create_file", "change_price", "change_database"])
def test_blocked_output_is_compatible_with_dry_run_contract(action):
    response = build_fake_adapter_response(enabled_request(action))

    assert_dry_run_boundary(response)
    assert response["status"] == "blocked"
    assert response["blocked"] is True
    assert response["fallback_required"] is True
    assert response["output_type"] == "blocked_output"
    assert_no_sensitive_response_data(response)


def test_fallback_output_is_compatible_with_dry_run_contract():
    response = build_fake_adapter_response(enabled_request("explain_status", {"fallback_required": True}))

    assert_dry_run_boundary(response)
    assert response["status"] == "fallback_required"
    assert response["blocked"] is True
    assert response["fallback_required"] is True
    assert response["output_type"] == "fallback_output"
    assert_no_sensitive_response_data(response)


@pytest.mark.parametrize("malformed_output", [{}, None, "not-a-dict"])
def test_malformed_output_returns_controlled_fallback(malformed_output):
    response = validate_fake_adapter_response(malformed_output)

    assert_dry_run_boundary(response)
    assert response["fallback_required"] is True
    assert response["output_type"] == "fallback_output"
    assert_no_sensitive_response_data(response)


def test_unsafe_diagnostics_do_not_leak_sensitive_values():
    response = build_fake_adapter_response(
        {
            "action": "explain_status",
            "payload": {
                "diagnostics": {
                    "raw": "TOKEN=super-secret-value",
                    "path": "/opt/malyarka-telegram-bot/config.py",
                    "command": "restart polling",
                }
            },
            "dry_run": True,
            "feature_flags": {
                "HERMES_ADAPTER_ENABLED": True,
                "HERMES_SAFE_MODE": True,
            },
            "diagnostics": True,
        }
    )

    assert_dry_run_boundary(response)
    assert response["diagnostics_safe"] is False
    assert response["output_type"] == "unsafe_output"
    assert_no_sensitive_response_data(response)


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
def test_export_admin_write_actions_remain_blocked_with_disabled_flags(action):
    response = build_fake_adapter_response(enabled_request(action))

    assert_dry_run_boundary(response)
    assert response["blocked"] is True
    assert response["fallback_required"] is True
    assert response["side_effects"] == []
    assert_no_sensitive_response_data(response)


def test_adapter_off_by_default_remains_blocked():
    response = build_fake_adapter_response(
        {
            "action": "answer_text",
            "payload": {"text": "safe"},
            "dry_run": True,
            "feature_flags": {},
        }
    )

    assert_dry_run_boundary(response)
    assert response["blocked"] is True
    assert response["fallback_required"] is True
    assert response["reason"] == "adapter_disabled_by_default"
    assert_no_sensitive_response_data(response)


@pytest.mark.parametrize("action", sorted(FORBIDDEN_ACTIONS))
def test_forbidden_actions_do_not_break_boundary(action):
    response = build_fake_adapter_response(enabled_request(action))

    assert_dry_run_boundary(response)
    assert response["blocked"] is True
    assert response["fallback_required"] is True
    assert response["side_effects"] == []


def test_response_has_no_live_telegram_or_server_identifiers():
    response = build_fake_adapter_response(enabled_request("summarize_project_state"))

    assert_dry_run_boundary(response)
    assert_no_sensitive_response_data(response)
