from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ActionDecision(str, Enum):
    SAFE = "SAFE"
    CONFIRM_REQUIRED = "CONFIRM_REQUIRED"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True)
class UserRequest:
    text: str
    channel: str = "local"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class PlannedAction:
    action_type: str
    description: str
    target: str = "local"
    requires_external_service: bool = False


@dataclass(frozen=True)
class HermesResponse:
    text: str
    decision: ActionDecision
    planned_actions: list[PlannedAction] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    next_step: str | None = None
