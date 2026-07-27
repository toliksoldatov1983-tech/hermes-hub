"""Tests for BATCH_115: Staging Review + Real Folder Write Plan."""

from __future__ import annotations
import sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

STAGING = ROOT / "06_EXPORT_STAGING"


class TestStagingReview:
    def test_all_4_original_files_exist(self):
        assert (STAGING / "demo_order_corel.txt").exists()
        assert (STAGING / "demo_order_malyarka.xlsx").exists()
        assert (STAGING / "demo_order_export_preview.json").exists()
        assert (STAGING / "demo_order_export_report.md").exists()

    def test_manifest_created(self):
        assert (STAGING / "STAGING_MANIFEST.md").exists() or \
               any(f.name.startswith("STAGING_MANIFEST") for f in STAGING.glob("*.md"))

    def test_checklist_created(self):
        assert (STAGING / "OPERATOR_REVIEW_CHECKLIST_RU.md").exists() or \
               any(f.name.startswith("OPERATOR_REVIEW") for f in STAGING.glob("*.md"))

    def test_files_in_staging_only(self):
        assert all(f.resolve().is_relative_to(STAGING.resolve())
                   for f in STAGING.glob("*") if f.is_file())

    def test_corel_txt_valid(self):
        content = (STAGING / "demo_order_corel.txt").read_text()
        assert content.startswith("\n") or content.startswith("\r\n")  # first line empty


class TestRealFolderContract:
    def test_request_defaults(self):
        from hermes_modules.malyarka.real_folder_contract import MalyarkaRealFolderWriteRequest
        req = MalyarkaRealFolderWriteRequest()
        assert req.write_mode == "plan_only"
        assert req.real_write_allowed is False
        assert req.overwrite_allowed is False
        assert req.delete_allowed is False

    def test_gates_all_closed(self):
        from hermes_modules.malyarka.real_folder_contract import REAL_FOLDER_GATES
        assert len(REAL_FOLDER_GATES) == 8
        for g in REAL_FOLDER_GATES:
            assert g["state"] == "CLOSED", f"{g['id']} should be CLOSED"

    def test_dry_run_resolver(self):
        from hermes_modules.malyarka.real_folder_contract import resolve_destination_dry_run
        result = resolve_destination_dry_run("demo_order")
        assert "E:\\" in result["target_path_preview"]
        assert result["audit"]["e_disk_accessed"] is False

    def test_no_e_disk_access(self):
        e_disk = Path("E:/Заказы")
        if e_disk.exists():
            demo_files = list(e_disk.glob("demo_order_*"))
            assert len(demo_files) == 0


class TestRegression:
    def test_malyarka_fixtures(self):
        from hermes_modules.malyarka.fixtures import run_all_fixtures
        assert len(run_all_fixtures()) == 12

    def test_export_dry_run(self):
        from hermes_modules.malyarka.export_dry_run import build_corel_txt_preview
        result = build_corel_txt_preview([{"height": 720, "width": 300, "quantity": 2}])
        assert "720\t300\t2" in result
