"""Tests for BATCH_111: Malyarka Export Dry-Run."""

from __future__ import annotations
import sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))


class TestCorelTXT:
    def test_first_line_empty(self):
        from hermes_modules.malyarka.export_dry_run import build_corel_txt_preview
        rows = [{"height": 720, "width": 300, "quantity": 2}]
        result = build_corel_txt_preview(rows)
        lines = result.split("\n")
        assert lines[0] == "", "First line must be empty"

    def test_no_headers(self):
        from hermes_modules.malyarka.export_dry_run import build_corel_txt_preview
        rows = [{"height": 720, "width": 300, "quantity": 2}]
        result = build_corel_txt_preview(rows)
        assert "height" not in result.lower()
        assert "width" not in result.lower()

    def test_height_width_order(self):
        from hermes_modules.malyarka.export_dry_run import build_corel_txt_preview
        rows = [{"height": 720, "width": 300, "quantity": 2}]
        result = build_corel_txt_preview(rows)
        assert "720\t300\t2" in result

    def test_only_confirmed_rows(self):
        from hermes_modules.malyarka.export_dry_run import build_corel_txt_preview
        rows = [{"height": 100, "width": 200, "quantity": 1}]
        result = build_corel_txt_preview(rows)
        assert "100\t200\t1" in result

    def test_empty_rows_no_crash(self):
        from hermes_modules.malyarka.export_dry_run import build_corel_txt_preview
        result = build_corel_txt_preview([])
        assert result == ""


class TestExcelPreview:
    def test_headers(self):
        from hermes_modules.malyarka.export_dry_run import build_excel_preview
        rows = [{"height": 720, "width": 300, "quantity": 2}]
        p = build_excel_preview(rows)
        assert "№" in p["headers"]
        assert "м²" in p["headers"]

    def test_area_calculation(self):
        from hermes_modules.malyarka.export_dry_run import build_excel_preview
        rows = [{"height": 1000, "width": 1000, "quantity": 1}]
        p = build_excel_preview(rows)
        assert p["total_area_m2"] == 1.0  # 1m x 1m = 1 m2

    def test_area_with_quantity(self):
        from hermes_modules.malyarka.export_dry_run import build_excel_preview
        rows = [{"height": 1000, "width": 500, "quantity": 2}]
        p = build_excel_preview(rows)
        assert p["total_area_m2"] == 1.0  # 0.5 * 2 = 1


class TestDisputedBlocking:
    def test_disputed_blocks_export(self):
        from hermes_modules.malyarka.export_dry_run import (
            MalyarkaExportRequest, build_export_preview,
        )
        req = MalyarkaExportRequest(
            confirmed_rows=[{"height": 100, "width": 200, "quantity": 1}],
            disputed_rows=[{"raw_text": "bad"}],
        )
        p = build_export_preview(req)
        assert p.export_allowed is False
        assert "спорные" in p.blocked_reason.lower()

    def test_no_disputed_allows(self):
        from hermes_modules.malyarka.export_dry_run import (
            MalyarkaExportRequest, build_export_preview,
        )
        req = MalyarkaExportRequest(
            confirmed_rows=[{"height": 100, "width": 200, "quantity": 1}],
        )
        p = build_export_preview(req)
        assert p.export_allowed is True


class TestSafetyPolicy:
    def test_file_write_blocked(self):
        from hermes_modules.malyarka.export_dry_run import ExportSafetyPolicy
        ok, reason = ExportSafetyPolicy.check_file_write("C:\\test")
        assert ok is False

    def test_corel_launch_blocked(self):
        from hermes_modules.malyarka.export_dry_run import ExportSafetyPolicy
        ok, _ = ExportSafetyPolicy.check_corel_launch()
        assert ok is False

    def test_e_orders_blocked(self):
        from hermes_modules.malyarka.export_dry_run import ExportSafetyPolicy
        ok, _ = ExportSafetyPolicy.check_file_write("E:\\Заказы\\test.txt")
        assert ok is False


class TestRegression:
    def test_malyarka_fixtures(self):
        from hermes_modules.malyarka.fixtures import run_all_fixtures
        assert len(run_all_fixtures()) == 12

    def test_telegram_hold(self):
        from hermes_core.telegram_live import HoldState
        assert HoldState.get().actual_live_allowed is False
