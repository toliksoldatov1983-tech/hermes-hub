"""Tests for BATCH_093: Old Hermes → Hermes-Clean Runtime Bridge.

Covers:
  - Bridge contract validation
  - Allowed action routing
  - Blocked action enforcement
  - No secrets, no external API, no live Telegram
  - No real orders, no deletion
  - Malyarka dry-run through bridge
  - Daily assistant through bridge
  - AI provider status through bridge
  - Minimal context bridge tests
  - Regression for BATCH_088–092
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "src"))


# ── 1. Bridge contract tests ──


class TestBridgeContract:
    """Bridge contract dataclasses and enums."""

    def test_bridge_action_type_enum_values(self):
        from hermes_core.runtime_bridge import BridgeActionType
        assert BridgeActionType.STATUS.value > 0
        assert BridgeActionType.DAILY_ASSISTANT.value > 0
        assert BridgeActionType.LIVE_TELEGRAM.value > 0

    def test_bridge_request_creation(self):
        from hermes_core.runtime_bridge import BridgeRequest, BridgeActionType
        req = BridgeRequest(action=BridgeActionType.STATUS)
        assert req.action == BridgeActionType.STATUS
        assert req.source == "old-hermes"
        assert req.mode == "safe-local"

    def test_bridge_request_from_string(self):
        from hermes_core.runtime_bridge import BridgeRequest, BridgeActionType
        req = BridgeRequest.from_string("daily-assistant")
        assert req.action == BridgeActionType.DAILY_ASSISTANT

    def test_bridge_request_from_string_unknown_fallback(self):
        from hermes_core.runtime_bridge import BridgeRequest
        req = BridgeRequest.from_string("nonexistent-action")
        assert req.action is not None  # falls back to STATUS

    def test_bridge_response_ok(self):
        from hermes_core.runtime_bridge import BridgeResponse
        resp = BridgeResponse.ok_action("test", ["line1", "line2"], "route1")
        assert resp.is_ok is True
        assert resp.is_blocked is False
        assert resp.output_text == "line1\nline2"
        assert resp.route == "route1"

    def test_bridge_response_blocked(self):
        from hermes_core.runtime_bridge import BridgeResponse
        resp = BridgeResponse.blocked_action("live_telegram", "blocked")
        assert resp.is_blocked is True
        assert "BLOCKED" in resp.output_text

    def test_bridge_response_error(self):
        from hermes_core.runtime_bridge import BridgeResponse
        resp = BridgeResponse.error_action("test", "boom")
        assert resp.status == "ERROR"

    def test_bridge_response_audit_metadata(self):
        from hermes_core.runtime_bridge import BridgeResponse
        resp = BridgeResponse.ok_action("test", [])
        assert resp.audit_metadata["bridge_version"] == "1.0"
        assert resp.audit_metadata["safe_local"] is True
        assert resp.audit_metadata["real_api_called"] is False
        assert resp.audit_metadata["env_read"] is False
        assert resp.audit_metadata["network_called"] is False

    def test_allowed_actions_not_empty(self):
        from hermes_core.runtime_bridge import ALLOWED_SAFE_ACTIONS
        assert len(ALLOWED_SAFE_ACTIONS) >= 20

    def test_blocked_actions_not_empty(self):
        from hermes_core.runtime_bridge import BLOCKED_ACTIONS
        assert len(BLOCKED_ACTIONS) >= 8

    def test_allowed_and_blocked_disjoint(self):
        from hermes_core.runtime_bridge import ALLOWED_SAFE_ACTIONS, BLOCKED_ACTIONS
        overlap = ALLOWED_SAFE_ACTIONS & BLOCKED_ACTIONS
        assert len(overlap) == 0, f"Overlap: {overlap}"


# ── 2. Allowed action routing tests ──


class TestAllowedRouting:
    """Allowed actions route correctly through the bridge."""

    def test_status_routes(self):
        from hermes_core.runtime_bridge import BridgeRouter, BridgeRequest, BridgeActionType
        router = BridgeRouter()
        resp = router.handle(BridgeRequest(action=BridgeActionType.STATUS))
        assert resp.is_ok is True
        assert "Hermes-Clean" in resp.output_text

    def test_daily_assistant_routes(self):
        from hermes_core.runtime_bridge import BridgeRouter, BridgeRequest, BridgeActionType
        router = BridgeRouter()
        resp = router.handle(BridgeRequest(action=BridgeActionType.DAILY_ASSISTANT))
        assert resp.is_ok is True
        assert any("daily_assistant" in line for line in resp.output_lines)

    def test_daily_brief_routes(self):
        from hermes_core.runtime_bridge import BridgeRouter, BridgeRequest, BridgeActionType
        router = BridgeRouter()
        resp = router.handle(BridgeRequest(action=BridgeActionType.DAILY_BRIEF))
        assert resp.is_ok is True

    def test_what_next_routes(self):
        from hermes_core.runtime_bridge import BridgeRouter, BridgeRequest, BridgeActionType
        router = BridgeRouter()
        resp = router.handle(BridgeRequest(action=BridgeActionType.WHAT_NEXT))
        assert resp.is_ok is True

    def test_local_health_routes(self):
        from hermes_core.runtime_bridge import BridgeRouter, BridgeRequest, BridgeActionType
        router = BridgeRouter()
        resp = router.handle(BridgeRequest(action=BridgeActionType.LOCAL_HEALTH))
        assert resp.is_ok is True

    def test_project_status_routes(self):
        from hermes_core.runtime_bridge import BridgeRouter, BridgeRequest, BridgeActionType
        router = BridgeRouter()
        resp = router.handle(BridgeRequest(action=BridgeActionType.PROJECT_STATUS))
        assert resp.is_ok is True

    def test_ai_provider_list_routes(self):
        from hermes_core.runtime_bridge import BridgeRouter, BridgeRequest, BridgeActionType
        router = BridgeRouter()
        resp = router.handle(BridgeRequest(action=BridgeActionType.AI_PROVIDER_LIST))
        assert resp.is_ok is True

    def test_malyarka_fixtures_routes(self):
        from hermes_core.runtime_bridge import BridgeRouter, BridgeRequest, BridgeActionType
        router = BridgeRouter()
        resp = router.handle(BridgeRequest(action=BridgeActionType.MALYARKA_FIXTURES))
        assert resp.is_ok is True

    def test_help_local_routes(self):
        from hermes_core.runtime_bridge import BridgeRouter, BridgeRequest, BridgeActionType
        router = BridgeRouter()
        resp = router.handle(BridgeRequest(action=BridgeActionType.HELP_LOCAL))
        assert resp.is_ok is True

    def test_route_text_convenience(self):
        from hermes_core.runtime_bridge import BridgeRouter
        router = BridgeRouter()
        resp = router.route_text("daily-assistant")
        assert resp.is_ok is True


# ── 3. Blocked action tests ──


class TestBlockedActions:
    """Blocked actions are rejected by the bridge safety policy."""

    def test_live_telegram_blocked(self):
        from hermes_core.runtime_bridge import BridgeRouter, BridgeRequest, BridgeActionType
        router = BridgeRouter()
        resp = router.handle(BridgeRequest(action=BridgeActionType.LIVE_TELEGRAM))
        assert resp.is_blocked is True
        assert "blocked" in resp.blocked_reason.lower() or "BLOCKED" in resp.output_text

    def test_external_api_blocked(self):
        from hermes_core.runtime_bridge import BridgeRouter, BridgeRequest, BridgeActionType
        router = BridgeRouter()
        resp = router.handle(BridgeRequest(action=BridgeActionType.EXTERNAL_API))
        assert resp.is_blocked is True

    def test_google_drive_write_blocked(self):
        from hermes_core.runtime_bridge import BridgeRouter, BridgeRequest, BridgeActionType
        router = BridgeRouter()
        resp = router.handle(BridgeRequest(action=BridgeActionType.GOOGLE_DRIVE_WRITE))
        assert resp.is_blocked is True

    def test_real_order_access_blocked(self):
        from hermes_core.runtime_bridge import BridgeRouter, BridgeRequest, BridgeActionType
        router = BridgeRouter()
        resp = router.handle(BridgeRequest(action=BridgeActionType.REAL_ORDER_ACCESS))
        assert resp.is_blocked is True

    def test_delete_operation_blocked(self):
        from hermes_core.runtime_bridge import BridgeRouter, BridgeRequest, BridgeActionType
        router = BridgeRouter()
        resp = router.handle(BridgeRequest(action=BridgeActionType.DELETE_OPERATION))
        assert resp.is_blocked is True

    def test_secret_read_blocked(self):
        from hermes_core.runtime_bridge import BridgeRouter, BridgeRequest, BridgeActionType
        router = BridgeRouter()
        resp = router.handle(BridgeRequest(action=BridgeActionType.SECRET_READ))
        assert resp.is_blocked is True

    def test_direct_gemini_blocked(self):
        from hermes_core.runtime_bridge import BridgeRouter, BridgeRequest, BridgeActionType
        router = BridgeRouter()
        resp = router.handle(BridgeRequest(action=BridgeActionType.DIRECT_GEMINI))
        assert resp.is_blocked is True

    def test_direct_deepseek_blocked(self):
        from hermes_core.runtime_bridge import BridgeRouter, BridgeRequest, BridgeActionType
        router = BridgeRouter()
        resp = router.handle(BridgeRequest(action=BridgeActionType.DIRECT_DEEPSEEK))
        assert resp.is_blocked is True

    def test_archive_import_blocked(self):
        from hermes_core.runtime_bridge import BridgeRouter, BridgeRequest, BridgeActionType
        router = BridgeRouter()
        resp = router.handle(BridgeRequest(action=BridgeActionType.ARCHIVE_IMPORT))
        assert resp.is_blocked is True

    def test_polling_webhook_blocked(self):
        from hermes_core.runtime_bridge import BridgeRouter, BridgeRequest, BridgeActionType
        router = BridgeRouter()
        resp = router.handle(BridgeRequest(action=BridgeActionType.POLLING_WEBHOOK))
        assert resp.is_blocked is True


# ── 4. No secrets, no external API, no network ──


class TestBridgeSafety:
    """Bridge maintains safety guarantees."""

    def test_bridge_response_never_has_secrets(self):
        from hermes_core.runtime_bridge import BridgeResponse
        resp = BridgeResponse.ok_action("test", [])
        assert resp.audit_metadata["env_read"] is False
        assert resp.audit_metadata["token_used"] is False

    def test_bridge_policy_all_allowed_safe(self):
        from hermes_core.runtime_bridge import BridgeSafetyPolicy
        policy = BridgeSafetyPolicy()
        for allowed in policy.ALLOWED:
            assert policy.is_allowed(allowed) is True

    def test_bridge_policy_all_blocked_unsafe(self):
        from hermes_core.runtime_bridge import BLOCKED_ACTIONS, BridgeSafetyPolicy
        policy = BridgeSafetyPolicy()
        for blocked in BLOCKED_ACTIONS:
            assert policy.is_allowed(blocked) is False

    def test_safety_policy_rejects_hard_blocked(self):
        from hermes_core.runtime_bridge import BridgeSafetyPolicy, BridgeRequest, BridgeActionType
        policy = BridgeSafetyPolicy()
        resp = policy.check(BridgeRequest(action=BridgeActionType.SECRET_READ))
        assert resp is not None  # blocked
        assert resp.is_blocked is True


# ── 5. Malyarka dry-run through bridge ──


class TestMalyarkaBridge:
    """Malyarka dry-run commands work through bridge."""

    def test_malyarka_status_through_bridge(self):
        from hermes_core.runtime_bridge import BridgeRouter, BridgeRequest, BridgeActionType
        router = BridgeRouter()
        resp = router.handle(BridgeRequest(action=BridgeActionType.MALYARKA_STATUS))
        assert resp.is_ok is True

    def test_malyarka_fixtures_through_bridge(self):
        from hermes_core.runtime_bridge import BridgeRouter, BridgeRequest, BridgeActionType
        router = BridgeRouter()
        resp = router.handle(BridgeRequest(action=BridgeActionType.MALYARKA_FIXTURES))
        assert resp.is_ok is True
        assert any("fixtures=12" in line or "fixtures" in line.lower() for line in resp.output_lines)


# ── 6. Daily assistant through bridge ──


class TestDailyAssistantBridge:
    """Daily assistant commands through bridge."""

    def test_daily_assistant_through_bridge_has_malyarka(self):
        from hermes_core.runtime_bridge import BridgeRouter, BridgeRequest, BridgeActionType
        router = BridgeRouter()
        resp = router.handle(BridgeRequest(action=BridgeActionType.DAILY_ASSISTANT))
        assert resp.is_ok is True
        text = resp.output_text
        assert "malyarka" in text.lower() or "Malyarka" in text

    def test_daily_assistant_through_bridge_has_ai_provider(self):
        from hermes_core.runtime_bridge import BridgeRouter, BridgeRequest, BridgeActionType
        router = BridgeRouter()
        resp = router.handle(BridgeRequest(action=BridgeActionType.DAILY_ASSISTANT))
        assert resp.is_ok is True
        text = resp.output_text
        assert "provider" in text.lower() or "AI" in text


# ── 7. AI provider status through bridge ──


class TestAIProviderBridge:
    """AI provider commands through bridge."""

    def test_ai_provider_list_through_bridge(self):
        from hermes_core.runtime_bridge import BridgeRouter, BridgeRequest, BridgeActionType
        router = BridgeRouter()
        resp = router.handle(BridgeRequest(action=BridgeActionType.AI_PROVIDER_LIST))
        assert resp.is_ok is True

    def test_secret_gate_through_bridge(self):
        from hermes_core.runtime_bridge import BridgeRouter, BridgeRequest, BridgeActionType
        router = BridgeRouter()
        resp = router.handle(BridgeRequest(action=BridgeActionType.SECRET_GATE_STATUS))
        assert resp.is_ok is True


# ── 8. Minimal context bridge test ──


class TestMinimalContextBridge:
    """Bridge works with minimal context pattern."""

    def test_bridge_request_context_budget(self):
        from hermes_core.runtime_bridge import BridgeRequest, BridgeActionType
        req = BridgeRequest(action=BridgeActionType.STATUS, context_budget_pct=35)
        assert req.context_budget_pct == 35

    def test_bridge_response_context_budget(self):
        from hermes_core.runtime_bridge import BridgeResponse
        resp = BridgeResponse.ok_action("test", [])
        assert resp.context_budget_remaining_pct == 100


# ── 9. Regression for BATCH_088–092 ──


class TestRegression:
    """Bridge doesn't break existing functionality."""

    def test_malyarka_fixtures_still_work(self):
        from hermes_modules.malyarka.fixtures import run_all_fixtures
        results = run_all_fixtures()
        assert len(results) == 12

    def test_ai_provider_router_still_works(self):
        from hermes_core.ai_provider import AIProviderRouter, reset_default_registry
        from hermes_core.ai_provider.registry import get_default_registry
        reset_default_registry()
        get_default_registry()
        router = AIProviderRouter()
        decision = router.select("mock")
        assert decision.is_blocked is False

    def test_daily_assistant_still_works(self):
        from hermes_core.daily_assistant import build_daily_assistant
        report = build_daily_assistant()
        assert report.health_status == "OK"

    def test_review_provider_still_works(self):
        from hermes_core.review.review_provider_factory import ReviewProviderConfig, ReviewProviderFactory
        selection = ReviewProviderFactory().select(ReviewProviderConfig())
        assert selection.is_blocked is False

    def test_bridge_action_to_route_mapping(self):
        from hermes_core.runtime_bridge import ACTION_TO_ROUTE, BridgeActionType
        assert ACTION_TO_ROUTE[BridgeActionType.DAILY_ASSISTANT] == "daily-assistant"
        assert ACTION_TO_ROUTE[BridgeActionType.SMOKE] == "smoke"
        assert len(ACTION_TO_ROUTE) >= 20


