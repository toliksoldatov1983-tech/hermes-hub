from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class TelegramMessage:
    text: str
    chat_id: str = "dry-run"
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class TelegramDryRunResult:
    command: str
    planned_response: str
    blocked_actions: list[str]
    warnings: list[str]
    next_step: str
    payload: dict[str, str] = field(default_factory=dict)
