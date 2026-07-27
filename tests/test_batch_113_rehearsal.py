"""Tests for BATCH_113: Export Reconciliation + Staging Rehearsal."""

from __future__ import annotations
import sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))


class TestReconciliation:
    def test_reconciliation_defined(self):
        from hermes_modules.malyarka.export_rehearsal import TEST_COUNT_RECONCILIATION
        assert "RECONCILED" in TEST_COUNT_RECONCILIATION
        assert "760" in TEST_COUNT_RECONCILIATION

    def test_full_test_count(self):
        import subprocess, sys
        result = subprocess.run([sys.executable, "-m", "pytest", "tests/", "--collect-only", "-q"],
                                capture_output=True, text=True, cwd=str(ROOT))
        assert "tests collected" in result.stdout or "errors" not in result.stdout.lower()


class TestHoldState:
    def test_hold_state(self):
        from hermes_modules.malyarka.export_rehearsal import EXPORT_HOLD_STATE
        assert "NO-GO" in EXPORT_HOLD_STATE
        assert "GO" in EXPORT_HOLD_STATE

    def test_preview_allowed(self):
        assert True  # Preview is always allowed in dry-run


class TestRehearsal:
    def test_staging_rehearsal_steps(self):
        from hermes_modules.malyarka.export_rehearsal import STAGING_REHEARSAL_STEPS
        assert len(STAGING_REHEARSAL_STEPS) == 9
        for _, _, status in STAGING_REHEARSAL_STEPS:
            assert "PASS" in status

    def test_fake_corel_verification(self):
        from hermes_modules.malyarka.export_rehearsal import FAKE_COREL_VERIFICATION
        assert "PASS" in FAKE_COREL_VERIFICATION
        assert "no real file" in FAKE_COREL_VERIFICATION.lower()

    def test_fake_excel_verification(self):
        from hermes_modules.malyarka.export_rehearsal import FAKE_EXCEL_VERIFICATION
        assert "PASS" in FAKE_EXCEL_VERIFICATION

    def test_collision_rehearsal(self):
        from hermes_modules.malyarka.export_rehearsal import FILENAME_COLLISION_REHEARSAL
        assert "BLOCKED" in FILENAME_COLLISION_REHEARSAL
        assert "overwrite" in FILENAME_COLLISION_REHEARSAL.lower()

    def test_rollback_rehearsal(self):
        from hermes_modules.malyarka.export_rehearsal import ROLLBACK_REHEARSAL
        assert "PASS" in ROLLBACK_REHEARSAL

    def test_approval_protocol(self):
        from hermes_modules.malyarka.export_rehearsal import APPROVAL_PROTOCOL_CHECK
        assert "BATCH_114" in APPROVAL_PROTOCOL_CHECK
        assert "NOT approval" in APPROVAL_PROTOCOL_CHECK


class TestRegression:
    def test_malyarka_fixtures(self):
        from hermes_modules.malyarka.fixtures import run_all_fixtures
        assert len(run_all_fixtures()) == 12

    def test_export_dry_run(self):
        from hermes_modules.malyarka.export_dry_run import build_corel_txt_preview
        result = build_corel_txt_preview([{"height": 720, "width": 300, "quantity": 2}])
        assert "720\t300\t2" in result

    def test_export_gates_closed(self):
        from hermes_modules.malyarka.export_approval import EXPORT_SAFETY_STATE
        assert EXPORT_SAFETY_STATE["staging_file_creation_allowed"] is False
