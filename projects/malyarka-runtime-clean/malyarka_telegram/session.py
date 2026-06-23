"""In-memory Telegram mode session store."""

from __future__ import annotations

from malyarka_telegram.modes import TelegramMode


class InMemoryModeSessionStore:
    """Store only user_id -> current_mode for the current process."""

    def __init__(self) -> None:
        self._modes: dict[int, TelegramMode] = {}

    def get_mode(self, user_id: int) -> TelegramMode:
        return self._modes.get(int(user_id), TelegramMode.NEUTRAL)

    def set_mode(self, user_id: int, mode: TelegramMode | str) -> TelegramMode:
        normalized_mode = TelegramMode(mode)
        self._modes[int(user_id)] = normalized_mode
        return normalized_mode

    def reset_mode(self, user_id: int) -> TelegramMode:
        self._modes.pop(int(user_id), None)
        return TelegramMode.NEUTRAL
