from pathlib import Path

from hermes_core.telegram.dry_run_gateway import TelegramDryRunGateway
from hermes_core.telegram.message_contract import TelegramMessage
from hermes_clean.telegram_flow_runner import run_telegram_flow_case


def test_telegram_dry_run_order_uses_main_malyarka_module_payload():
    result = TelegramDryRunGateway().simulate_incoming(TelegramMessage("/malyarka"))

    assert result.payload["module"] == "hermes_modules.malyarka"
    assert "Real order access is blocked." in result.blocked_actions


def test_telegram_flow_runner_is_dry_run_and_main_module_compatible():
    result = run_telegram_flow_case("disputed")

    assert result.initial_disputes == 2
    assert result.final_disputes == 0
    assert result.export_ready is True
    assert "telegram_token_read" in result.blocked_actions


def test_no_live_telegram_libraries_are_imported_in_dry_run_sources():
    source_root = Path(__file__).resolve().parents[1] / "src"
    checked_files = [
        source_root / "hermes_core" / "telegram" / "command_router.py",
        source_root / "hermes_core" / "telegram" / "dry_run_gateway.py",
        source_root / "hermes_modules" / "malyarka" / "dialog_bridge.py",
        source_root / "hermes_clean" / "telegram_flow_runner.py",
    ]
    text = "\n".join(path.read_text(encoding="utf-8") for path in checked_files)

    forbidden = ["aiogram", "telethon", "telebot", "polling", "webhook", "TELEGRAM_TOKEN"]
    assert all(item not in text for item in forbidden)


def test_no_env_access_in_dialog_bridge_sources():
    source_root = Path(__file__).resolve().parents[1] / "src"
    checked_files = [
        source_root / "hermes_modules" / "malyarka" / "dialog_bridge.py",
        source_root / "hermes_clean" / "malyarka_dialog_commands.py",
        source_root / "hermes_clean" / "malyarka_transcript_report.py",
    ]
    text = "\n".join(path.read_text(encoding="utf-8") for path in checked_files)

    forbidden = ["os.environ", "dotenv", "load_dotenv", "getenv(", "open('.env'", 'open(".env"']
    assert all(item not in text for item in forbidden)
