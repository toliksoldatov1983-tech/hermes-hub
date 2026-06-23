import ast
import importlib
from pathlib import Path

from malyarka_telegram.config import TelegramConfig, load_config


def test_import_app_does_not_require_token_or_start_polling(monkeypatch):
    monkeypatch.delenv("MALYARKA_TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.delenv("BOT_TOKEN", raising=False)

    app_module = importlib.import_module("malyarka_telegram.app")

    assert hasattr(app_module, "create_app")
    assert not Path("hermes_bot.py").exists()


def test_import_app_does_not_import_aiogram_or_create_runtime_objects(monkeypatch):
    monkeypatch.delenv("MALYARKA_TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.delenv("BOT_TOKEN", raising=False)

    app_module = importlib.import_module("malyarka_telegram.app")

    assert "Bot" not in vars(app_module)
    assert "Dispatcher" not in vars(app_module)


def test_create_app_returns_status_without_polling():
    from malyarka_telegram.app import create_app

    status = create_app(TelegramConfig(bot_token=None))

    assert status["has_token"] is False
    assert status["polling_started"] is False
    assert "ready" in status


def test_check_diagnostics_do_not_start_polling_without_token(monkeypatch):
    from malyarka_telegram.app import get_diagnostics, main

    monkeypatch.delenv("MALYARKA_TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.delenv("BOT_TOKEN", raising=False)

    diagnostics = get_diagnostics()

    assert diagnostics["has_token"] is False
    assert diagnostics["polling_started"] is False
    assert diagnostics["handle_text_message_available"] is True
    assert diagnostics["hermes_router_available"] is True
    assert main(["--check"]) == 0


def test_run_polling_without_token_returns_error_without_starting_polling(
    monkeypatch, capsys
):
    from malyarka_telegram import app as app_module

    monkeypatch.delenv("MALYARKA_TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.delenv("BOT_TOKEN", raising=False)

    async def fail_if_polling_starts(*args, **kwargs):
        raise AssertionError("polling must not start without a token")

    monkeypatch.setattr(app_module, "_run_aiogram_polling", fail_if_polling_starts)

    exit_code = app_module.main(["--run-polling"])
    output = capsys.readouterr()

    assert exit_code == 2
    assert "Telegram token is not configured" in output.err
    assert "token-for-test" not in output.out
    assert "token-for-test" not in output.err


def test_run_polling_without_aiogram_returns_error_without_traceback(
    monkeypatch, capsys
):
    from malyarka_telegram import app as app_module

    async def fail_if_polling_starts(*args, **kwargs):
        raise AssertionError("polling must not start without aiogram")

    monkeypatch.setattr(app_module, "_is_aiogram_available", lambda: False)
    monkeypatch.setattr(app_module, "_run_aiogram_polling", fail_if_polling_starts)

    exit_code = app_module.run_polling(TelegramConfig(bot_token="fake-token"))
    output = capsys.readouterr()

    assert exit_code == 3
    assert "aiogram is not installed" in output.err
    assert "Traceback" not in output.err
    assert "fake-token" not in output.out
    assert "fake-token" not in output.err


def test_run_polling_handles_telegram_unauthorized_without_traceback(
    monkeypatch, capsys
):
    from malyarka_telegram import app as app_module

    class TelegramUnauthorizedError(Exception):
        pass

    async def fail_with_unauthorized(*args, **kwargs):
        raise TelegramUnauthorizedError("secret-token-for-test")

    monkeypatch.setattr(app_module, "_is_aiogram_available", lambda: True)
    monkeypatch.setattr(app_module, "_run_aiogram_polling", fail_with_unauthorized)

    exit_code = app_module.run_polling(TelegramConfig(bot_token="secret-token-for-test"))
    output = capsys.readouterr()

    assert exit_code == app_module.POLLING_EXIT_UNAUTHORIZED
    assert "Unauthorized" in output.err
    assert "Traceback" not in output.err
    assert "secret-token-for-test" not in output.out
    assert "secret-token-for-test" not in output.err


def test_run_polling_handles_telegram_conflict_without_traceback(
    monkeypatch, capsys
):
    from malyarka_telegram import app as app_module

    class TelegramConflictError(Exception):
        pass

    async def fail_with_conflict(*args, **kwargs):
        raise TelegramConflictError("another getUpdates request")

    monkeypatch.setattr(app_module, "_is_aiogram_available", lambda: True)
    monkeypatch.setattr(app_module, "_run_aiogram_polling", fail_with_conflict)

    exit_code = app_module.run_polling(TelegramConfig(bot_token="secret-token-for-test"))
    output = capsys.readouterr()

    assert exit_code == app_module.POLLING_EXIT_CONFLICT
    assert "another bot instance" in output.err
    assert "Traceback" not in output.err
    assert "secret-token-for-test" not in output.out
    assert "secret-token-for-test" not in output.err


def test_diagnostics_hide_token_value(monkeypatch, capsys):
    from malyarka_telegram.app import get_diagnostics, main

    fake_token = "fake-secret-token-for-test"
    monkeypatch.setenv("MALYARKA_TELEGRAM_BOT_TOKEN", fake_token)
    monkeypatch.delenv("BOT_TOKEN", raising=False)

    diagnostics = get_diagnostics()
    exit_code = main(["--check"])
    output = capsys.readouterr().out

    assert exit_code == 0
    assert diagnostics["has_token"] is True
    assert diagnostics["polling_started"] is False
    assert fake_token not in output
    assert "has_token" in output


def test_config_prefers_project_token_environment(monkeypatch):
    monkeypatch.setenv("MALYARKA_TELEGRAM_BOT_TOKEN", "primary-token")
    monkeypatch.setenv("BOT_TOKEN", "fallback-token")

    config = load_config()

    assert config.bot_token == "primary-token"


def test_aiogram_is_optional_for_import_and_check():
    from malyarka_telegram.app import get_diagnostics

    diagnostics = get_diagnostics(TelegramConfig(bot_token=None))

    assert "aiogram_available" in diagnostics
    assert diagnostics["polling_started"] is False


def test_no_forbidden_files_are_created_or_used_by_safe_launch():
    assert not Path("hermes_bot.py").exists()

    imported_names = _collect_imported_names(Path("malyarka_telegram"))

    assert "bot" not in imported_names
    assert "bot_backup_before_vision" not in imported_names


def test_safe_launch_source_does_not_reference_env_file_or_orders_db():
    app_source = Path("malyarka_telegram/app.py").read_text(encoding="utf-8")
    config_source = Path("malyarka_telegram/config.py").read_text(encoding="utf-8")
    combined = app_source + "\n" + config_source

    assert "orders.db" not in combined
    assert "dotenv" not in combined


def test_aiogram_is_imported_only_inside_explicit_polling_function():
    tree = ast.parse(Path("malyarka_telegram/app.py").read_text(encoding="utf-8"))
    module_imports: set[str] = set()
    aiogram_import_functions: set[str] = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                module_imports.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_name = node.module.split(".")[0]
            parent = _find_parent_function(tree, node)
            if imported_name == "aiogram" and parent is not None:
                aiogram_import_functions.add(parent.name)
            elif parent is None:
                module_imports.add(imported_name)

    assert "aiogram" not in module_imports
    assert aiogram_import_functions == {
        "_build_telegram_document",
        "_run_aiogram_polling",
    }


def _collect_imported_names(root: Path) -> set[str]:
    imported_names: set[str] = set()

    for path in root.glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_names.update(
                    alias.name.split(".")[0].lower() for alias in node.names
                )
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_names.add(node.module.split(".")[0].lower())

    return imported_names


def _find_parent_function(
    tree: ast.AST, target: ast.AST
) -> ast.FunctionDef | ast.AsyncFunctionDef | None:
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if target in ast.walk(node):
                return node
    return None
