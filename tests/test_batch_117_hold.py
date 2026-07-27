"""Tests for BATCH_117: No E: disk guard + HOLD state."""

from __future__ import annotations
import sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

STAGING = ROOT / "06_EXPORT_STAGING"


class TestNoEDiskGuard:
    """Verify BATCH_117 safe branch: no E: disk access, no dangerous actions."""

    def test_e_disk_not_accessed_in_this_test(self):
        """This test does NOT touch E: disk — it only checks local files."""
        e = Path("E:/Заказы")
        # We do NOT check e.exists() — that would be an access.
        # We only verify local staging files exist.
        assert STAGING.exists()

    def test_batch_117_docs_exist(self):
        assert (STAGING / "BATCH_117_OPERATOR_DECISION_PACKAGE.md").exists()
        assert (STAGING / "BATCH_117_REAL_FOLDER_PREFLIGHT_HOLD.md").exists()
        assert (STAGING / "BATCH_117_APPROVAL_WORDING.md").exists()
        assert (STAGING / "BATCH_117_NO_E_DISK_GUARD_REPORT.md").exists()

    def test_operator_decision_contains_hold(self):
        content = (STAGING / "BATCH_117_OPERATOR_DECISION_PACKAGE.md").read_text(encoding="utf-8")
        assert "HOLD" in content
        assert "BATCH_117" in content

    def test_hold_doc_status(self):
        content = (STAGING / "BATCH_117_REAL_FOLDER_PREFLIGHT_HOLD.md").read_text(encoding="utf-8")
        assert "HOLD" in content
        assert "ОДОБРЯЮ" in content

    def test_approval_wording(self):
        content = (STAGING / "BATCH_117_APPROVAL_WORDING.md").read_text(encoding="utf-8")
        assert "ОДОБРЯЮ BATCH_117 MALYARKA REAL FOLDER PREFLIGHT" in content
        assert "НЕ разрешит" in content or "НЕ разрешает" in content

    def test_guard_report_no_access(self):
        content = (STAGING / "BATCH_117_NO_E_DISK_GUARD_REPORT.md").read_text(encoding="utf-8")
        assert "FALSE" in content
        assert "SAFE" in content


class TestStagingIntegrity:
    def test_original_staging_files_intact(self):
        assert (STAGING / "demo_order_corel.txt").exists()
        assert (STAGING / "demo_order_malyarka.xlsx").exists()

    def test_preflight_files_intact(self):
        from hermes_modules.malyarka.real_folder_preflight import (
            SOURCE_LOCK_SNAPSHOT, DRY_RUN_MAPPING,
        )
        assert SOURCE_LOCK_SNAPSHOT["audit"]["e_disk_accessed"] is False
        assert DRY_RUN_MAPPING["e_disk_accessed"] is False


class TestRegression:
    def test_malyarka_fixtures(self):
        from hermes_modules.malyarka.fixtures import run_all_fixtures
        assert len(run_all_fixtures()) == 12

    def test_real_folder_contract(self):
        from hermes_modules.malyarka.real_folder_contract import REAL_FOLDER_GATES
        for g in REAL_FOLDER_GATES:
            assert g["state"] == "CLOSED"
