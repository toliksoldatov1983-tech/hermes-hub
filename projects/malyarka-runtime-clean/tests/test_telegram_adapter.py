import ast
import sqlite3
from pathlib import Path

import pytest

from malyarka_core.adapters.telegram import (
    build_confirmed_lines_message,
    build_disputed_lines_message,
    build_order_preview_from_text,
    build_order_summary_message,
    prepare_export_rows_from_text,
    save_order_from_text,
)
from malyarka_core.storage.repository import initialize_database


def _create_initialized_temp_database(tmp_path: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(tmp_path / "telegram_adapter.db")
    initialize_database(connection)
    return connection


def test_build_order_preview_from_text_with_confirmed_items():
    preview = build_order_preview_from_text("500 700 2\n300 400")

    assert preview["confirmed_items"] == [
        {"height": 500, "width": 700, "quantity": 2},
        {"height": 300, "width": 400, "quantity": 1},
    ]
    assert preview["disputed_items"] == []
    assert preview["confirmed_count"] == 2
    assert preview["disputed_count"] == 0
    assert preview["total_quantity"] == 3
    assert preview["total_area_m2"] == pytest.approx(0.82)
    assert preview["can_export"] is True
    assert preview["export_blocked_reason"] == ""


def test_build_order_preview_from_text_with_disputed_items():
    preview = build_order_preview_from_text("500 700 2\nтолько фасад")

    assert preview["confirmed_count"] == 1
    assert preview["disputed_count"] == 1
    assert preview["can_export"] is False
    assert preview["export_blocked_reason"]
    assert preview["disputed_items"][0]["raw"] == "только фасад"


def test_disputed_items_do_not_enter_confirmed_preview():
    preview = build_order_preview_from_text("500 700 2\nтолько фасад")

    assert preview["confirmed_items"] == [
        {"height": 500, "width": 700, "quantity": 2}
    ]
    assert all(item.get("raw") != "только фасад" for item in preview["confirmed_items"])
    assert preview["disputed_items"][0]["raw"] == "только фасад"


def test_prepare_export_rows_from_text_returns_corel_and_malyarka_rows():
    rows = prepare_export_rows_from_text("500 700 2")

    assert rows["corel_rows"] == [[], [500, 700, 2]]
    assert rows["malyarka_rows"][1][:5] == [1, 500, 700, 2, 0.7]
    assert rows["malyarka_rows"][-1][3] == 2
    assert rows["malyarka_rows"][-1][4] == 0.7


def test_prepare_export_rows_from_text_rejects_disputed_order():
    with pytest.raises(ValueError):
        prepare_export_rows_from_text("500 700 2\nтолько фасад")


def test_prepare_export_rows_from_text_rejects_empty_order():
    with pytest.raises(ValueError):
        prepare_export_rows_from_text("")


def test_save_order_from_text_uses_provided_connection(tmp_path, monkeypatch):
    original_connect = sqlite3.connect
    connection = _create_initialized_temp_database(tmp_path)

    def fail_if_adapter_opens_connection(*args, **kwargs):
        raise AssertionError("adapter must use the provided sqlite3.Connection only")

    monkeypatch.setattr(sqlite3, "connect", fail_if_adapter_opens_connection)

    result = save_order_from_text(connection, "500 700 2")

    assert result == {
        "order_id": 1,
        "confirmed_count": 1,
        "disputed_count": 0,
        "can_export": True,
    }
    assert connection.execute("SELECT COUNT(*) FROM order_items").fetchone()[0] == 1
    monkeypatch.setattr(sqlite3, "connect", original_connect)


def test_save_order_from_text_persists_confirmed_and_disputed_items(tmp_path):
    connection = _create_initialized_temp_database(tmp_path)

    result = save_order_from_text(connection, "500 700 2\nтолько фасад")

    assert result["order_id"] == 1
    assert result["confirmed_count"] == 1
    assert result["disputed_count"] == 1
    assert result["can_export"] is False
    assert connection.execute("SELECT COUNT(*) FROM order_items").fetchone()[0] == 1
    assert connection.execute("SELECT COUNT(*) FROM disputed_items").fetchone()[0] == 1


def test_build_disputed_lines_message_returns_empty_string_without_disputes():
    preview = build_order_preview_from_text("500 700 2")

    assert build_disputed_lines_message(preview) == ""


def test_build_disputed_lines_message_contains_raw_and_reason():
    preview = build_order_preview_from_text("только фасад")

    message = build_disputed_lines_message(preview)

    assert message.startswith("СПОРНЫЕ СТРОКИ:")
    assert "1. только фасад" in message
    assert preview["disputed_items"][0]["reason"] in message


def test_build_confirmed_lines_message_contains_only_height_width_quantity():
    preview = build_order_preview_from_text("500 700 2")

    message = build_confirmed_lines_message(preview)

    assert message == "ПОДТВЕРЖДЁННЫЕ СТРОКИ:\n1. 500 700 2"
    assert "м²" not in message
    assert "материал" not in message.lower()
    assert "цвет" not in message.lower()


def test_build_order_summary_message_contains_counts_area_and_export_status():
    preview = build_order_preview_from_text("500 700 2\nтолько фасад")

    message = build_order_summary_message(preview)

    assert "Подтверждённых строк: 1" in message
    assert "Спорных строк: 1" in message
    assert "Всего деталей: 2" in message
    assert "Общая площадь: 0.700 м²" in message
    assert "Можно делать экспорт: нет" in message


def test_adapter_does_not_import_telegram_aiogram_openai_or_vision():
    adapter_path = Path("malyarka_core/adapters/telegram.py")
    tree = ast.parse(adapter_path.read_text(encoding="utf-8"))
    forbidden = {"telegram", "aiogram", "openai", "vision"}
    imported_names = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_names.update(alias.name.split(".")[0].lower() for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_names.add(node.module.split(".")[0].lower())

    assert forbidden.isdisjoint(imported_names)
