"""Phone Pairing Contract — safe device pairing for mobile access.

All pairing is dry-run/mock by default.
Real tokens require APPROVE_PHONE_PAIRING gate.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any


class PairingMode(Enum):
    """Pairing mode — how a device connects to Hermes-Clean."""

    NONE = "none"                       # No pairing — localhost only
    DRY_RUN = "dry-run"                 # Mock pairing for testing
    LAN = "lan"                         # Same Wi-Fi network
    TAILSCALE = "tailscale"             # Tailscale VPN mesh
    USB_REVERSE = "usb-reverse"         # USB reverse port forward (adb reverse)
    HTTPS_PROXY = "https-proxy"         # Future: reverse proxy with HTTPS


class ConnectionStatus(Enum):
    """Connection status for a paired device."""

    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    BLOCKED = "blocked"
    EXPIRED = "expired"


class ConnectivityTier(Enum):
    """Access tier for mobile devices."""

    LOCALHOST_ONLY = "localhost_only"     # Current: 127.0.0.1 only
    LAN_DISABLED = "lan_disabled"         # LAN blocked
    TAILSCALE_DISABLED = "tailscale_disabled"  # Tailscale blocked
    PAIRING_DRY_RUN = "pairing_dry_run"   # Mock pairing only
    EXTERNAL_BLOCKED = "external_blocked"  # Internet blocked


@dataclass
class DevicePairing:
    """Pairing contract for a mobile device.

    In dry-run mode, all fields are synthetic/mock.
    Real tokens require APPROVE_PHONE_PAIRING.
    """

    device_id: str = "dry-run-device-001"
    device_name: str = "Dry-Run Phone"
    pairing_mode: PairingMode = PairingMode.DRY_RUN
    connection_status: ConnectionStatus = ConnectionStatus.DISCONNECTED
    tier: ConnectivityTier = ConnectivityTier.LOCALHOST_ONLY
    api_base_url: str = "http://127.0.0.1:8514"
    allowed_actions: list[str] = field(default_factory=lambda: [
        "status", "dashboard", "daily-assistant", "daily-brief",
        "what-next", "local-health", "malyarka-status",
        "ai-provider-status", "secret-gate",
    ])
    blocked_actions: list[str] = field(default_factory=lambda: [
        "live-telegram", "google-drive-write", "external-api",
        "real-orders", "delete-operation", "archive-import",
        "direct-gemini", "direct-deepseek",
    ])
    expires_at: str = "never"
    approval_required: str = "APPROVE_PHONE_PAIRING"
    is_real: bool = False
    is_dry_run: bool = True
    audit_metadata: dict[str, Any] = field(default_factory=lambda: {
        "pairing_version": "1.0",
        "safe_local": True,
        "real_token": False,
        "real_device": False,
        "real_connection": False,
        "env_read": False,
        "network_called": False,
        "external_port_open": False,
    })

    def to_dict(self) -> dict[str, Any]:
        return {
            "device_id": self.device_id,
            "device_name": self.device_name,
            "pairing_mode": self.pairing_mode.value,
            "connection_status": self.connection_status.value,
            "tier": self.tier.value,
            "api_base_url": self.api_base_url,
            "allowed_actions": self.allowed_actions,
            "blocked_actions": self.blocked_actions,
            "expires_at": self.expires_at,
            "approval_required": self.approval_required,
            "is_real": self.is_real,
            "is_dry_run": self.is_dry_run,
            "audit_metadata": self.audit_metadata,
        }

    @staticmethod
    def dry_run() -> DevicePairing:
        """Create a dry-run pairing (safe-local, mock)."""
        return DevicePairing()

    @staticmethod
    def dry_run_pair(name: str, device_id: str) -> DevicePairing:
        return DevicePairing(
            device_id=device_id,
            device_name=name,
            pairing_mode=PairingMode.DRY_RUN,
        )
