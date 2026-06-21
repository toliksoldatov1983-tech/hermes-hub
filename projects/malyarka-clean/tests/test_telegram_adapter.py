import builtins
import importlib
from pathlib import Path


def test_telegram_module_import_does_not_require_token(monkeypatch):
    for name in ("TELEGRAM_TOKEN", "BOT_TOKEN", "TELEGRAM_BOT_TOKEN"):
        monkeypatch.delenv(name, raising=False)

    module = importlib.import_module("malyarka_clean_telegram")

    assert hasattr(module, "build_telegram_order_reply")


def test_telegram_module_import_does_not_read_env_file(monkeypatch):
    original_open = builtins.open
    original_path_open = Path.open

    def guarded_open(file, *args, **kwargs):
        if str(file).endswith(".env"):
            raise AssertionError(".env must not be read by Telegram skeleton")
        return original_open(file, *args, **kwargs)

    def guarded_path_open(self, *args, **kwargs):
        if str(self).endswith(".env"):
            raise AssertionError(".env must not be read by Telegram skeleton")
        return original_path_open(self, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", guarded_open)
    monkeypatch.setattr(Path, "open", guarded_path_open)

    importlib.reload(importlib.import_module("malyarka_clean_telegram"))


def test_clean_text_reply_says_clean_and_excel_can_be_created_locally():
    from malyarka_clean_telegram import build_telegram_order_reply

    reply = build_telegram_order_reply("1000 400 2\n700 300")

    assert "Статус: clean" in reply
    assert "Подтверждённые строки:" in reply
    assert "Спорные строки:\nнет" in reply
    assert "Площадь:" in reply
    assert "Excel можно создать локальным запускателем" in reply


def test_disputed_text_reply_shows_disputes_and_fix_only_disputed_rows():
    from malyarka_clean_telegram import build_telegram_order_reply

    reply = build_telegram_order_reply("1000 400 2\n1000")

    assert "Статус: has_disputes" in reply
    assert "Спорные строки:" in reply
    assert "missing_width" in reply
    assert "Исправь только спорные строки" in reply


def test_garbage_text_reply_says_empty_or_invalid():
    from malyarka_clean_telegram import build_telegram_order_reply

    reply = build_telegram_order_reply("привет\nничего непонятно")

    assert "Статус: empty_or_invalid" in reply
    assert "Заказ пустой или непонятный" in reply


def test_telegram_adapter_does_not_create_corel_export_xlsx(tmp_path, monkeypatch):
    from malyarka_clean_telegram import build_telegram_order_reply

    monkeypatch.chdir(tmp_path)

    build_telegram_order_reply("1000 400 2")

    assert not (tmp_path / "COREL_EXPORT.xlsx").exists()
    assert not (tmp_path / "outputs" / "COREL_EXPORT.xlsx").exists()


def test_telegram_adapter_does_not_start_polling():
    from malyarka_clean_telegram import get_telegram_skeleton_diagnostics

    diagnostics = get_telegram_skeleton_diagnostics()

    assert diagnostics["polling"] is False
    assert diagnostics["live_telegram"] is False
    assert diagnostics["token_required"] is False
    assert diagnostics["reads_env_file"] is False
    assert diagnostics["creates_excel"] is False
