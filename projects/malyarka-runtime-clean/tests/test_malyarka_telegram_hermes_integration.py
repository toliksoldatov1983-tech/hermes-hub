from pathlib import Path

from malyarka_hermes import handle_user_text
from malyarka_hermes.safety import dangerous_response
from malyarka_telegram.handlers import handle_text_message


def test_help_routes_to_hermes() -> None:
    assert handle_text_message("!помощь") == handle_user_text("!помощь")


def test_next_step_routes_to_hermes() -> None:
    response = handle_text_message("!следующий шаг")

    assert "## 16. Следующий шаг" in response
    assert "clean runtime candidate" in response
    assert "проверить бота вручную в Telegram" in response
    assert "/opt/malyarka-telegram-bot" in response


def test_env_is_blocked_by_hermes() -> None:
    assert handle_text_message(".env") == dangerous_response()


def test_git_add_is_blocked_by_hermes() -> None:
    assert handle_text_message("git add .") == dangerous_response()


def test_bot_py_is_blocked_by_hermes() -> None:
    assert handle_text_message("bot.py") == dangerous_response()


def test_empty_text_routes_to_hermes() -> None:
    assert handle_text_message("") == handle_user_text("")


def test_regular_text_stays_on_legacy_order_logic() -> None:
    response = handle_text_message("regular text without command")

    assert response != handle_user_text("!помощь")
    assert "!статус" not in response
    assert "!следующий шаг" not in response
    assert "!помощь" not in response


def test_hermes_bot_file_is_not_created() -> None:
    assert not Path("hermes_bot.py").exists()
