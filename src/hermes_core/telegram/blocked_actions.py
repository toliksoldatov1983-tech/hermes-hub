"""Blocked actions list for Telegram dry-run mode.

Every action that is blocked in dry-run is defined here.
Used by command_router, scenarios, status_report, and smoke tests.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BlockedAction:
    id: str
    label: str
    category: str  # telegram / export / secrets / orders / external


# ── Full blocked actions registry ──

BLOCKED: tuple[BlockedAction, ...] = (
    # ── Telegram live ──
    BlockedAction("live_polling", "Live Telegram polling", "telegram"),
    BlockedAction("live_webhook", "Live Telegram webhook", "telegram"),
    BlockedAction("send_message", "Outbound Telegram messages", "telegram"),
    BlockedAction("token_read", "Telegram token reading", "secrets"),
    BlockedAction("live_bot_start", "Live bot start", "telegram"),

    # ── Secrets ──
    BlockedAction("env_read", ".env file reading", "secrets"),
    BlockedAction("key_access", "API key / token access", "secrets"),
    BlockedAction("secret_storage", "Secret storage in code/docs", "secrets"),

    # ── Orders ──
    BlockedAction("real_order_read", "Real order reading", "orders"),
    BlockedAction("real_order_modify", "Real order modification", "orders"),
    BlockedAction("client_data_access", "Client personal data access", "orders"),

    # ── Export ──
    BlockedAction("file_export", "Real file export (Excel, Corel)", "export"),
    BlockedAction("real_excel_create", "Real Excel file creation", "export"),
    BlockedAction("external_send", "Sending files externally", "export"),

    # ── External ──
    BlockedAction("external_api", "External API call", "external"),
    BlockedAction("google_drive_write", "Google Drive write", "external"),
    BlockedAction("google_drive_move", "Google Drive move without approval", "external"),
    BlockedAction("archives_access", "Old archive reading", "external"),
)


def blocked_summary() -> dict[str, int]:
    """Return count of blocked actions by category."""
    counts: dict[str, int] = {}
    for ba in BLOCKED:
        counts[ba.category] = counts.get(ba.category, 0) + 1
    return counts


def blocked_labels() -> list[str]:
    """Return all blocked action labels as strings."""
    return [ba.label for ba in BLOCKED]


def blocked_by_category(category: str) -> list[BlockedAction]:
    """Return all blocked actions for a category."""
    return [ba for ba in BLOCKED if ba.category == category]
