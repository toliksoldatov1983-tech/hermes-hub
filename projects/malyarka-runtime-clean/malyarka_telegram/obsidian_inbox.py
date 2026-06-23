"""Safe append-only Obsidian inbox for Hermes notes."""

from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path


DEFAULT_VAULT_PATH = Path(
    os.environ.get(
        "MALYARKA_OBSIDIAN_VAULT_PATH",
        r"C:\Users\user\Documents\Codex\Malyarka_Obsidian_Vault",
    )
)
INBOX_FILENAME = "HERMES_INBOX.md"
MAX_NOTE_CHARS = 8000


class ObsidianInboxError(RuntimeError):
    """Raised when a Hermes note cannot be safely written to Obsidian."""


def append_hermes_inbox_note(
    text: str,
    *,
    user_id: int | str | None = None,
    inbox_path: str | Path | None = None,
    vault_path: str | Path | None = None,
    now: datetime | None = None,
) -> Path:
    """Append a Hermes note to the single allowed Obsidian inbox file."""

    note_text = _sanitize_note_text(text)
    target = resolve_inbox_path(inbox_path=inbox_path, vault_path=vault_path)
    target.parent.mkdir(parents=True, exist_ok=True)

    timestamp = (now or datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    header = ""
    if not target.exists() or target.stat().st_size == 0:
        header = "# HERMES_INBOX\n\nSafe append-only inbox for Hermes notes.\n\n"

    user_line = f"user_id: {user_id}" if user_id is not None else "user_id: unknown"
    block = "\n".join(
        [
            f"## {timestamp}",
            "source: telegram-engineer",
            user_line,
            "",
            "```text",
            note_text,
            "```",
            "",
        ]
    )
    with target.open("a", encoding="utf-8", newline="\n") as file:
        file.write(header)
        file.write(block)
    return target


def resolve_inbox_path(
    *,
    inbox_path: str | Path | None = None,
    vault_path: str | Path | None = None,
) -> Path:
    """Resolve and validate the only file Hermes is allowed to write."""

    vault = Path(vault_path) if vault_path is not None else DEFAULT_VAULT_PATH
    target = Path(inbox_path) if inbox_path is not None else vault / INBOX_FILENAME
    if vault_path is None and inbox_path is not None:
        vault = target.parent

    if target.name != INBOX_FILENAME:
        raise ObsidianInboxError("Hermes can write only to HERMES_INBOX.md")

    try:
        resolved_vault = vault.resolve(strict=False)
        resolved_target = target.resolve(strict=False)
        resolved_target.relative_to(resolved_vault)
    except ValueError as error:
        raise ObsidianInboxError("Hermes inbox must stay inside the Obsidian vault") from error

    return resolved_target


def _sanitize_note_text(text: str) -> str:
    note_text = str(text or "").strip()
    if not note_text:
        raise ObsidianInboxError("Hermes inbox note is empty")
    if len(note_text) > MAX_NOTE_CHARS:
        note_text = note_text[:MAX_NOTE_CHARS].rstrip() + "\n...[truncated]"
    return note_text.replace("```", "` ` `")
