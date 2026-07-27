"""Tests for BATCH_107: User Acceptance + Freeze."""

from __future__ import annotations
import sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))


class TestAcceptanceScenarios:
    def test_scenarios_count(self):
        from hermes_core.telegram_live import ACCEPTANCE_SCENARIOS
        assert len(ACCEPTANCE_SCENARIOS) == 10

    def test_all_accepted(self):
        from hermes_core.telegram_live import ACCEPTANCE_SCENARIOS
        for s in ACCEPTANCE_SCENARIOS:
            assert s.accepted is True, f"{s.scenario_id} should be accepted"

    def test_covers_all_types(self):
        from hermes_core.telegram_live import ACCEPTANCE_SCENARIOS
        ids = {s.scenario_id for s in ACCEPTANCE_SCENARIOS}
        assert "A01" in ids  # general chat
        assert "A03" in ids  # explicit order
        assert "A04" in ids  # ambiguous
        assert "A07" in ids  # confirmation dry-run
        assert "A10" in ids  # dangerous action

    def test_expected_responses(self):
        from hermes_core.telegram_live import EXPECTED_BOT_RESPONSES
        assert len(EXPECTED_BOT_RESPONSES) == 9

    def test_responses_no_internal_classes(self):
        from hermes_core.telegram_live import EXPECTED_BOT_RESPONSES
        for _, resp in EXPECTED_BOT_RESPONSES:
            assert "BridgeActionType" not in resp
            assert "IntentType" not in resp
            assert "class " not in resp

    def test_responses_no_secrets(self):
        from hermes_core.telegram_live import EXPECTED_BOT_RESPONSES
        for _, resp in EXPECTED_BOT_RESPONSES:
            assert "token" not in resp.lower()
            assert "api_key" not in resp.lower()


class TestFreezeAndBlockers:
    def test_freeze_defined(self):
        from hermes_core.telegram_live import DRY_RUN_FREEZE
        assert "FREEZE" in DRY_RUN_FREEZE

    def test_blockers_count(self):
        from hermes_core.telegram_live import LIVE_BLOCKERS_FINAL
        assert len(LIVE_BLOCKERS_FINAL) == 9

    def test_final_go_nogo(self):
        from hermes_core.telegram_live import FINAL_GO_NOGO
        assert "GO" in FINAL_GO_NOGO
        assert "NO-GO" in FINAL_GO_NOGO

    def test_acceptance_checklist(self):
        from hermes_core.telegram_live import ACCEPTANCE_CHECKLIST
        assert "ALL CRITERIA PASSED" in ACCEPTANCE_CHECKLIST


class TestCLIAcceptance:
    def test_acceptance_status(self):
        from hermes_core.cli import telegram_acceptance_status_command
        import argparse
        assert telegram_acceptance_status_command(argparse.Namespace()) == 0

    def test_acceptance_checklist(self):
        from hermes_core.cli import telegram_acceptance_checklist_command
        import argparse
        assert telegram_acceptance_checklist_command(argparse.Namespace()) == 0

    def test_freeze_status(self):
        from hermes_core.cli import telegram_dry_run_freeze_status_command
        import argparse
        assert telegram_dry_run_freeze_status_command(argparse.Namespace()) == 0


class TestRegression:
    def test_malyarka(self):
        from hermes_modules.malyarka.fixtures import run_all_fixtures
        assert len(run_all_fixtures()) == 12

    def test_intent_router(self):
        from hermes_core.telegram_intent import TelegramIntentRouter
        assert TelegramIntentRouter().detect("привет").intent.value == "general_chat"

    def test_e2e(self):
        from hermes_core.telegram_e2e import E2EScenarioRunner, build_all_scenarios
        results = E2EScenarioRunner().run_all(build_all_scenarios())
        assert all(r.passed for r in results)
