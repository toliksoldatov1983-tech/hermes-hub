"""Runtime bridge contract — safe communication between old Hermes and Hermes-Clean.

All bridge communication is safe-local by default. Real/external actions are blocked.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any


class BridgeActionType(Enum):
    """Allowed and blocked bridge action types."""

    # ── Allowed in safe-local ──
    STATUS = auto()
    DASHBOARD = auto()
    DAILY_REPORT = auto()
    DAILY_ASSISTANT = auto()
    DAILY_BRIEF = auto()
    WHAT_NEXT = auto()
    LOCAL_HEALTH = auto()
    PROJECT_STATUS = auto()
    MALYARKA_STATUS = auto()
    MALYARKA_DIALOG = auto()
    MALYARKA_TRANSCRIPT = auto()
    MALYARKA_FIXTURES = auto()
    MALYARKA_COMBINED = auto()
    TELEGRAM_FLOW_DRY_RUN = auto()
    AI_PROVIDER_STATUS = auto()
    AI_PROVIDER_LIST = auto()
    SECRET_GATE_STATUS = auto()
    PROJECT_AUDIT = auto()
    SMOKE = auto()
    HELP_LOCAL = auto()
    MEMORY_SNAPSHOT = auto()

    # ── Blocked in safe-local ──
    LIVE_TELEGRAM = auto()
    POLLING_WEBHOOK = auto()
    EXTERNAL_API = auto()
    GOOGLE_DRIVE_WRITE = auto()
    REAL_ORDER_ACCESS = auto()
    ARCHIVE_IMPORT = auto()
    DELETE_OPERATION = auto()
    SECRET_READ = auto()
    DIRECT_GEMINI = auto()
    DIRECT_DEEPSEEK = auto()


# ── Allowed / Blocked sets ──

ALLOWED_SAFE_ACTIONS: frozenset[BridgeActionType] = frozenset({
    BridgeActionType.STATUS,
    BridgeActionType.DASHBOARD,
    BridgeActionType.DAILY_REPORT,
    BridgeActionType.DAILY_ASSISTANT,
    BridgeActionType.DAILY_BRIEF,
    BridgeActionType.WHAT_NEXT,
    BridgeActionType.LOCAL_HEALTH,
    BridgeActionType.PROJECT_STATUS,
    BridgeActionType.MALYARKA_STATUS,
    BridgeActionType.MALYARKA_DIALOG,
    BridgeActionType.MALYARKA_TRANSCRIPT,
    BridgeActionType.MALYARKA_FIXTURES,
    BridgeActionType.MALYARKA_COMBINED,
    BridgeActionType.TELEGRAM_FLOW_DRY_RUN,
    BridgeActionType.AI_PROVIDER_STATUS,
    BridgeActionType.AI_PROVIDER_LIST,
    BridgeActionType.SECRET_GATE_STATUS,
    BridgeActionType.PROJECT_AUDIT,
    BridgeActionType.SMOKE,
    BridgeActionType.HELP_LOCAL,
    BridgeActionType.MEMORY_SNAPSHOT,
})

BLOCKED_ACTIONS: frozenset[BridgeActionType] = frozenset({
    BridgeActionType.LIVE_TELEGRAM,
    BridgeActionType.POLLING_WEBHOOK,
    BridgeActionType.EXTERNAL_API,
    BridgeActionType.GOOGLE_DRIVE_WRITE,
    BridgeActionType.REAL_ORDER_ACCESS,
    BridgeActionType.ARCHIVE_IMPORT,
    BridgeActionType.DELETE_OPERATION,
    BridgeActionType.SECRET_READ,
    BridgeActionType.DIRECT_GEMINI,
    BridgeActionType.DIRECT_DEEPSEEK,
})


# ── Request / Response ──


@dataclass(frozen=True)
class BridgeRequest:
    """Incoming request from old Hermes shell."""

    action: BridgeActionType
    source: str = "archive"
    mode: str = "safe-local"
    payload: dict[str, Any] = field(default_factory=dict)
    context_budget_pct: int = 0

    @staticmethod
    def from_string(action_name: str, **payload: Any) -> BridgeRequest:
        """Parse a request from a string action name."""
        try:
            action = BridgeActionType[action_name.upper().replace("-", "_")]
        except KeyError:
            action = BridgeActionType.STATUS  # fallback
        return BridgeRequest(action=action, payload=payload)


@dataclass(frozen=True)
class BridgeResponse:
    """Response from Hermes-Clean back to old Hermes."""

    status: str  # "OK", "BLOCKED", "ERROR"
    action: str
    output_lines: list[str] = field(default_factory=list)
    route: str = ""
    blocked_reason: str = ""
    audit_metadata: dict[str, Any] = field(default_factory=lambda: {
        "bridge_version": "1.0",
        "safe_local": True,
        "real_api_called": False,
        "env_read": False,
        "token_used": False,
        "network_called": False,
    })
    context_budget_remaining_pct: int = 100

    @property
    def is_blocked(self) -> bool:
        return self.status == "BLOCKED"

    @property
    def is_ok(self) -> bool:
        return self.status == "OK"

    @property
    def output_text(self) -> str:
        return "\n".join(self.output_lines)

    @staticmethod
    def blocked_action(action_name: str, reason: str) -> BridgeResponse:
        return BridgeResponse(
            status="BLOCKED",
            action=action_name,
            blocked_reason=reason,
            output_lines=[f"BLOCKED: {reason}"],
        )

    @staticmethod
    def ok_action(action_name: str, output_lines: list[str], route: str = "") -> BridgeResponse:
        return BridgeResponse(
            status="OK",
            action=action_name,
            output_lines=output_lines,
            route=route,
        )

    @staticmethod
    def error_action(action_name: str, message: str) -> BridgeResponse:
        return BridgeResponse(
            status="ERROR",
            action=action_name,
            output_lines=[f"ERROR: {message}"],
            blocked_reason=message,
        )


# ── Action name mapping ──

ACTION_TO_ROUTE: dict[BridgeActionType, str] = {
    BridgeActionType.STATUS: "app-status",
    BridgeActionType.DASHBOARD: "dashboard",
    BridgeActionType.DAILY_REPORT: "daily-report",
    BridgeActionType.DAILY_ASSISTANT: "daily-assistant",
    BridgeActionType.DAILY_BRIEF: "daily-brief",
    BridgeActionType.WHAT_NEXT: "what-next",
    BridgeActionType.LOCAL_HEALTH: "local-health",
    BridgeActionType.PROJECT_STATUS: "project-status",
    BridgeActionType.MALYARKA_STATUS: "malyarka-status",
    BridgeActionType.MALYARKA_DIALOG: "malyarka-dialog",
    BridgeActionType.MALYARKA_TRANSCRIPT: "malyarka-transcript",
    BridgeActionType.MALYARKA_FIXTURES: "malyarka-fixtures",
    BridgeActionType.MALYARKA_COMBINED: "malyarka-combined",
    BridgeActionType.TELEGRAM_FLOW_DRY_RUN: "telegram-flow",
    BridgeActionType.AI_PROVIDER_STATUS: "ai-provider-status",
    BridgeActionType.AI_PROVIDER_LIST: "ai-provider-list",
    BridgeActionType.SECRET_GATE_STATUS: "secret-gate",
    BridgeActionType.PROJECT_AUDIT: "project-audit",
    BridgeActionType.SMOKE: "smoke",
    BridgeActionType.HELP_LOCAL: "help-local",
    BridgeActionType.MEMORY_SNAPSHOT: "memory",
}

ROUTE_TO_ACTION: dict[str, BridgeActionType] = {v: k for k, v in ACTION_TO_ROUTE.items()}
