"""E2E Scenario Contract — end-to-end dry-run scenarios for Telegram bot UX."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any


class E2EStepStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    BLOCKED = "blocked"
    SKIPPED = "skipped"


@dataclass
class E2EStep:
    """One step in an E2E scenario."""
    user_message: str
    expected_intent: str = ""
    expected_mode: str = ""  # session mode after step
    expected_buttons: list[str] = field(default_factory=list)
    expected_blocked: bool = False
    expected_draft_status: str = ""  # draft status after step
    description: str = ""
    status: E2EStepStatus = E2EStepStatus.PENDING

    def to_dict(self) -> dict:
        return {
            "user_message": self.user_message[:80],
            "expected_intent": self.expected_intent,
            "expected_mode": self.expected_mode,
            "expected_blocked": self.expected_blocked,
            "expected_draft_status": self.expected_draft_status,
            "status": self.status.value,
        }


@dataclass
class E2EScenario:
    """An end-to-end dry-run scenario."""

    scenario_id: str
    title: str
    description: str = ""
    steps: list[E2EStep] = field(default_factory=list)
    expected_final_state: str = ""  # summary of expected outcome
    safe_local: bool = True
    audit_metadata: dict[str, Any] = field(default_factory=lambda: {
        "real_telegram": False,
        "token_used": False,
        "network_called": False,
        "real_export": False,
        "env_read": False,
    })

    def to_dict(self) -> dict:
        return {
            "scenario_id": self.scenario_id,
            "title": self.title,
            "description": self.description,
            "steps_count": len(self.steps),
            "expected_final_state": self.expected_final_state,
            "safe_local": self.safe_local,
        }


@dataclass
class E2EResult:
    """Result of running an E2E scenario."""

    scenario_id: str
    passed: bool = False
    total_steps: int = 0
    passed_steps: int = 0
    failed_steps: int = 0
    blocked_steps: int = 0
    transcript: list[str] = field(default_factory=list)
    final_mode: str = ""
    final_draft_status: str = ""
    final_buttons: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def summary(self) -> str:
        status = "PASS" if self.passed else "FAIL"
        return f"[{status}] {self.scenario_id}: {self.passed_steps}/{self.total_steps} steps"
