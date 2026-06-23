from malyarka_telegram.access import is_owner, is_owner_id_configured, parse_owner_id
from malyarka_telegram.config import TelegramConfig


def test_parse_owner_id_accepts_positive_integer_text():
    assert parse_owner_id("12345") == 12345
    assert parse_owner_id(" 12345 ") == 12345


def test_parse_owner_id_rejects_empty_invalid_and_non_positive_values():
    assert parse_owner_id(None) is None
    assert parse_owner_id("") is None
    assert parse_owner_id("abc") is None
    assert parse_owner_id("0") is None
    assert parse_owner_id("-1") is None


def test_is_owner_requires_configured_matching_owner_id():
    assert is_owner(777, 777) is True
    assert is_owner("777", 777) is True
    assert is_owner(778, 777) is False
    assert is_owner(777, None) is False


def test_owner_diagnostics_is_boolean_only():
    assert is_owner_id_configured(777) is True
    assert is_owner_id_configured(None) is False


def test_telegram_config_reads_owner_id_from_environment_only(monkeypatch):
    monkeypatch.setenv("MALYARKA_TELEGRAM_OWNER_ID", "777")
    monkeypatch.delenv("MALYARKA_TELEGRAM_BOT_TOKEN", raising=False)

    config = TelegramConfig.from_environment()

    assert config.owner_id == 777
    assert config.bot_token is None


def test_telegram_config_does_not_read_legacy_bot_token(monkeypatch):
    monkeypatch.delenv("MALYARKA_TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.setenv("BOT_TOKEN", "legacy-token-must-not-be-read")

    config = TelegramConfig.from_environment()

    assert config.bot_token is None
