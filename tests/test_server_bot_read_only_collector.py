from pathlib import Path
import runpy


COLLECTOR_PATH = Path("E:/Hermes-Hub/tools/server_bot/collect_server_bot_read_only.py")


def _collector():
    return runpy.run_path(str(COLLECTOR_PATH))


def test_whitelist_contains_expected_files():
    module = _collector()
    whitelist = module["WHITELIST_FILES"]

    assert "malyarka_telegram/app.py" in whitelist
    assert "malyarka_telegram/handlers.py" in whitelist
    assert "malyarka_core/services/orders.py" in whitelist
    assert "requirements.txt" in whitelist


def test_env_and_token_like_paths_are_forbidden():
    module = _collector()
    is_forbidden_path = module["is_forbidden_path"]

    assert is_forbidden_path(".env") is True
    assert is_forbidden_path("malyarka_telegram/token.txt") is True
    assert is_forbidden_path("logs/bot.log") is True
    assert is_forbidden_path("orders.db") is True


def test_collector_source_does_not_use_dangerous_runtime_tools():
    source = COLLECTOR_PATH.read_text(encoding="utf-8")
    imports = _imports_from_source(source)

    assert "subprocess" not in imports
    assert "run(" not in source
    assert "Popen" not in source
    assert "os.environ" not in source
    assert "importlib" not in source
    assert "malyarka_telegram" not in imports
    assert "malyarka_core" not in imports
    assert "aiogram" not in imports


def test_redaction_masks_secret_like_lines():
    module = _collector()
    redact_line = module["redact_line"]

    assert redact_line("BOT_TOKEN: 'abc'") == "[REDACTED: suspicious secret-like line]"
    assert redact_line("PASSWORD='abc'") == "[REDACTED: suspicious secret-like line]"
    assert redact_line("PRIVATE_KEY='abc'") == "[REDACTED: suspicious secret-like line]"
    assert redact_line("safe = True") == "safe = True"


def test_report_created_on_temporary_project_copy(tmp_path):
    project = tmp_path / "bot"
    telegram = project / "malyarka_telegram"
    core_services = project / "malyarka_core" / "services"
    telegram.mkdir(parents=True)
    core_services.mkdir(parents=True)
    (project / "malyarka_core").mkdir(exist_ok=True)

    (telegram / "app.py").write_text(
        "from malyarka_telegram.router import router\n"
        "def main():\n"
        "    run_polling()\n"
        "BOT_TOKEN: 'must_hide'\n",
        encoding="utf-8",
    )
    (telegram / "handlers.py").write_text(
        "@router.message(Command('start'))\n"
        "async def start(message):\n"
        "    pass\n",
        encoding="utf-8",
    )
    (telegram / "keyboards.py").write_text(
        "InlineKeyboardButton(text='OK', callback_data='ok')\n",
        encoding="utf-8",
    )
    (project / "malyarka_core" / "parsing.py").write_text("def parse_order(text): pass\n", encoding="utf-8")
    (core_services / "orders.py").write_text("def save_order(order): pass\n", encoding="utf-8")
    (project / "requirements.txt").write_text("aiogram\n", encoding="utf-8")

    module = _collector()
    output = tmp_path / "SERVER_BOT_READ_ONLY_REPORT.md"
    module["write_report"](project, output)

    report = output.read_text(encoding="utf-8")
    assert "## Safety status" in report
    assert "read_only: true" in report
    assert "## Whitelist files checked" in report
    assert "malyarka_telegram/app.py" in report
    assert "## What was not read" in report
    assert ".env" in report
    assert "## What was not executed" in report
    assert "subprocesses" in report
    assert "BOT_TOKEN: 'must_hide'" not in report
    assert "[REDACTED: suspicious secret-like line]" in report


def _imports_from_source(source: str) -> set[str]:
    imports: set[str] = set()
    for line in source.splitlines():
        stripped = line.strip()
        if stripped.startswith("import "):
            imports.add(stripped.split()[1].split(".")[0])
        if stripped.startswith("from "):
            imports.add(stripped.split()[1].split(".")[0])
    return imports
