import pytest

from fake_adapter import (
    FORBIDDEN_ACTIONS,
    RESPONSE_FIELDS,
    build_fake_adapter_response,
)


SENSITIVE_MARKERS = (
    "TOKEN=",
    "BOT_TOKEN",
    "API_KEY=",
    "PASSWORD=",
    "PRIVATE_KEY",
    ".env",
    "config.py",
    "/opt/malyarka-telegram-bot",
    "178.104.95.187",
    "orders.db",
    "run-polling",
    "--run-polling",
    "restart polling",
)


def flags(**overrides):
    base = {
        "HERMES_ADAPTER_ENABLED": False,
        "HERMES_SAFE_MODE": True,
        "HERMES_ASSISTANT_MODE_ENABLED": False,
        "HERMES_ENGINEER_MODE_ENABLED": False,
        "HERMES_ADMIN_CHANGES_ENABLED": False,
        "HERMES_EXPORT_CALLBACKS_ENABLED": False,
    }
    base.update(overrides)
    return base


def request(action="answer_text", payload=None, feature_flags=None, dry_run=True, diagnostics=None):
    data = {
        "action": action,
        "payload": payload or {"text": "safe local request"},
        "dry_run": dry_run,
        "feature_flags": feature_flags if feature_flags is not None else flags(),
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


def assert_gate_response(response):
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
    for marker in SENSITIVE_MARKERS:
        assert marker not in response_text


def test_adapter_is_disabled_by_default():
    response = build_fake_adapter_response(request())

    assert_gate_response(response)
    assert response["ok"] is False
    assert response["blocked"] is True
    assert response["fallback_required"] is True
    assert response["reason"] == "adapter_disabled_by_default"
    assert response["output_type"] == "fallback_output"
    assert_no_sensitive_markers(response)


@pytest.mark.parametrize(
    "action",
    [
        "answer_text",
        "suggest_mode",
        "explain_status",
        "prepare_engineer_task_draft",
        "summarize_project_state",
        "explain_order_result",
        "suggest_next_safe_step",
    ],
)
def test_safe_dry_run_actions_require_adapter_enabled_flag(action):
    disabled = build_fake_adapter_response(request(action=action, feature_flags=flags()))
    enabled = build_fake_adapter_response(
        request(action=action, feature_flags=flags(HERMES_ADAPTER_ENABLED=True))
    )

    assert_gate_response(disabled)
    assert disabled["blocked"] is True
    assert disabled["fallback_required"] is True
    assert disabled["reason"] == "adapter_disabled_by_default"

    assert_gate_response(enabled)
    assert enabled["ok"] is True
    assert enabled["blocked"] is False
    assert enabled["fallback_required"] is False
    assert enabled["output_type"] == "valid_output"
    assert_no_sensitive_markers(enabled)


@pytest.mark.parametrize("action", ["create_file", "process_real_order_files"])
def test_export_actions_blocked_when_export_flag_is_disabled(action):
    response = build_fake_adapter_response(
        request(
            action=action,
            feature_flags=flags(
                HERMES_ADAPTER_ENABLED=True,
                HERMES_EXPORT_CALLBACKS_ENABLED=False,
            ),
        )
    )

    assert_gate_response(response)
    assert response["blocked"] is True
    assert response["fallback_required"] is True
    assert response["output_type"] == "blocked_output"
    assert "forbidden_action" in response["reason"]
    assert_no_sensitive_markers(response)


@pytest.mark.parametrize("action", ["change_price", "change_rules", "change_database"])
def test_admin_actions_blocked_when_admin_flag_is_disabled(action):
    response = build_fake_adapter_response(
        request(
            action=action,
            feature_flags=flags(
                HERMES_ADAPTER_ENABLED=True,
                HERMES_ADMIN_CHANGES_ENABLED=False,
            ),
        )
    )

    assert_gate_response(response)
    assert response["blocked"] is True
    assert response["fallback_required"] is True
    assert response["output_type"] == "blocked_output"
    assert "forbidden_action" in response["reason"]
    assert_no_sensitive_markers(response)


@pytest.mark.parametrize("action", ["edit_file", "delete_file"])
def test_write_actions_blocked_when_write_flags_are_disabled(action):
    response = build_fake_adapter_response(
        request(
            action=action,
            feature_flags=flags(
                HERMES_ADAPTER_ENABLED=True,
                HERMES_ADMIN_CHANGES_ENABLED=False,
                HERMES_EXPORT_CALLBACKS_ENABLED=False,
            ),
        )
    )

    assert_gate_response(response)
    assert response["blocked"] is True
    assert response["fallback_required"] is True
    assert response["output_type"] == "blocked_output"
    assert "forbidden_action" in response["reason"]
    assert_no_sensitive_markers(response)


def test_safe_diagnostics_remain_safe_only_when_no_diagnostics_flag_exists():
    response = build_fake_adapter_response(
        request(
            action="explain_status",
            payload={"diagnostics": {"adapter": "enabled", "safe_mode": True}},
            feature_flags=flags(HERMES_ADAPTER_ENABLED=True),
            diagnostics=True,
        )
    )

    assert_gate_response(response)
    assert response["ok"] is True
    assert response["diagnostics_safe"] is True
    assert response["side_effects"] == []
    assert_no_sensitive_markers(response)


def test_unsafe_diagnostics_are_blocked_even_when_adapter_enabled():
    response = build_fake_adapter_response(
        request(
            action="explain_status",
            payload={"diagnostics": {"raw": "TOKEN=hidden", "path": "/opt/malyarka-telegram-bot/config.py"}},
            feature_flags=flags(HERMES_ADAPTER_ENABLED=True),
            diagnostics=True,
        )
    )

    assert_gate_response(response)
    assert response["blocked"] is True
    assert response["fallback_required"] is True
    assert response["diagnostics_safe"] is False
    assert response["output_type"] == "unsafe_output"
    assert_no_sensitive_markers(response)


def test_unknown_action_blocked_regardless_of_flags():
    response = build_fake_adapter_response(
        request(
            action="future_unreviewed_action",
            feature_flags=flags(
                HERMES_ADAPTER_ENABLED=True,
                HERMES_ADMIN_CHANGES_ENABLED=True,
                HERMES_EXPORT_CALLBACKS_ENABLED=True,
            ),
        )
    )

    assert_gate_response(response)
    assert response["blocked"] is True
    assert response["fallback_required"] is True
    assert response["output_type"] == "blocked_output"
    assert "unknown_action" in response["reason"]
    assert_no_sensitive_markers(response)


@pytest.mark.parametrize("action", sorted(FORBIDDEN_ACTIONS))
def test_forbidden_actions_blocked_regardless_of_flags(action):
    response = build_fake_adapter_response(
        request(
            action=action,
            feature_flags=flags(
                HERMES_ADAPTER_ENABLED=True,
                HERMES_ADMIN_CHANGES_ENABLED=True,
                HERMES_EXPORT_CALLBACKS_ENABLED=True,
                HERMES_ENGINEER_MODE_ENABLED=True,
                HERMES_ASSISTANT_MODE_ENABLED=True,
            ),
        )
    )

    assert_gate_response(response)
    assert response["blocked"] is True
    assert response["fallback_required"] is True
    assert response["output_type"] == "blocked_output"
    assert_no_sensitive_markers(response)


def test_fallback_required_does_not_bypass_feature_flags():
    response = build_fake_adapter_response(
        request(
            action="answer_text",
            payload={"fallback_required": True},
            feature_flags=flags(HERMES_ADAPTER_ENABLED=True),
        )
    )

    assert_gate_response(response)
    assert response["blocked"] is True
    assert response["fallback_required"] is True
    assert response["output_type"] == "fallback_output"
    assert response["reason"] == "fallback_required_by_request"
    assert_no_sensitive_markers(response)


def test_side_effects_are_empty_for_feature_gate_paths():
    responses = [
        build_fake_adapter_response(request()),
        build_fake_adapter_response(request(feature_flags=flags(HERMES_ADAPTER_ENABLED=True))),
        build_fake_adapter_response(request("create_file", feature_flags=flags(HERMES_ADAPTER_ENABLED=True))),
        build_fake_adapter_response(request("future_unreviewed_action", feature_flags=flags(HERMES_ADAPTER_ENABLED=True))),
    ]

    for response in responses:
        assert_gate_response(response)
        assert response["side_effects"] == []
        assert_no_sensitive_markers(response)
