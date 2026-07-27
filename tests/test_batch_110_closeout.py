"""Tests for BATCH_110: Dry-Run Acceptance + Closeout."""

from __future__ import annotations
import sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))


class TestSignoff:
    def test_signoff_defined(self):
        from hermes_core.telegram_live import DRY_RUN_SIGNOFF
        assert "ACCEPTED" in DRY_RUN_SIGNOFF
        assert "NOT APPROVED" in DRY_RUN_SIGNOFF
        assert "NOT ENABLED" in DRY_RUN_SIGNOFF

    def test_rc_closeout(self):
        from hermes_core.telegram_live import RC_CLOSEOUT
        assert "CLOSED" in RC_CLOSEOUT
        assert "TELEGRAM-DRY-RUN-RC-1" in RC_CLOSEOUT

    def test_final_hold(self):
        from hermes_core.telegram_live import FINAL_HOLD_STATE
        assert "DRY_RUN_ACCEPTED" in FINAL_HOLD_STATE
        assert "FALSE" in FINAL_HOLD_STATE

    def test_decision_board(self):
        from hermes_core.telegram_live import OPERATOR_DECISION_BOARD
        assert "Вариант A" in OPERATOR_DECISION_BOARD
        assert "Вариант B" in OPERATOR_DECISION_BOARD

    def test_path_selector(self):
        from hermes_core.telegram_live import NEXT_PATH_SELECTOR
        assert "BATCH_111" in NEXT_PATH_SELECTOR

    def test_approval_phrase(self):
        from hermes_core.telegram_live import LIVE_APPROVAL_PHRASE
        assert "ОДОБРЯЮ" in LIVE_APPROVAL_PHRASE
        assert "НЕ ЯВЛЯЕТСЯ APPROVAL" in LIVE_APPROVAL_PHRASE

    def test_batch_without_approval_is_not_approval(self):
        from hermes_core.telegram_live import HoldState
        h = HoldState.get()
        assert h.explicit_approval_received is False
        # "BATCH_111" alone is just a string, not approval

    def test_user_summary(self):
        from hermes_core.telegram_live import FINAL_USER_SUMMARY
        assert "ЧТО ГОТОВО" in FINAL_USER_SUMMARY
        assert "ЧТО ЗАПРЕЩЕНО" in FINAL_USER_SUMMARY


class TestRegression:
    def test_malyarka(self):
        from hermes_modules.malyarka.fixtures import run_all_fixtures
        assert len(run_all_fixtures()) == 12

    def test_intent(self):
        from hermes_core.telegram_intent import TelegramIntentRouter
        assert TelegramIntentRouter().detect("привет").intent.value == "general_chat"

    def test_hold_state(self):
        from hermes_core.telegram_live import HoldState
        h = HoldState.get()
        assert h.actual_live_allowed is False
        assert h.token_read_allowed is False
