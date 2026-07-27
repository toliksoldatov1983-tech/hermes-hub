"""Controlled Access Policy — enforces safe bind and client access rules.

All real external access blocked by default.
Tailscale/LAN require explicit approval gates.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any

from hermes_core.controlled_access.bind_mode import BindMode, classify_host, BIND_MODE_POLICY


class AccessDecision(Enum):
    ALLOWED = "allowed"
    BLOCKED = "blocked"
    PENDING_APPROVAL = "pending_approval"
    PERMANENTLY_BLOCKED = "permanently_blocked"


class ClientType(Enum):
    LOCALHOST = "localhost"
    PHONE_LAN = "phone_lan"
    PHONE_TAILSCALE = "phone_tailscale"
    PHONE_USB = "phone_usb"
    PUBLIC = "public"
    UNKNOWN = "unknown"


@dataclass
class AccessRequest:
    """An access request from a client."""

    client_host: str = "127.0.0.1"
    client_type: ClientType = ClientType.LOCALHOST
    device_id: str = ""
    pairing_status: str = "none"  # none, dry-run, approved
    requested_actions: list[str] = field(default_factory=lambda: ["status"])
    approval_approved: bool = False


@dataclass
class AccessDecisionResult:
    """Result of an access policy check."""

    decision: AccessDecision
    bind_mode: BindMode
    reason: str
    allowed_actions: list[str]
    blocked_actions: list[str]
    requires_approval: bool
    approval_gate: str
    audit: dict[str, Any] = field(default_factory=lambda: {
        "safe_local": True,
        "env_read": False,
        "network_called": False,
        "firewall_changed": False,
    })


class AccessPolicy:
    """Central access policy for controlled phone access.

    Enforces:
      - localhost: always allowed
      - Tailscale: blocked until APPROVE_TAILSCALE_MODE
      - LAN: blocked until APPROVE_LAN_MODE
      - Public/0.0.0.0: permanently blocked
    """

    # Hard-blocked actions — never allowed from any remote source
    HARD_BLOCKED_ACTIONS = frozenset({
        "secret-read", ".env-read", "token-read",
        "live-telegram", "google-drive-write", "external-api",
        "real-orders", "delete-operation", "archive-import",
        "direct-gemini", "direct-deepseek",
    })

    # Safe actions allowed from remote (after approval)
    SAFE_REMOTE_ACTIONS = frozenset({
        "status", "dashboard", "daily-report", "daily-assistant",
        "daily-brief", "what-next", "local-health", "project-status",
        "malyarka-status", "malyarka-dialog", "malyarka-fixtures",
        "ai-provider-status", "ai-provider-list", "secret-gate",
        "project-audit", "smoke", "help-local", "memory",
    })

    def check(self, request: AccessRequest) -> AccessDecisionResult:
        """Check an access request against the policy."""
        bind_mode = classify_host(request.client_host)

        # Permanently blocked
        if bind_mode in (BindMode.ZERO, BindMode.PUBLIC):
            return AccessDecisionResult(
                decision=AccessDecision.PERMANENTLY_BLOCKED,
                bind_mode=bind_mode,
                reason=f"Bind to {bind_mode.value} is permanently blocked.",
                allowed_actions=[],
                blocked_actions=request.requested_actions,
                requires_approval=False,
                approval_gate="PERMANENTLY_BLOCKED",
            )

        # Localhost — always allowed
        if bind_mode == BindMode.LOCALHOST:
            safe = [a for a in request.requested_actions if a not in self.HARD_BLOCKED_ACTIONS]
            blocked = [a for a in request.requested_actions if a in self.HARD_BLOCKED_ACTIONS]
            return AccessDecisionResult(
                decision=AccessDecision.ALLOWED,
                bind_mode=bind_mode,
                reason="Localhost access — always allowed.",
                allowed_actions=safe,
                blocked_actions=blocked,
                requires_approval=False,
                approval_gate="",
            )

        # Tailscale — needs approval
        if bind_mode == BindMode.TAILSCALE:
            if request.approval_approved:
                safe = [a for a in request.requested_actions if a in self.SAFE_REMOTE_ACTIONS]
                blocked = [a for a in request.requested_actions if a not in self.SAFE_REMOTE_ACTIONS]
                return AccessDecisionResult(
                    decision=AccessDecision.ALLOWED,
                    bind_mode=bind_mode,
                    reason="Tailscale access approved.",
                    allowed_actions=safe,
                    blocked_actions=blocked,
                    requires_approval=False,
                    approval_gate="APPROVE_TAILSCALE_MODE",
                )
            return AccessDecisionResult(
                decision=AccessDecision.PENDING_APPROVAL,
                bind_mode=bind_mode,
                reason="Tailscale access requires APPROVE_TAILSCALE_MODE and APPROVE_PHONE_PAIRING.",
                allowed_actions=[],
                blocked_actions=request.requested_actions,
                requires_approval=True,
                approval_gate="APPROVE_TAILSCALE_MODE",
            )

        # LAN — needs approval
        if bind_mode == BindMode.LAN:
            return AccessDecisionResult(
                decision=AccessDecision.PENDING_APPROVAL,
                bind_mode=bind_mode,
                reason="LAN access requires APPROVE_LAN_MODE and APPROVE_PHONE_PAIRING.",
                allowed_actions=[],
                blocked_actions=request.requested_actions,
                requires_approval=True,
                approval_gate="APPROVE_LAN_MODE",
            )

        # Unknown — blocked
        return AccessDecisionResult(
            decision=AccessDecision.BLOCKED,
            bind_mode=bind_mode,
            reason=f"Unknown client type: {request.client_type.value}",
            allowed_actions=[],
            blocked_actions=request.requested_actions,
            requires_approval=False,
            approval_gate="",
        )

    def status_report(self) -> dict[str, Any]:
        """Generate a full status report."""
        return {
            "tailscale_recommended": True,
            "tailscale_enabled": False,
            "lan_enabled": False,
            "public_blocked": True,
            "zero_blocked": True,
            "localhost_enabled": True,
            "pairing_real": False,
            "pairing_dry_run": True,
            "hard_blocked_actions": sorted(self.HARD_BLOCKED_ACTIONS),
            "safe_remote_actions": sorted(self.SAFE_REMOTE_ACTIONS),
            "next_step": (
                "Установите Tailscale, получите APPROVE_TAILSCALE_MODE "
                "и APPROVE_PHONE_PAIRING для доступа с телефона."
            ),
        }


_default_policy = AccessPolicy()


def get_access_policy() -> AccessPolicy:
    return _default_policy
