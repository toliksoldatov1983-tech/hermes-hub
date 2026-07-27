"""Tests for BATCH_116: Real Folder Preflight Package."""

from __future__ import annotations
import sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))


class TestPreflightPackage:
    def test_package_defined(self):
        from hermes_modules.malyarka.real_folder_preflight import PREFLIGHT_PACKAGE
        assert "PREFLIGHT PACKAGE" in PREFLIGHT_PACKAGE
        assert "06_EXPORT_STAGING" in PREFLIGHT_PACKAGE

    def test_source_lock(self):
        from hermes_modules.malyarka.real_folder_preflight import SOURCE_LOCK_SNAPSHOT
        assert SOURCE_LOCK_SNAPSHOT["locked_for_review"] is True
        assert SOURCE_LOCK_SNAPSHOT["real_folder_write_allowed"] is False
        assert SOURCE_LOCK_SNAPSHOT["audit"]["e_disk_accessed"] is False

    def test_dry_run_mapping(self):
        from hermes_modules.malyarka.real_folder_preflight import DRY_RUN_MAPPING
        assert DRY_RUN_MAPPING["e_disk_accessed"] is False
        assert DRY_RUN_MAPPING["files_copied"] is False
        assert DRY_RUN_MAPPING["write_allowed_now"] is False
        assert len(DRY_RUN_MAPPING["mappings"]) == 3

    def test_naming_rules(self):
        from hermes_modules.malyarka.real_folder_preflight import TARGET_FOLDER_NAMING_RULES
        assert "E:\\" in TARGET_FOLDER_NAMING_RULES or "Заказы" in TARGET_FOLDER_NAMING_RULES

    def test_copy_plan(self):
        from hermes_modules.malyarka.real_folder_preflight import COPY_PLAN_WITHOUT_COPY
        assert "COPY NOT PERFORMED" in COPY_PLAN_WITHOUT_COPY

    def test_risk_register(self):
        from hermes_modules.malyarka.real_folder_preflight import RISK_REGISTER
        assert len(RISK_REGISTER["risks"]) == 10

    def test_readiness(self):
        from hermes_modules.malyarka.real_folder_preflight import READINESS_SNAPSHOT
        assert "GO" in READINESS_SNAPSHOT
        assert "NO-GO" in READINESS_SNAPSHOT

    def test_approval_wording(self):
        from hermes_modules.malyarka.real_folder_preflight import APPROVAL_WORDING_B117
        assert "BATCH_117" in APPROVAL_WORDING_B117


class TestNoEDiskAccess:
    def test_no_e_disk_mapping_access(self):
        from hermes_modules.malyarka.real_folder_preflight import DRY_RUN_MAPPING
        assert DRY_RUN_MAPPING["e_disk_accessed"] is False
        assert DRY_RUN_MAPPING["target_path_checked"] is False

    def test_staging_files_still_intact(self):
        staging = ROOT / "06_EXPORT_STAGING"
        assert (staging / "demo_order_corel.txt").exists()


class TestRegression:
    def test_malyarka_fixtures(self):
        from hermes_modules.malyarka.fixtures import run_all_fixtures
        assert len(run_all_fixtures()) == 12

    def test_export_dry_run(self):
        from hermes_modules.malyarka.export_dry_run import build_corel_txt_preview
        result = build_corel_txt_preview([{"height": 720, "width": 300, "quantity": 2}])
        assert "720\t300\t2" in result

    def test_real_folder_gates_closed(self):
        from hermes_modules.malyarka.real_folder_contract import REAL_FOLDER_GATES
        for g in REAL_FOLDER_GATES:
            assert g["state"] == "CLOSED"
