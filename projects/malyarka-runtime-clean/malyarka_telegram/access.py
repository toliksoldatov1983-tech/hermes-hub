"""Owner access helpers for the private Telegram control layer."""

from __future__ import annotations


def parse_owner_id(value: str | int | None) -> int | None:
    """Parse an owner id from an environment value without exposing it."""

    if value is None:
        return None
    if isinstance(value, int):
        return value if value > 0 else None
    stripped = str(value).strip()
    if not stripped:
        return None
    try:
        owner_id = int(stripped)
    except ValueError:
        return None
    return owner_id if owner_id > 0 else None


def is_owner(user_id: int | str | None, owner_id: int | None) -> bool:
    """Return True only when owner_id is configured and matches user_id."""

    if owner_id is None or user_id is None:
        return False
    try:
        return int(user_id) == int(owner_id)
    except (TypeError, ValueError):
        return False


def is_owner_id_configured(owner_id: int | None) -> bool:
    """Return a safe boolean diagnostics flag without revealing the value."""

    return owner_id is not None
