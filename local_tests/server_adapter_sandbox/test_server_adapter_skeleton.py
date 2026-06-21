"""
Focused contract tests for server_adapter_skeleton.

BUNDLE_271_300: Tests based on contract examples from BUNDLE_247_250.

10 contract examples:
1. adapter off by default
2. safe dry-run allowed
3. export blocked
4. admin blocked
5. write blocked
6. unknown action blocked
7. malformed request
8. fallback_required=true
9. diagnostics safe-only
10. unsafe diagnostics blocked (dry_run=false)

All tests are local-only and do not touch server/live/secrets/real orders.
"""

import sys
import os
import pytest

# Add sandbox dir to path so we can import the skeleton
sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "local_tests",
        "server_adapter_sandbox",
    ),
)

from server_adapter_skeleton import process_request  # type: ignore[import-untyped]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _base_request(**overrides):
    """Build a safe base request with all required fields."""
    req = {
        "action": "answer_text",
        "payload": {
            "text": "test",
            "current_mode": "chat",
            "safe_context_summary": "local safe context",
        },
        "dry_run": True,
        "feature_flags": {
            "HERMES_ADAPTER_ENABLED": True,
            "HERMES_SERVER_ADAPTER_ENABLED": True,
            "HERMES_SAFE_MODE": True,
            "HERMES_DRY_RUN_ONLY": True,
        },
        "safe_mode": True,
        "diagnostics": False,
    }
    req.update(overrides)
    return req


def _assert_response(resp, **expected):
    """Assert response fields match expected values."""
    for key, value in expected.items():
        assert resp[key] == value, f"Field '{key}': expected {value}, got {resp[key]}"


def _assert_side_effects_empty(resp):
    """Assert side_effects is always an empty list."""
    assert resp["side_effects"] == [], (
        f"side_effects must be [], got {resp['side_effects']}"
    )


# ---------------------------------------------------------------------------
# Example 1 — Adapter Off By Default
# ---------------------------------------------------------------------------


def test_example_1_adapter_off_by_default():
    """Adapter is disabled → fallback required, no action executed."""
    req = _base_request(
        feature_flags={
            "HERMES_ADAPTER_ENABLED": False,
            "HERMES_SAFE_MODE": True,
            "HERMES_DRY_RUN_ONLY": True,
        }
    )
    resp = process_request(req)
    _assert_side_effects_empty(resp)
    _assert_response(
        resp,
        ok=False,
        status="disabled",
        action="fallback",
        dry_run=True,
        blocked=True,
        fallback_required=True,
        reason="adapter disabled by feature flag",
        output_type="fallback",
        diagnostics_safe=True,
    )


# ---------------------------------------------------------------------------
# Example 2 — Safe Dry-Run Allowed
# ---------------------------------------------------------------------------


def test_example_2_safe_dry_run_allowed():
    """Safe action with dry-run and adapter enabled → allowed."""
    req = _base_request(
        action="explain_status",
        payload={
            "text": "Покажи статус безопасно",
            "current_mode": "chat",
            "safe_context_summary": "adapter dry-run local status only",
        },
        feature_flags={
            "HERMES_ADAPTER_ENABLED": True,
            "HERMES_SERVER_ADAPTER_ENABLED": True,
            "HERMES_SAFE_MODE": True,
            "HERMES_DRY_RUN_ONLY": True,
        },
    )
    resp = process_request(req)
    _assert_side_effects_empty(resp)
    _assert_response(
        resp,
        ok=True,
        status="dry_run",
        action="explain_status",
        dry_run=True,
        blocked=False,
        fallback_required=False,
        reason="safe dry-run action allowed",
        output_type="draft",
        diagnostics_safe=True,
    )


# ---------------------------------------------------------------------------
# Example 3 — Export Blocked
# ---------------------------------------------------------------------------


def test_example_3_export_blocked():
    """Export callback disabled → export blocked, fallback required."""
    req = _base_request(
        action="create_export",
        payload={"order_preview_safe": "summary only"},
        feature_flags={
            "HERMES_ADAPTER_ENABLED": True,
            "HERMES_EXPORT_CALLBACKS_ENABLED": False,
            "HERMES_SAFE_MODE": True,
            "HERMES_DRY_RUN_ONLY": True,
        },
    )
    resp = process_request(req)
    _assert_side_effects_empty(resp)
    _assert_response(
        resp,
        ok=False,
        status="blocked",
        action="blocked",
        dry_run=True,
        blocked=True,
        fallback_required=True,
        reason="export action blocked by feature flags",
        output_type="blocked",
        diagnostics_safe=True,
    )


