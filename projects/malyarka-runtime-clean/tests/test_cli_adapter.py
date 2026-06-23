import ast
import subprocess
import sys
from pathlib import Path

import pytest

from malyarka_core.adapters.cli import (
    build_cli_report_from_text,
    format_cli_report,
    preview_text_order,
)


def test_build_cli_report_from_text_with_confirmed_items():
    report = build_cli_report_from_text("500 700 2\n300 400")

    assert report["confirmed_items"] == [
        {"number": 1, "height": 500, "width": 700, "quantity": 2},
        {"number": 2, "height": 300, "width": 400, "quantity": 1},
    ]
    assert report["disputed_items"] == []
    assert report["confirmed_count"] == 2
    assert report["disputed_count"] == 0
    assert report["total_quantity"] == 3
    assert report["total_area_m2"] == pytest.approx(0.82)
    assert report["can_export"] is True
    assert report["export_blocked_reason"] == ""


def test_build_cli_report_from_text_with_disputed_items():
    report = build_cli_report_from_text("500 700 2\nonly facade")

    assert report["confirmed_count"] == 1
    assert report["disputed_count"] == 1
    assert report["can_export"] is False
    assert report["export_blocked_reason"]
    assert report["disputed_items"][0]["raw"] == "only facade"


def test_cli_report_does_not_include_disputed_items_in_confirmed():
    report = build_cli_report_from_text("500 700 2\nonly facade")

    assert report["confirmed_items"] == [
        {"number": 1, "height": 500, "width": 700, "quantity": 2}
    ]
    assert all(item.get("raw") != "only facade" for item in report["confirmed_items"])
    assert report["disputed_items"][0]["raw"] == "only facade"


def test_cli_report_contains_corel_rows_when_export_allowed():
    report = build_cli_report_from_text("500 700 2")

    assert report["corel_rows"] == [[], [500, 700, 2]]
    assert report["malyarka_rows"][1][:5] == [1, 500, 700, 2, 0.7]
    assert report["archive_snapshot"]["confirmed_items_count"] == 1


def test_cli_report_blocks_export_when_disputed_items_exist():
    report = build_cli_report_from_text("500 700 2\nonly facade")

    assert report["can_export"] is False
    assert report["corel_rows"] is None
    assert report["malyarka_rows"] is None
    assert report["archive_snapshot"] is None


def test_format_cli_report_contains_summary_confirmed_and_area():
    report = build_cli_report_from_text("500 700 2")

    text = format_cli_report(report)

    assert "ИТОГ" in text
    assert "Подтверждённых строк: 1" in text
    assert "Всего деталей: 2" in text
    assert "Общая площадь: 0.700 м²" in text
    assert "ПОДТВЕРЖДЁННЫЕ СТРОКИ\n1. 500 700 2" in text


def test_format_cli_report_contains_disputed_block():
    report = build_cli_report_from_text("only facade")

    text = format_cli_report(report)

    assert "СПОРНЫЕ СТРОКИ" in text
    assert "1. only facade |" in text
    assert "Причина блокировки:" in text


def test_preview_text_order_returns_human_readable_text():
    text = preview_text_order("500 700 2")

    assert isinstance(text, str)
    assert "ИТОГ" in text
    assert "COREL ROWS" in text
    assert "[500, 700, 2]" in text


def test_preview_order_script_reads_file_and_prints_report(tmp_path):
    order_path = tmp_path / "order.txt"
    order_path.write_text("500 700 2\n300 400", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "scripts/preview_order.py", str(order_path)],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )

    assert result.returncode == 0
    assert "ИТОГ" in result.stdout
    assert "Подтверждённых строк: 2" in result.stdout
    assert "1. 500 700 2" in result.stdout
    assert result.stderr == ""


def test_preview_order_script_handles_missing_file():
    result = subprocess.run(
        [sys.executable, "scripts/preview_order.py", "missing-order.txt"],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )

    assert result.returncode == 1
    assert "Файл не найден: missing-order.txt" in result.stdout
    assert result.stderr == ""


def test_cli_adapter_does_not_import_telegram_aiogram_openai_or_vision():
    adapter_path = Path("malyarka_core/adapters/cli.py")
    tree = ast.parse(adapter_path.read_text(encoding="utf-8"))
    forbidden = {"telegram", "aiogram", "openai", "vision"}
    imported_names = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_names.update(alias.name.split(".")[0].lower() for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_names.add(node.module.split(".")[0].lower())

    assert forbidden.isdisjoint(imported_names)
