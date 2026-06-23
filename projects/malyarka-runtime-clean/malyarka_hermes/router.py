"""Minimal read-only Hermes Router."""

from .commands import HELP_TEXT, normalize_command
from .memory import (
    extract_first_status_block,
    extract_markdown_section,
    read_current_state,
)
from .safety import dangerous_response, is_dangerous_text

EMPTY_MESSAGE_RESPONSE = "Пустое сообщение. Напишите !помощь для списка команд."
UNKNOWN_COMMAND_RESPONSE = (
    "Команда не распознана. Напиши !помощь, чтобы увидеть список доступных команд."
)
MEMORY_NOT_FOUND_RESPONSE = "Файл памяти не найден: MALYARKA_CURRENT_STATE.md"
NEXT_STEP_NOT_FOUND_RESPONSE = 'Раздел "Следующий шаг" не найден в файле памяти.'


class HermesRouter:
    def __init__(self, current_state_path: str | None = None):
        self.current_state_path = current_state_path

    def handle_user_text(self, text: str, user_id: int | str | None = None) -> str:
        del user_id

        if text is None or not text.strip():
            return EMPTY_MESSAGE_RESPONSE

        if is_dangerous_text(text):
            return dangerous_response()

        command = normalize_command(text)

        if command == "!помощь":
            return HELP_TEXT
        if command == "!следующий шаг":
            return self._handle_next_step()
        if command == "!статус":
            return self._handle_status()

        return UNKNOWN_COMMAND_RESPONSE

    def _read_state_or_error(self) -> tuple[str | None, str | None]:
        try:
            return read_current_state(self.current_state_path), None
        except FileNotFoundError:
            return None, MEMORY_NOT_FOUND_RESPONSE

    def _extract_next_step(self, state_text: str) -> str:
        next_step = extract_markdown_section(state_text, "## 16. Следующий шаг")
        if next_step:
            return next_step
        return extract_markdown_section(state_text, "## Следующий шаг")

    def _handle_next_step(self) -> str:
        state_text, error = self._read_state_or_error()
        if error is not None:
            return error

        next_step = self._extract_next_step(state_text or "")
        if not next_step:
            return NEXT_STEP_NOT_FOUND_RESPONSE
        return next_step

    def _handle_status(self) -> str:
        state_text, error = self._read_state_or_error()
        if error is not None:
            return error

        status_text = extract_first_status_block(state_text or "")
        if not status_text:
            status_text = "Статус не указан в файле памяти"

        next_step = self._extract_next_step(state_text or "")
        if not next_step:
            next_step = NEXT_STEP_NOT_FOUND_RESPONSE

        return "\n\n".join(
            [
                "Проект: Малярка",
                "Главный источник правды: MALYARKA_CURRENT_STATE.md",
                "Краткий статус:",
                status_text,
                "Следующий шаг:",
                next_step,
            ]
        )


def handle_user_text(text: str, user_id: int | str | None = None) -> str:
    return HermesRouter().handle_user_text(text, user_id=user_id)