# ---------------------------------------------------------------------------
# Example 4 — Admin Blocked
# ---------------------------------------------------------------------------


def test_example_4_admin_blocked():
    """Admin changes disabled → admin action blocked."""
    req = _base_request(
        action="admin_change",
        payload={"requested_change": "change rule draft only"},
        feature_flags={
            "HERMES_ADAPTER_ENABLED": True,
            "HERMES_ADMIN_CHANGES_ENABLED": False,
            "HERMES_SAFE_MODE": True,
            "HERMES_DRY_RUN_ONLY": True,
        },
    )
    resp = process_request(req)
    _assert_side_effects_empty(resp)
    _assert_response(
        resp,
        ok=False,
        status="blocked",
        action="blocked",
        dry_run=True,
        blocked=True,
        fallback_required=True,
        reason="admin changes disabled",
        output_type="blocked",
        diagnostics_safe=True,
    )


# ---------------------------------------------------------------------------
# Example 5 — Write Blocked
# ---------------------------------------------------------------------------


def test_example_5_write_blocked():
    """Write action → blocked, fallback required."""
    req = _base_request(
        action="edit_file",
        payload={"target": "server file"},
        feature_flags={
            "HERMES_ADAPTER_ENABLED": True,
            "HERMES_SAFE_MODE": True,
            "HERMES_DRY_RUN_ONLY": True,
        },
    )
    resp = process_request(req)
    _assert_side_effects_empty(resp)
    _assert_response(
        resp,
        ok=False,
        status="blocked",
        action="blocked",
        dry_run=True,
        blocked=True,
        fallback_required=True,
        reason="write action forbidden",
        output_type="blocked",
        diagnostics_safe=True,
    )


# ---------------------------------------------------------------------------
# Example 6 — Unknown Action Blocked
# ---------------------------------------------------------------------------


def test_example_6_unknown_action_blocked():
    """Unknown action → blocked, fallback required."""
    req = _base_request(
        action="do_magic_live",
        payload={},
        feature_flags={
            "HERMES_ADAPTER_ENABLED": True,
            "HERMES_SAFE_MODE": True,
            "HERMES_DRY_RUN_ONLY": True,
        },
    )
    resp = process_request(req)
    _assert_side_effects_empty(resp)
    _assert_response(
        resp,
        ok=False,
        status="blocked",
        action="blocked",
        dry_run=True,
        blocked=True,
        fallback_required=True,
        reason="unknown action blocked",
        output_type="blocked",
        diagnostics_safe=True,
    )


# ---------------------------------------------------------------------------
# Example 7 — Malformed Request
# ---------------------------------------------------------------------------


def test_example_7_malformed_request_missing_fields():
    """Missing required fields → malformed, fallback required."""
    req: dict = {
        "payload": "not a dict",
        "dry_run": True,
        # missing: action, feature_flags, safe_mode, diagnostics
    }
    resp = process_request(req)
    _assert_side_effects_empty(resp)
    _assert_response(
        resp,
        ok=False,
        status="malformed",
        action="malformed",
        blocked=True,
        fallback_required=True,
        output_type="malformed",
        diagnostics_safe=True,
    )


def test_example_7_malformed_request_payload_not_dict():
    """Payload is not a dict → malformed."""
    req = _base_request(payload="not a dict")
    resp = process_request(req)
    _assert_side_effects_empty(resp)
    _assert_response(
        resp,
        ok=False,
        status="malformed",
        action="malformed",
        blocked=True,
        fallback_required=True,
        output_type="malformed",
    )


def test_example_7_malformed_request_not_dict():
    """Request itself is not a dict → malformed."""
    resp = process_request("not a dict")  # type: ignore[arg-type]
    _assert_side_effects_empty(resp)
    assert resp["ok"] is False
    assert resp["status"] == "malformed"
    assert resp["blocked"] is True
    assert resp["fallback_required"] is True


