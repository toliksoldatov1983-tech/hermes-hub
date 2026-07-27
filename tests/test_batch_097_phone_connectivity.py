"""Tests for BATCH_097: Phone Connectivity & Pairing Plan."""

from __future__ import annotations
import sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))


class TestPairingContract:
    def test_dry_run_pairing_defaults(self):
        from hermes_core.phone_connectivity import DevicePairing, PairingMode
        p = DevicePairing.dry_run()
        assert p.pairing_mode == PairingMode.DRY_RUN
        assert p.is_dry_run is True
        assert p.is_real is False
        assert p.api_base_url == "http://127.0.0.1:8514"

    def test_pairing_audit_safe(self):
        from hermes_core.phone_connectivity import DevicePairing
        p = DevicePairing.dry_run()
        assert p.audit_metadata["real_token"] is False
        assert p.audit_metadata["real_connection"] is False
        assert p.audit_metadata["safe_local"] is True

    def test_pairing_to_dict(self):
        from hermes_core.phone_connectivity import DevicePairing
        d = DevicePairing.dry_run().to_dict()
        assert d["pairing_mode"] == "dry-run"
        assert d["is_real"] is False

    def test_pairing_blocked_actions(self):
        from hermes_core.phone_connectivity import DevicePairing
        p = DevicePairing.dry_run()
        assert "live-telegram" in p.blocked_actions
        assert "direct-gemini" in p.blocked_actions

    def test_dry_run_pair_custom(self):
        from hermes_core.phone_connectivity import DevicePairing, PairingMode
        p = DevicePairing.dry_run_pair("TestPhone", "test-001")
        assert p.device_name == "TestPhone"
        assert p.device_id == "test-001"


class TestConnectivityPolicy:
    def test_default_localhost_only(self):
        from hermes_core.phone_connectivity import get_default_policy, ConnectivityMode
        p = get_default_policy()
        assert p.current_mode == ConnectivityMode.LOCALHOST_ONLY
        assert p.is_localhost_only is True

    def test_lan_disabled(self):
        from hermes_core.phone_connectivity import get_default_policy
        p = get_default_policy()
        assert p.is_lan_enabled is False

    def test_external_blocked(self):
        from hermes_core.phone_connectivity import get_default_policy
        p = get_default_policy()
        assert p.is_external_blocked is True

    def test_can_bind_localhost(self):
        from hermes_core.phone_connectivity import get_default_policy
        p = get_default_policy()
        ok, msg = p.can_bind_to("127.0.0.1")
        assert ok is True
        ok2, _ = p.can_bind_to("localhost")
        assert ok2 is True

    def test_0_0_0_0_blocked(self):
        from hermes_core.phone_connectivity import get_default_policy
        p = get_default_policy()
        ok, msg = p.can_bind_to("0.0.0.0")
        assert ok is False
        assert "blocked" in msg.lower()

    def test_lan_ip_blocked(self):
        from hermes_core.phone_connectivity import get_default_policy
        p = get_default_policy()
        for ip in ["192.168.1.1", "10.0.0.1", "172.16.0.1"]:
            ok, _ = p.can_bind_to(ip)
            assert ok is False, f"{ip} should be blocked"

    def test_public_ip_blocked(self):
        from hermes_core.phone_connectivity import get_default_policy
        p = get_default_policy()
        ok, _ = p.can_bind_to("8.8.8.8")
        assert ok is False

    def test_status_report(self):
        from hermes_core.phone_connectivity import get_default_policy
        r = get_default_policy().status_report()
        assert r["localhost_only"] is True
        assert r["external_blocked"] is True
        assert r["pairing_real_enabled"] is False

    def test_list_options(self):
        from hermes_core.phone_connectivity import get_default_policy
        p = get_default_policy()
        opts = p.list_options()
        assert len(opts) == 5

    def test_one_enabled_only(self):
        from hermes_core.phone_connectivity import get_default_policy
        p = get_default_policy()
        enabled = p.list_enabled()
        assert len(enabled) == 1
        assert enabled[0].name.startswith("Localhost")


class TestConnectivityOptions:
    def test_lan_option_disabled(self):
        from hermes_core.phone_connectivity import CONNECTIVITY_OPTIONS
        lan = [o for o in CONNECTIVITY_OPTIONS if o.mode.value == "lan_disabled"][0]
        assert lan.enabled is False
        assert "APPROVE_LAN_MODE" in lan.approval_gates

    def test_tailscale_option_disabled(self):
        from hermes_core.phone_connectivity import CONNECTIVITY_OPTIONS
        ts = [o for o in CONNECTIVITY_OPTIONS if o.mode.value == "tailscale_disabled"][0]
        assert ts.enabled is False

    def test_external_option_has_blocked_gate(self):
        from hermes_core.phone_connectivity import CONNECTIVITY_OPTIONS
        ext = [o for o in CONNECTIVITY_OPTIONS if o.mode.value == "external_blocked"][0]
        assert ext.enabled is False
        assert "BLOCKED" in ext.approval_gates[0]


class TestCLIPhoneCommands:
    def test_connectivity_status(self):
        from hermes_core.cli import phone_connectivity_status_command
        import argparse
        assert phone_connectivity_status_command(argparse.Namespace()) == 0

    def test_connectivity_options(self):
        from hermes_core.cli import phone_connectivity_options_command
        import argparse
        assert phone_connectivity_options_command(argparse.Namespace()) == 0

    def test_pairing_contract(self):
        from hermes_core.cli import phone_pairing_contract_command
        import argparse
        assert phone_pairing_contract_command(argparse.Namespace()) == 0

    def test_pairing_dry_run(self):
        from hermes_core.cli import phone_pairing_dry_run_command
        import argparse
        assert phone_pairing_dry_run_command(argparse.Namespace()) == 0

    def test_phone_security_check(self):
        from hermes_core.cli import phone_security_check_command
        import argparse
        rc = phone_security_check_command(argparse.Namespace())
        assert rc == 0  # should pass — all security checks green


class TestRegression:
    def test_malyarka(self):
        from hermes_modules.malyarka.fixtures import run_all_fixtures
        assert len(run_all_fixtures()) == 12

    def test_ai_provider(self):
        from hermes_core.ai_provider import AIProviderRouter, reset_default_registry
        from hermes_core.ai_provider.registry import get_default_registry
        reset_default_registry()
        get_default_registry()
        assert not AIProviderRouter().select("mock").is_blocked

    def test_bridge(self):
        from hermes_core.runtime_bridge import BridgeRouter, BridgeRequest, BridgeActionType
        assert BridgeRouter().handle(BridgeRequest(action=BridgeActionType.STATUS)).is_ok

    def test_mobile_gateway(self):
        from hermes_core.mobile_gateway import MobileGateway
        assert MobileGateway().status().status == "OK"

    def test_android_shell(self):
        from hermes_core.android_shell import check_required_files
        assert len(check_required_files()) == 0
