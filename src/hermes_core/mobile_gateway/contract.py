"""Mobile API contract — standardized JSON response format.

All mobile API responses follow this contract.
Safe-local only. No secrets, no network.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class MobileAPIEndpoint(Enum):
    """Mobile API endpoints."""

    # ── Allowed ──
    STATUS = "GET /api/status"
    DASHBOARD = "GET /api/dashboard"
    DAILY_REPORT = "GET /api/daily-report"
    DAILY_ASSISTANT = "GET /api/daily-assistant"
    WHAT_NEXT = "GET /api/what-next"
    LOCAL_HEALTH = "GET /api/local-health"
    MALYARKA_STATUS = "GET /api/malyarka/status"
    MALYARKA_DIALOG = "POST /api/malyarka/dialog"
    AI_PROVIDER_STATUS = "GET /api/ai-provider/status"
    BRIDGE_STATUS = "GET /api/bridge/status"
    BRIDGE_ROUTE = "POST /api/bridge/route"

    # ── Blocked (no API path — permanently blocked) ──
    LIVE_TELEGRAM = "BLOCKED:live-telegram"
    GOOGLE_DRIVE = "BLOCKED:google-drive"
    EXTERNAL_API = "BLOCKED:external-api"
    SECRET_READ = "BLOCKED:secret-read"
    REAL_ORDERS = "BLOCKED:real-orders"
    ARCHIVE_IMPORT = "BLOCKED:archive-import"
    DELETE_OPERATION = "BLOCKED:delete-operation"
    DIRECT_GEMINI = "BLOCKED:direct-gemini"
    DIRECT_DEEPSEEK = "BLOCKED:direct-deepseek"


# ── Allowed / Blocked ──

ALLOWED_ENDPOINTS: frozenset[MobileAPIEndpoint] = frozenset({
    MobileAPIEndpoint.STATUS,
    MobileAPIEndpoint.DASHBOARD,
    MobileAPIEndpoint.DAILY_REPORT,
    MobileAPIEndpoint.DAILY_ASSISTANT,
    MobileAPIEndpoint.WHAT_NEXT,
    MobileAPIEndpoint.LOCAL_HEALTH,
    MobileAPIEndpoint.MALYARKA_STATUS,
    MobileAPIEndpoint.MALYARKA_DIALOG,
    MobileAPIEndpoint.AI_PROVIDER_STATUS,
    MobileAPIEndpoint.BRIDGE_STATUS,
    MobileAPIEndpoint.BRIDGE_ROUTE,
})

BLOCKED_ENDPOINTS: frozenset[MobileAPIEndpoint] = frozenset({
    MobileAPIEndpoint.LIVE_TELEGRAM,
    MobileAPIEndpoint.GOOGLE_DRIVE,
    MobileAPIEndpoint.EXTERNAL_API,
    MobileAPIEndpoint.SECRET_READ,
    MobileAPIEndpoint.REAL_ORDERS,
    MobileAPIEndpoint.ARCHIVE_IMPORT,
    MobileAPIEndpoint.DELETE_OPERATION,
    MobileAPIEndpoint.DIRECT_GEMINI,
    MobileAPIEndpoint.DIRECT_DEEPSEEK,
})


# ── Standard response ──


@dataclass
class MobileAPIResponse:
    """Standard JSON response for all mobile API endpoints.

    Every response contains safety metadata.
    """

    status: str = "OK"           # OK / BLOCKED / ERROR
    safe_local: bool = True
    endpoint: str = ""
    action: str = ""
    data: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    blocked_reason: str = ""
    next_step: str = ""
    audit_metadata: dict[str, Any] = field(default_factory=lambda: {
        "mobile_gateway_version": "1.0",
        "safe_local": True,
        "bind_address": "127.0.0.1",
        "real_api_called": False,
        "env_read": False,
        "token_used": False,
        "network_called": False,
        "external_port_open": False,
    })

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "safe_local": self.safe_local,
            "endpoint": self.endpoint,
            "action": self.action,
            "data": self.data,
            "warnings": self.warnings,
            "blocked_reason": self.blocked_reason,
            "next_step": self.next_step,
            "audit_metadata": self.audit_metadata,
        }

    @staticmethod
    def ok(endpoint: str, action: str, data: dict, next_step: str = "") -> MobileAPIResponse:
        return MobileAPIResponse(
            status="OK",
            endpoint=endpoint,
            action=action,
            data=data,
            next_step=next_step or "Run 'mobile-gateway-status' for full overview.",
        )

    @staticmethod
    def blocked(endpoint: str, action: str, reason: str) -> MobileAPIResponse:
        return MobileAPIResponse(
            status="BLOCKED",
            endpoint=endpoint,
            action=action,
            blocked_reason=reason,
            warnings=[reason],
            next_step="This action requires APPROVE_SECRET_SETUP or is permanently blocked.",
        )

    @staticmethod
    def error(endpoint: str, action: str, message: str) -> MobileAPIResponse:
        return MobileAPIResponse(
            status="ERROR",
            endpoint=endpoint,
            action=action,
            blocked_reason=message,
            warnings=[message],
        )
