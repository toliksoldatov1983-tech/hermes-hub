"""Telegram mode constants for the safe router state machine."""

from __future__ import annotations

from enum import StrEnum


class TelegramMode(StrEnum):
    NEUTRAL = "neutral"
    ORDER = "order"
    CHAT = "chat"
    ENGINEER = "engineer"
    IDEAS = "ideas"
    ADMIN = "admin"
    SUMMARY = "summary"
    RULES = "rules"


MODE_COMMANDS: dict[str, TelegramMode] = {
    "/заказ": TelegramMode.ORDER,
    "заказ": TelegramMode.ORDER,
    "новый заказ": TelegramMode.ORDER,
    "🧾 новый заказ": TelegramMode.ORDER,
    "/чат": TelegramMode.CHAT,
    "чат": TelegramMode.CHAT,
    "/инженер": TelegramMode.ENGINEER,
    "инженер": TelegramMode.ENGINEER,
    "инженер проекта": TelegramMode.ENGINEER,
    "🛠 инженер": TelegramMode.ENGINEER,
    "🛠 инженер проекта": TelegramMode.ENGINEER,
    "/идеи": TelegramMode.IDEAS,
    "идеи": TelegramMode.IDEAS,
    "идеи / разговор": TelegramMode.IDEAS,
    "💬 идеи / разговор": TelegramMode.IDEAS,
    "/админ": TelegramMode.ADMIN,
    "/выжимка": TelegramMode.SUMMARY,
    "/правила": TelegramMode.RULES,
}

MODE_LABELS: dict[TelegramMode, str] = {
    TelegramMode.NEUTRAL: "нейтральный режим",
    TelegramMode.ORDER: "режим заказа",
    TelegramMode.CHAT: "режим чата",
    TelegramMode.ENGINEER: "инженерный режим",
    TelegramMode.IDEAS: "режим идей",
    TelegramMode.ADMIN: "админ-режим",
    TelegramMode.SUMMARY: "режим выжимки",
    TelegramMode.RULES: "режим правил",
}


def mode_from_command(command: str | None) -> TelegramMode | None:
    """Return a mode for a Telegram command, or None for non-mode commands."""

    if not command:
        return None
    normalized = " ".join(str(command).strip().lower().split())
    if normalized in MODE_COMMANDS:
        return MODE_COMMANDS[normalized]
    first_token = normalized.split(maxsplit=1)[0] if normalized else ""
    return MODE_COMMANDS.get(first_token)


def is_mode_command(text: str | None) -> bool:
    """Return whether text starts with a known mode command."""

    return mode_from_command(text) is not None


def get_mode_label(mode: TelegramMode | str | None) -> str:
    """Return a safe user-facing label for a known mode."""

    try:
        normalized_mode = TelegramMode(mode) if mode is not None else TelegramMode.NEUTRAL
    except ValueError:
        normalized_mode = TelegramMode.NEUTRAL
    return MODE_LABELS[normalized_mode]
