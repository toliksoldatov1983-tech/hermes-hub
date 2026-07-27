"""Tests for BATCH_112: Export Approval Gates + Controlled File Creation."""

from __future__ import annotations
import sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))


class TestExportGates:
    def test_gates_count(self):
        from hermes_modules.malyarka.export_approval import EXPORT_APPROVAL_GATES
        assert len(EXPORT_APPROVAL_GATES) == 11

    def test_all_gates_closed(self):
        from hermes_modules.malyarka.export_approval import EXPORT_APPROVAL_GATES
        for g in EXPORT_APPROVAL_GATES:
            assert g.default_state == "CLOSED", f"{g.gate_id} should be CLOSED"

    def test_preview_allowed_while_creation_blocked(self):
        from hermes_modules.malyarka.export_approval import EXPORT_SAFETY_STATE
        assert EXPORT_SAFETY_STATE["preview_allowed"] is True
        assert EXPORT_SAFETY_STATE["staging_file_creation_allowed"] is False

    def test_real_folder_blocked(self):
        from hermes_modules.malyarka.export_approval import EXPORT_SAFETY_STATE
        assert EXPORT_SAFETY_STATE["real_order_folder_write_allowed"] is False

    def test_corel_blocked(self):
        from hermes_modules.malyarka.export_approval import EXPORT_SAFETY_STATE
        assert EXPORT_SAFETY_STATE["corel_automation_allowed"] is False

    def test_drive_blocked(self):
        from hermes_modules.malyarka.export_approval import EXPORT_SAFETY_STATE
        assert EXPORT_SAFETY_STATE["google_drive_allowed"] is False


class TestPlans:
    def test_file_creation_plan(self):
        from hermes_modules.malyarka.export_approval import FILE_CREATION_PLAN
        assert "STAGE 0" in FILE_CREATION_PLAN
        assert "BLOCKED" in FILE_CREATION_PLAN

    def test_staging_policy(self):
        from hermes_modules.malyarka.export_approval import STAGING_POLICY
        assert "E:\\" in STAGING_POLICY or "Заказы" in STAGING_POLICY

    def test_file_naming(self):
        from hermes_modules.malyarka.export_approval import FILE_NAMING_CONTRACT
        assert "corel.txt" in FILE_NAMING_CONTRACT
        assert "malyarka.xlsx" in FILE_NAMING_CONTRACT

    def test_overwrite_protection(self):
        from hermes_modules.malyarka.export_approval import OVERWRITE_PROTECTION
        assert "overwrite_allowed = False" in OVERWRITE_PROTECTION

    def test_preflight(self):
        from hermes_modules.malyarka.export_approval import EXPORT_PREFLIGHT
        assert "PASS" in EXPORT_PREFLIGHT
        assert "NO-GO" in EXPORT_PREFLIGHT

    def test_approval_wording(self):
        from hermes_modules.malyarka.export_approval import EXPORT_APPROVAL_WORDING
        assert "BATCH_113" in EXPORT_APPROVAL_WORDING
        assert "STAGING FILE CREATION" in EXPORT_APPROVAL_WORDING


class TestRegression:
    def test_malyarka_fixtures(self):
        from hermes_modules.malyarka.fixtures import run_all_fixtures
        assert len(run_all_fixtures()) == 12

    def test_export_dry_run(self):
        from hermes_modules.malyarka.export_dry_run import build_corel_txt_preview
        rows = [{"height": 720, "width": 300, "quantity": 2}]
        result = build_corel_txt_preview(rows)
        assert "720\t300\t2" in result
