"""Tests for BATCH_109: RC Stabilization + No-Approval Hold."""

from __future__ import annotations
import sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))


class TestHoldState:
    def test_hold_state_defaults(self):
        from hermes_core.telegram_live import HoldState
        h = HoldState.get()
        assert h.current_state == "WAITING_FOR_USER_DECISION"
        assert h.dry_run_rc_ready is True
        assert h.actual_live_allowed is False
        assert h.explicit_approval_received is False
        assert h.all_gates_closed is True
        assert h.token_read_allowed is False
        assert h.polling_allowed is False
        assert h.send_allowed is False

    def test_approval_phrase(self):
        from hermes_core.telegram_live import HoldState
        h = HoldState.get()
        assert "BATCH_110" in h.approval_phrase

    def test_audit(self):
        from hermes_core.telegram_live import HoldState
        h = HoldState.get()
        assert h.audit["live_allowed"] is False
        assert h.audit["token_read"] is False


class TestRcStabilization:
    def test_stabilization_defined(self):
        from hermes_core.telegram_live import RC_STABILIZATION
        assert "STABLE" in RC_STABILIZATION

    def test_consistency_check(self):
        from hermes_core.telegram_live import RELEASE_CONSISTENCY_CHECK
        assert "OK" in RELEASE_CONSISTENCY_CHECK
        assert "нет противоречий" in RELEASE_CONSISTENCY_CHECK

    def test_handoff_check(self):
        from hermes_core.telegram_live import OPERATOR_HANDOFF_CHECK
        assert "OK" in OPERATOR_HANDOFF_CHECK

    def test_acceptance_verification(self):
        from hermes_core.telegram_live import ACCEPTANCE_REPLAY_VERIFICATION
        assert "PASS" in ACCEPTANCE_REPLAY_VERIFICATION


class TestApprovalBoard:
    def test_phrase_board(self):
        from hermes_core.telegram_live import APPROVAL_PHRASE_BOARD
        assert "ОДОБРЯЮ" in APPROVAL_PHRASE_BOARD
        assert "BATCH_110" in APPROVAL_PHRASE_BOARD

    def test_command_matrix(self):
        from hermes_core.telegram_live import FINAL_COMMAND_MATRIX
        assert "COMMAND MATRIX" in FINAL_COMMAND_MATRIX

    def test_decision_dashboard(self):
        from hermes_core.telegram_live import DECISION_READY_DASHBOARD
        assert "DECISION-READY" in DECISION_READY_DASHBOARD
        assert "BATCH_110" in DECISION_READY_DASHBOARD


class TestCLIStabilization:
    def test_rc_stabilization_cli(self):
        from hermes_core.cli import telegram_rc_stabilization_status_command
        import argparse
        assert telegram_rc_stabilization_status_command(argparse.Namespace()) == 0

    def test_consistency_cli(self):
        from hermes_core.cli import telegram_release_consistency_check_command
        import argparse
        assert telegram_release_consistency_check_command(argparse.Namespace()) == 0


class TestRegression:
    def test_malyarka(self):
        from hermes_modules.malyarka.fixtures import run_all_fixtures
        assert len(run_all_fixtures()) == 12

    def test_intent(self):
        from hermes_core.telegram_intent import TelegramIntentRouter
        assert TelegramIntentRouter().detect("привет").intent.value == "general_chat"
