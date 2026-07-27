"""Tests for BATCH_094: Mobile Gateway and Local API.

Covers:
  - Mobile API contract validation
  - Allowed endpoint routing via MobileGateway
  - Blocked endpoint enforcement
  - Localhost-only policy (127.0.0.1, not 0.0.0.0)
  - No secrets, no external API, no network
  - Malyarka dry-run via mobile gateway
  - Daily assistant via mobile gateway
  - AI provider status via mobile gateway
  - Mobile API response format (JSON-safe)
  - Mobile API server self-check
  - Regression for BATCH_088–093
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "src"))


# ── 1. Mobile API contract tests ──


class TestMobileAPIContract:
    """Mobile API contract validation."""

    def test_allowed_endpoints_non_empty(self):
        from hermes_core.mobile_gateway import ALLOWED_ENDPOINTS
        assert len(ALLOWED_ENDPOINTS) == 11

    def test_blocked_endpoints_non_empty(self):
        from hermes_core.mobile_gateway import BLOCKED_ENDPOINTS
        assert len(BLOCKED_ENDPOINTS) == 9

    def test_no_overlap(self):
        from hermes_core.mobile_gateway import ALLOWED_ENDPOINTS, BLOCKED_ENDPOINTS
        overlap = ALLOWED_ENDPOINTS & BLOCKED_ENDPOINTS
        assert len(overlap) == 0

    def test_response_to_dict(self):
        from hermes_core.mobile_gateway import MobileAPIResponse
        resp = MobileAPIResponse.ok("GET /test", "TEST", {"key": "val"})
        d = resp.to_dict()
        assert d["status"] == "OK"
        assert d["safe_local"] is True
        assert d["endpoint"] == "GET /test"
        assert d["data"]["key"] == "val"
        assert "audit_metadata" in d

    def test_response_audit_metadata(self):
        from hermes_core.mobile_gateway import MobileAPIResponse
        resp = MobileAPIResponse.ok("GET /test", "TEST", {})
        meta = resp.audit_metadata
        assert meta["bind_address"] == "127.0.0.1"
        assert meta["real_api_called"] is False
        assert meta["env_read"] is False
        assert meta["token_used"] is False
        assert meta["network_called"] is False
        assert meta["external_port_open"] is False

    def test_response_blocked(self):
        from hermes_core.mobile_gateway import MobileAPIResponse
        resp = MobileAPIResponse.blocked("GET /test", "TEST", "blocked reason")
        assert resp.status == "BLOCKED"
        assert resp.blocked_reason == "blocked reason"

    def test_response_error(self):
        from hermes_core.mobile_gateway import MobileAPIResponse
        resp = MobileAPIResponse.error("GET /test", "TEST", "error msg")
        assert resp.status == "ERROR"

    def test_contract_is_json_serializable(self):
        import json
        from hermes_core.mobile_gateway import MobileAPIResponse
        resp = MobileAPIResponse.ok("GET /test", "TEST", {"nested": {"deep": True}})
        json_str = json.dumps(resp.to_dict(), ensure_ascii=False)
        parsed = json.loads(json_str)
        assert parsed["status"] == "OK"


# ── 2. Allowed endpoint routing ──


class TestAllowedEndpoints:
    """Allowed endpoints return OK through MobileGateway."""

    def test_status_endpoint(self):
        from hermes_core.mobile_gateway import MobileGateway
        gw = MobileGateway()
        resp = gw.status()
        assert resp.status == "OK"

    def test_dashboard_endpoint(self):
        from hermes_core.mobile_gateway import MobileGateway
        gw = MobileGateway()
        resp = gw.dashboard()
        assert resp.status == "OK"

    def test_daily_assistant_endpoint(self):
        from hermes_core.mobile_gateway import MobileGateway
        gw = MobileGateway()
        resp = gw.daily_assistant()
        assert resp.status == "OK"

    def test_what_next_endpoint(self):
        from hermes_core.mobile_gateway import MobileGateway
        gw = MobileGateway()
        resp = gw.what_next()
        assert resp.status == "OK"

    def test_local_health_endpoint(self):
        from hermes_core.mobile_gateway import MobileGateway
        gw = MobileGateway()
        resp = gw.local_health()
        assert resp.status == "OK"

    def test_malyarka_status_endpoint(self):
        from hermes_core.mobile_gateway import MobileGateway
        gw = MobileGateway()
        resp = gw.malyarka_status()
        assert resp.status == "OK"

    def test_ai_provider_status_endpoint(self):
        from hermes_core.mobile_gateway import MobileGateway
        gw = MobileGateway()
        resp = gw.ai_provider_status()
        assert resp.status == "OK"

    def test_bridge_status_endpoint(self):
        from hermes_core.mobile_gateway import MobileGateway
        gw = MobileGateway()
        resp = gw.bridge_status()
        assert resp.status == "OK"

    def test_all_responses_safe_local(self):
        from hermes_core.mobile_gateway import MobileGateway
        gw = MobileGateway()
        for name, fn in [
            ("status", gw.status),
            ("dashboard", gw.dashboard),
            ("daily-assistant", gw.daily_assistant),
            ("what-next", gw.what_next),
            ("local-health", gw.local_health),
            ("malyarka-status", gw.malyarka_status),
            ("ai-provider-status", gw.ai_provider_status),
        ]:
            resp = fn()
            assert resp.safe_local is True, f"{name}: safe_local should be True"
            assert resp.audit_metadata["bind_address"] == "127.0.0.1", f"{name}: bind should be 127.0.0.1"


# ── 3. Blocked endpoint tests ──


class TestBlockedEndpoints:
    """Blocked endpoints are rejected."""

    def test_live_telegram_blocked(self):
        from hermes_core.mobile_gateway import MobileGateway, MobileAPIEndpoint
        gw = MobileGateway()
        resp = gw.handle(MobileAPIEndpoint.LIVE_TELEGRAM)
        assert resp.status == "BLOCKED"

    def test_google_drive_blocked(self):
        from hermes_core.mobile_gateway import MobileGateway, MobileAPIEndpoint
        gw = MobileGateway()
        resp = gw.handle(MobileAPIEndpoint.GOOGLE_DRIVE)
        assert resp.status == "BLOCKED"

    def test_external_api_blocked(self):
        from hermes_core.mobile_gateway import MobileGateway, MobileAPIEndpoint
        gw = MobileGateway()
        resp = gw.handle(MobileAPIEndpoint.EXTERNAL_API)
        assert resp.status == "BLOCKED"

    def test_direct_gemini_blocked(self):
        from hermes_core.mobile_gateway import MobileGateway, MobileAPIEndpoint
        gw = MobileGateway()
        resp = gw.handle(MobileAPIEndpoint.DIRECT_GEMINI)
        assert resp.status == "BLOCKED"

    def test_direct_deepseek_blocked(self):
        from hermes_core.mobile_gateway import MobileGateway, MobileAPIEndpoint
        gw = MobileGateway()
        resp = gw.handle(MobileAPIEndpoint.DIRECT_DEEPSEEK)
        assert resp.status == "BLOCKED"

    def test_real_orders_blocked(self):
        from hermes_core.mobile_gateway import MobileGateway, MobileAPIEndpoint
        gw = MobileGateway()
        resp = gw.handle(MobileAPIEndpoint.REAL_ORDERS)
        assert resp.status == "BLOCKED"

    def test_delete_operation_blocked(self):
        from hermes_core.mobile_gateway import MobileGateway, MobileAPIEndpoint
        gw = MobileGateway()
        resp = gw.handle(MobileAPIEndpoint.DELETE_OPERATION)
        assert resp.status == "BLOCKED"


# ── 4. Localhost-only policy tests ──


class TestLocalhostPolicy:
    """Server binds only to 127.0.0.1."""

    def test_default_host_is_localhost(self):
        from hermes_core.mobile_gateway import LocalAPIServer
        srv = LocalAPIServer()
        assert srv.host == "127.0.0.1"

    def test_default_port_is_8514(self):
        from hermes_core.mobile_gateway import LocalAPIServer
        srv = LocalAPIServer()
        assert srv.port == 8514

    def test_0_0_0_0_raises(self):
        from hermes_core.mobile_gateway import LocalAPIServer
        srv = LocalAPIServer(host="0.0.0.0")
        with pytest.raises(ValueError, match="127.0.0.1"):
            srv.start()

    def test_external_ip_raises(self):
        from hermes_core.mobile_gateway import LocalAPIServer
        srv = LocalAPIServer(host="192.168.1.1")
        with pytest.raises(ValueError, match="127.0.0.1"):
            srv.start()


# ── 5. No secrets / no API tests ──


class TestMobileSafety:
    """Mobile gateway doesn't touch secrets or external APIs."""

    def test_audit_no_env_read(self):
        from hermes_core.mobile_gateway import MobileGateway
        gw = MobileGateway()
        resp = gw.status()
        assert resp.audit_metadata["env_read"] is False

    def test_audit_no_token_used(self):
        from hermes_core.mobile_gateway import MobileGateway
        gw = MobileGateway()
        resp = gw.status()
        assert resp.audit_metadata["token_used"] is False

    def test_audit_no_network_called(self):
        from hermes_core.mobile_gateway import MobileGateway
        gw = MobileGateway()
        resp = gw.status()
        assert resp.audit_metadata["network_called"] is False

    def test_audit_no_real_api_called(self):
        from hermes_core.mobile_gateway import MobileGateway
        gw = MobileGateway()
        resp = gw.status()
        assert resp.audit_metadata["real_api_called"] is False


