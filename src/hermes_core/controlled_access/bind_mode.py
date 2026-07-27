"""Bind Mode Configuration — safe bind addresses for Local API server.

Default: 127.0.0.1 only. All other modes disabled until approval.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class BindMode(Enum):
    """Bind modes for the local API server."""

    LOCALHOST = "127.0.0.1"          # ✅ Default, always allowed
    TAILSCALE = "tailscale-ip"        # 🚫 Disabled, needs APPROVE_TAILSCALE_MODE
    LAN = "lan-ip"                    # 🚫 Disabled, needs APPROVE_LAN_MODE
    PUBLIC = "public-ip"              # ❌ Permanently blocked
    ZERO = "0.0.0.0"                 # ❌ Permanently blocked


BIND_MODE_POLICY: dict[BindMode, dict] = {
    BindMode.LOCALHOST: {
        "enabled": True,
        "requires_approval": False,
        "approval_gate": "",
        "risk": "none",
        "description": "Только этот компьютер. Безопасно по умолчанию.",
    },
    BindMode.TAILSCALE: {
        "enabled": False,
        "requires_approval": True,
        "approval_gate": "APPROVE_TAILSCALE_MODE",
        "risk": "low",
        "description": "Доступ через Tailscale VPN. Сквозное шифрование.",
    },
    BindMode.LAN: {
        "enabled": False,
        "requires_approval": True,
        "approval_gate": "APPROVE_LAN_MODE",
        "risk": "medium",
        "description": "Доступ из локальной сети (192.168.x.x).",
    },
    BindMode.PUBLIC: {
        "enabled": False,
        "requires_approval": False,
        "approval_gate": "PERMANENTLY_BLOCKED",
        "risk": "extreme",
        "description": "Публичный доступ из интернета. PERMANENTLY BLOCKED.",
    },
    BindMode.ZERO: {
        "enabled": False,
        "requires_approval": False,
        "approval_gate": "PERMANENTLY_BLOCKED",
        "risk": "extreme",
        "description": "0.0.0.0 — слушать все интерфейсы. PERMANENTLY BLOCKED.",
    },
}


@dataclass
class BindConfig:
    """Current bind configuration."""

    mode: BindMode = BindMode.LOCALHOST
    host: str = "127.0.0.1"
    port: int = 8514
    safe_local: bool = True

    @property
    def bind_address(self) -> str:
        return f"{self.host}:{self.port}"

    @property
    def is_allowed(self) -> bool:
        return BIND_MODE_POLICY.get(self.mode, {}).get("enabled", False)

    @property
    def is_blocked(self) -> bool:
        return not self.is_allowed

    def to_dict(self) -> dict:
        return {
            "mode": self.mode.value,
            "host": self.host,
            "port": self.port,
            "bind_address": self.bind_address,
            "safe_local": self.safe_local,
            "is_allowed": self.is_allowed,
            "enabled": self.is_allowed,
            **BIND_MODE_POLICY.get(self.mode, {}),
        }


def get_bind_config() -> BindConfig:
    """Get the current bind configuration (always localhost)."""
    return BindConfig()


def classify_host(host: str) -> BindMode:
    """Classify a host string into a BindMode."""
    host = host.strip().lower()
    if host in ("127.0.0.1", "localhost", "::1"):
        return BindMode.LOCALHOST
    if host == "0.0.0.0":
        return BindMode.ZERO
    if host.startswith("192.168.") or host.startswith("10.") or host.startswith("172.16."):
        return BindMode.LAN
    if host.startswith("100.") and "." in host:
        # Tailscale uses 100.x.x.x
        return BindMode.TAILSCALE
    return BindMode.PUBLIC


TAILSCALE_RECOMMENDATION = """
Tailscale рекомендован как первый безопасный вариант доступа с телефона.

Преимущества:
  - Сквозное шифрование (WireGuard)
  - Не открывает порты на роутере
  - Работает из любой сети (Wi-Fi, мобильный интернет)
  - Бесплатно для личного использования (до 100 устройств)

Как включить (вручную, не автоматически):
  1. Установить Tailscale на ПК: https://tailscale.com/download
  2. Установить Tailscale на телефон (Google Play / App Store)
  3. Войти в тот же аккаунт на обоих устройствах
  4. Узнать Tailscale IP ПК (обычно 100.x.x.x)
  5. В Hermes-Clean: дать APPROVE_TAILSCALE_MODE
  6. Изменить API URL в Android Shell на Tailscale IP ПК

Hermes НЕ делает это автоматически. Все шаги — вручную пользователем.
"""