# ---------------------------------------------------------------------------
# Example 8 — fallback_required=true
# ---------------------------------------------------------------------------


def test_example_8_fallback_requested():
    """Explicit fallback action → fallback required."""
    req = _base_request(
        action="fallback",
        payload={"reason": "use existing Telegram flow"},
    )
    resp = process_request(req)
    _assert_side_effects_empty(resp)
    _assert_response(
        resp,
        ok=False,
        status="fallback",
        action="fallback",
        dry_run=True,
        blocked=True,
        fallback_required=True,
        reason="fallback requested",
        output_type="fallback",
        diagnostics_safe=True,
    )


# ---------------------------------------------------------------------------
# Example 9 — Diagnostics Safe-Only
# ---------------------------------------------------------------------------


def test_example_9_diagnostics_safe_only():
    """Diagnostics with safe flags → allowed, no side effects."""
    req = _base_request(
        action="diagnostics",
        payload={"include": "safe flags only"},
        diagnostics=True,
    )
    resp = process_request(req)
    _assert_side_effects_empty(resp)
    _assert_response(
        resp,
        ok=True,
        status="dry_run",
        action="diagnostics",
        dry_run=True,
        blocked=False,
        fallback_required=False,
        reason="safe diagnostics only",
        output_type="diagnostics",
        diagnostics_safe=True,
    )


# ---------------------------------------------------------------------------
# Example 10 — Unsafe: dry_run=false must be blocked
# ---------------------------------------------------------------------------


def test_example_10_dry_run_false_blocked():
    """dry_run=false → blocked, fallback required."""
    req = _base_request(dry_run=False)
    resp = process_request(req)
    _assert_side_effects_empty(resp)
    _assert_response(
        resp,
        ok=False,
        status="blocked",
        action="blocked",
        dry_run=False,
        blocked=True,
        fallback_required=True,
        reason="dry-run must be true",
        output_type="blocked",
        diagnostics_safe=True,
    )


# ---------------------------------------------------------------------------
# Additional safety edge-cases
# ---------------------------------------------------------------------------


def test_safe_mode_false_blocked():
    """safe_mode=false → blocked, fallback required."""
    req = _base_request(safe_mode=False)
    resp = process_request(req)
    _assert_side_effects_empty(resp)
    assert resp["ok"] is False
    assert resp["status"] == "blocked"
    assert resp["blocked"] is True
    assert resp["fallback_required"] is True
    assert "safe mode must be true" in resp["reason"]


def test_explicitly_blocked_action():
    """send_telegram_message is in BLOCKED_ACTIONS → blocked."""
    req = _base_request(action="send_telegram_message")
    resp = process_request(req)
    _assert_side_effects_empty(resp)
    assert resp["ok"] is False
    assert resp["status"] == "blocked"
    assert "action blocked" in resp["reason"]


def test_all_allowed_actions_work():
    """All explicitly allowed actions work in safe dry-run mode."""
    for action in [
        "answer_text",
        "explain_status",
        "suggest_next_safe_step",
    ]:
        req = _base_request(action=action)
        resp = process_request(req)
        _assert_side_effects_empty(resp)
        assert resp["ok"] is True, f"Action '{action}' should be allowed"
        assert resp["status"] == "dry_run"
        assert resp["blocked"] is False
        assert resp["fallback_required"] is False


def test_unknown_flags_ignored():
    """Unknown feature flags must not enable behaviour."""
    req = _base_request(
        feature_flags={
            "HERMES_ADAPTER_ENABLED": True,
            "HERMES_SAFE_MODE": True,
            "HERMES_DRY_RUN_ONLY": True,
            "UNKNOWN_DANGEROUS_FLAG": True,
        }
    )
    resp = process_request(req)
    assert resp["ok"] is True  # unknown flag ignored, safe defaults prevail


def test_missing_flags_default_safe():
    """Missing flags default to safest value."""
    req = _base_request(
        feature_flags={
            "HERMES_ADAPTER_ENABLED": True,
            "HERMES_SAFE_MODE": True,
        }
        # HERMES_DRY_RUN_ONLY missing → defaults to True
    )
    resp = process_request(req)
    assert resp["ok"] is True  # dry_run defaults to True from request