# ── 6. Mobile API server self-check ──


class TestMobileAPIServer:
    """Local API server starts and responds correctly."""

    def test_server_self_check(self):
        from hermes_core.mobile_gateway import LocalAPIServer
        server = LocalAPIServer()
        ok = server.self_check()
        assert ok is True, "Server self-check should pass"

    def test_server_start_stop(self):
        from hermes_core.mobile_gateway import LocalAPIServer
        server = LocalAPIServer()
        server.start()
        assert server.is_running is True
        server.stop()
        assert server.is_running is False

    def test_server_not_running_after_stop(self):
        from hermes_core.mobile_gateway import LocalAPIServer
        server = LocalAPIServer()
        server.start()
        server.stop()
        # Double stop should not error
        server.stop()
        assert server.is_running is False


# ── 7. CLI integration ──


class TestCLIGatewayCommands:
    """Mobile gateway CLI commands work."""

    def test_mobile_gateway_status_cli(self):
        from hermes_core.cli import mobile_gateway_status_command
        import argparse
        rc = mobile_gateway_status_command(argparse.Namespace())
        assert rc == 0

    def test_mobile_api_contract_cli(self):
        from hermes_core.cli import mobile_api_contract_command
        import argparse
        rc = mobile_api_contract_command(argparse.Namespace())
        assert rc == 0

    def test_mobile_api_dry_run_cli(self):
        from hermes_core.cli import mobile_api_dry_run_command
        import argparse
        rc = mobile_api_dry_run_command(argparse.Namespace())
        assert rc == 0

    def test_mobile_api_server_check_cli(self):
        from hermes_core.cli import mobile_api_server_check_command
        import argparse
        rc = mobile_api_server_check_command(argparse.Namespace())
        assert rc == 0

    def test_commands_registered_in_parser(self):
        from hermes_core.cli import build_parser
        parser = build_parser()
        args = parser.parse_args(["mobile-gateway-status"])
        assert args.command == "mobile-gateway-status"


# ── 8. Regression for BATCH_088–093 ──


class TestRegression:
    """Mobile gateway doesn't break existing functionality."""

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
        assert router.select("mock").is_blocked is False

    def test_runtime_bridge_still_works(self):
        from hermes_core.runtime_bridge import BridgeRouter, BridgeRequest, BridgeActionType
        router = BridgeRouter()
        resp = router.handle(BridgeRequest(action=BridgeActionType.STATUS))
        assert resp.is_ok is True

    def test_daily_assistant_still_works(self):
        from hermes_core.daily_assistant import build_daily_assistant
        report = build_daily_assistant()
        assert report.health_status == "OK"

    def test_mobile_gateway_uses_runtime_bridge(self):
        """Verify MobileGateway uses BridgeRouter, not direct calls."""
        from hermes_core.mobile_gateway.gateway import MobileGateway
        gw = MobileGateway()
        assert gw._bridge is not None
        from hermes_core.runtime_bridge.router import BridgeRouter
        assert isinstance(gw._bridge, BridgeRouter)
