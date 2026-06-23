from datetime import datetime
from pathlib import Path

import pytest

from malyarka_telegram import handlers as telegram_handlers
from malyarka_telegram.app import build_live_text_response
from malyarka_telegram.config import TelegramConfig
from malyarka_telegram.obsidian_inbox import (
    INBOX_FILENAME,
    ObsidianInboxError,
    append_hermes_inbox_note,
    resolve_inbox_path,
)
from malyarka_telegram.session import InMemoryModeSessionStore


def test_append_hermes_inbox_note_creates_single_append_only_file(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    inbox = vault / INBOX_FILENAME

    result = append_hermes_inbox_note(
        "first note",
        user_id=42,
        inbox_path=inbox,
        vault_path=vault,
        now=datetime(2026, 5, 29, 18, 30, 0),
    )
    append_hermes_inbox_note(
        "second note",
        user_id=42,
        inbox_path=inbox,
        vault_path=vault,
        now=datetime(2026, 5, 29, 18, 31, 0),
    )

    assert result == inbox
    text = inbox.read_text(encoding="utf-8")
    assert text.count("# HERMES_INBOX") == 1
    assert "## 2026-05-29 18:30:00" in text
    assert "## 2026-05-29 18:31:00" in text
    assert "source: telegram-engineer" in text
    assert "user_id: 42" in text
    assert "first note" in text
    assert "second note" in text


def test_resolve_inbox_path_rejects_any_file_except_hermes_inbox(tmp_path: Path) -> None:
    vault = tmp_path / "vault"

    with pytest.raises(ObsidianInboxError):
        resolve_inbox_path(inbox_path=vault / "TASKS.md", vault_path=vault)


def test_resolve_inbox_path_rejects_paths_outside_vault(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    outside = tmp_path / "other" / INBOX_FILENAME

    with pytest.raises(ObsidianInboxError):
        resolve_inbox_path(inbox_path=outside, vault_path=vault)


def test_live_engineer_mode_can_save_task_card_to_obsidian_inbox(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    inbox = vault / INBOX_FILENAME
    store = InMemoryModeSessionStore()

    build_live_text_response(
        text="/инженер",
        user_id=7,
        session_store=store,
        config=TelegramConfig(owner_id=7),
        write_obsidian_inbox=True,
        obsidian_inbox_path=inbox,
    )
    response = build_live_text_response(
        text="запомнить идею про безопасный inbox",
        user_id=7,
        session_store=store,
        config=TelegramConfig(owner_id=7),
        write_obsidian_inbox=True,
        obsidian_inbox_path=inbox,
    )

    assert "Obsidian inbox: saved to HERMES_INBOX.md." in response.text
    text = inbox.read_text(encoding="utf-8")
    assert "ЗАДАЧА ДЛЯ HERMES" in text
    assert "запомнить идею про безопасный inbox" in text
