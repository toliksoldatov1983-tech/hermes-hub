from pathlib import Path

import pytest

from malyarka_telegram import handlers as telegram_handlers


def test_engineer_task_card_is_kept_when_obsidian_inbox_is_unavailable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def raise_permission_error(*args: object, **kwargs: object) -> Path:
        raise PermissionError("permission denied")

    monkeypatch.setattr(telegram_handlers, "append_hermes_inbox_note", raise_permission_error)

    response_text = telegram_handlers._append_engineer_task_to_obsidian(
        "TASK CARD",
        user_id=7,
        obsidian_inbox_path=None,
    )

    assert response_text.startswith("TASK CARD")
    assert "Obsidian inbox: not saved (permission denied)." in response_text
