"""Tests for BATCH_106: Operator Console + Failure Drills."""

from __future__ import annotations
import sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))


class TestOperatorConsole:
    def test_console_defined(self):
        from hermes_core.telegram_live import OPERATOR_CONSOLE
        assert "OPERATOR CONSOLE" in OPERATOR_CONSOLE
        assert "NO-GO" in OPERATOR_CONSOLE

    def test_console_shows_readiness(self):
        from hermes_core.telegram_live import OPERATOR_CONSOLE
        assert "READINESS_ONLY" in OPERATOR_CONSOLE
        assert "DISABLED" in OPERATOR_CONSOLE


class TestLiveBlockers:
    def test_blockers_count(self):
        from hermes_core.telegram_live import LIVE_BLOCKERS
        assert len(LIVE_BLOCKERS) == 10

    def test_all_blockers_blocked(self):
        from hermes_core.telegram_live import LIVE_BLOCKERS
        for b in LIVE_BLOCKERS:
            assert b.current_status == "BLOCKED", f"{b.blocker_id} should be BLOCKED"

    def test_blockers_board(self):
        from hermes_core.telegram_live import BLOCKERS_BOARD
        assert "LIVE BLOCKERS BOARD" in BLOCKERS_BOARD


class TestPreLiveChecklist:
    def test_checklist_count(self):
        from hermes_core.telegram_live import PRE_LIVE_CHECKLIST
        assert len(PRE_LIVE_CHECKLIST) == 15

    def test_ready_items(self):
        from hermes_core.telegram_live import PRE_LIVE_CHECKLIST
        ready = [c for c in PRE_LIVE_CHECKLIST if c[2] == "READY"]
        assert len(ready) >= 9, "At least 9 hardening items should be READY"


class TestFailureDrills:
    def test_drills_count(self):
        from hermes_core.telegram_live import FAILURE_DRILLS
        assert len(FAILURE_DRILLS) == 10

    def test_all_drills_blocked(self):
        from hermes_core.telegram_live import FAILURE_DRILLS
        for d in FAILURE_DRILLS:
            assert d.blocked is True, f"{d.drill_id} should expect BLOCKED"
            assert "BLOCKED" in d.expected_result

    def test_run_failure_drills(self):
        from hermes_core.telegram_live import run_failure_drills
        transcripts = run_failure_drills()
        assert len(transcripts) == 10
        for t in transcripts:
            assert "PASS" in t


class TestSafeRecovery:
    def test_recovery_plan(self):
        from hermes_core.telegram_live import SAFE_RECOVERY_PLAN
        assert "Safe Recovery" in SAFE_RECOVERY_PLAN
        assert "dry-run" in SAFE_RECOVERY_PLAN.lower()


class TestApprovalWording:
    def test_approval_wording(self):
        from hermes_core.telegram_live import FINAL_APPROVAL_WORDING
        assert "BATCH_107" in FINAL_APPROVAL_WORDING
        assert "LIVE PREFLIGHT" in FINAL_APPROVAL_WORDING


class TestCLIOperatorCommands:
    def test_operator_console(self):
        from hermes_core.cli import telegram_operator_console_command
        import argparse
        assert telegram_operator_console_command(argparse.Namespace()) == 0

    def test_blockers_board(self):
        from hermes_core.cli import telegram_live_blockers_board_command
        import argparse
        assert telegram_live_blockers_board_command(argparse.Namespace()) == 0

    def test_pre_live_checklist(self):
        from hermes_core.cli import telegram_pre_live_checklist_command
        import argparse
        assert telegram_pre_live_checklist_command(argparse.Namespace()) == 0

    def test_drills_run_all(self):
        from hermes_core.cli import telegram_failure_drills_run_all_command
        import argparse
        assert telegram_failure_drills_run_all_command(argparse.Namespace()) == 0


class TestRegression:
    def test_malyarka(self):
        from hermes_modules.malyarka.fixtures import run_all_fixtures
        assert len(run_all_fixtures()) == 12

    def test_intent_router(self):
        from hermes_core.telegram_intent import TelegramIntentRouter
        assert TelegramIntentRouter().detect("привет").intent.value == "general_chat"

    def test_e2e(self):
        from hermes_core.telegram_e2e import E2EScenarioRunner, build_all_scenarios
        runner = E2EScenarioRunner()
        results = runner.run_all(build_all_scenarios())
        assert all(r.passed for r in results)