# ── 10. Bridge router smoke test ──


class TestBridgeRouterSmoke:
    """Quick smoke test of all allowed routes."""

    @pytest.mark.parametrize("action,expect_ok", [
        ("STATUS", True),
        ("DASHBOARD", True),
        ("DAILY_REPORT", True),
        ("DAILY_ASSISTANT", True),
        ("DAILY_BRIEF", True),
        ("WHAT_NEXT", True),
        ("LOCAL_HEALTH", True),
        ("PROJECT_STATUS", True),
        ("MALYARKA_STATUS", True),
        ("MALYARKA_FIXTURES", True),
        ("AI_PROVIDER_LIST", True),
        ("SECRET_GATE_STATUS", True),
        ("HELP_LOCAL", True),
        ("LIVE_TELEGRAM", False),
        ("EXTERNAL_API", False),
        ("GOOGLE_DRIVE_WRITE", False),
        ("REAL_ORDER_ACCESS", False),
        ("DELETE_OPERATION", False),
        ("SECRET_READ", False),
        ("DIRECT_GEMINI", False),
        ("DIRECT_DEEPSEEK", False),
    ])
    def test_bridge_route_param(self, action, expect_ok):
        from hermes_core.runtime_bridge import BridgeRouter, BridgeRequest, BridgeActionType
        router = BridgeRouter()
        action_enum = BridgeActionType[action]
        resp = router.handle(BridgeRequest(action=action_enum))
        assert resp.is_ok == expect_ok, f"{action}: expected ok={expect_ok}, got {resp.status}"
