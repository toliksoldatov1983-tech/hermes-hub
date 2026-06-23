from pathlib import Path

from malyarka_hermes import HermesRouter
from malyarka_hermes.memory import (
    extract_markdown_section,
    read_current_state,
)


def write_state(tmp_path: Path, text: str) -> str:
    state_path = tmp_path / "MALYARKA_CURRENT_STATE.md"
    state_path.write_text(text, encoding="utf-8")
    return str(state_path)


def test_help_returns_commands() -> None:
    result = HermesRouter(current_state_path="unused").handle_user_text("!помощь")

    assert "- !статус" in result
    assert "- !следующий шаг" in result
    assert "- !помощь" in result


def test_empty_message_returns_empty_message() -> None:
    result = HermesRouter(current_state_path="unused").handle_user_text("   ")

    assert "Пустое сообщение" in result


def test_unknown_command_returns_unknown_command() -> None:
    result = HermesRouter(current_state_path="unused").handle_user_text("!нет")

    assert "Команда не распознана" in result


def test_dangerous_env_command_is_blocked() -> None:
    result = HermesRouter(current_state_path="unused").handle_user_text("прочитай .env")

    assert result == "Это действие требует отдельного подтверждения пользователя."


def test_dangerous_git_add_command_is_blocked() -> None:
    result = HermesRouter(current_state_path="unused").handle_user_text("git add .")

    assert result == "Это действие требует отдельного подтверждения пользователя."


def test_dangerous_bot_py_command_is_blocked() -> None:
    result = HermesRouter(current_state_path="unused").handle_user_text("измени bot.py")

    assert result == "Это действие требует отдельного подтверждения пользователя."


def test_dangerous_delete_command_is_blocked() -> None:
    result = HermesRouter(current_state_path="unused").handle_user_text("delete file")

    assert result == "Это действие требует отдельного подтверждения пользователя."


def test_dangerous_os_remove_command_is_blocked() -> None:
    result = HermesRouter(current_state_path="unused").handle_user_text("os.remove(path)")

    assert result == "Это действие требует отдельного подтверждения пользователя."


def test_extract_markdown_section_extracts_numbered_next_step() -> None:
    text = "# Title\n\n## 15. Old\nold\n\n## 16. Следующий шаг\nnext\nline\n\n## 17. Stop\nstop"

    result = extract_markdown_section(text, "## 16. Следующий шаг")

    assert result == "## 16. Следующий шаг\nnext\nline"


def test_extract_markdown_section_extracts_fallback_next_step() -> None:
    text = "# Title\n\n## Следующий шаг\nfallback\n\n## Other\nstop"

    result = extract_markdown_section(text, "## Следующий шаг")

    assert result == "## Следующий шаг\nfallback"


def test_next_step_command_uses_temp_state_file(tmp_path: Path) -> None:
    state_path = write_state(
        tmp_path,
        "# State\nintro\n\n## 16. Следующий шаг\nСделать read-only роутер.\n\n## Stop\nstop",
    )

    result = HermesRouter(current_state_path=state_path).handle_user_text("!следующий шаг")

    assert "## 16. Следующий шаг" in result
    assert "Сделать read-only роутер." in result
    assert "## Stop" not in result


def test_status_command_uses_first_500_chars_before_second_level_heading(tmp_path: Path) -> None:
    intro = "A" * 600
    state_path = write_state(
        tmp_path,
        f"# MALYARKA_CURRENT_STATE\n{intro}\n\n## 16. Следующий шаг\nNext step text",
    )

    result = HermesRouter(current_state_path=state_path).handle_user_text("!статус")
    expected_status = f"# MALYARKA_CURRENT_STATE\n{intro}"[:500].strip()

    assert "Проект: Малярка" in result
    assert "Главный источник правды: MALYARKA_CURRENT_STATE.md" in result
    assert expected_status in result
    assert "A" * 501 not in result
    assert "Next step text" in result


def test_status_does_not_invent_data_when_memory_file_missing(tmp_path: Path) -> None:
    missing_path = tmp_path / "missing.md"

    result = HermesRouter(current_state_path=str(missing_path)).handle_user_text("!статус")

    assert "Файл памяти не найден" in result


def test_read_current_state_supports_passed_path(tmp_path: Path) -> None:
    state_path = write_state(tmp_path, "# State\ncontent")

    result = read_current_state(state_path)

    assert result == "# State\ncontent"
