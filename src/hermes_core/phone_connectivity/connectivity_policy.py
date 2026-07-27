"""Phone Connectivity Policy — safe modes for mobile phone access to Hermes-Clean.

All modes default to safe-local. Real access requires approval gates.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any


class ConnectivityMode(Enum):
    """Allowed connectivity modes for phone access."""

    LOCALHOST_ONLY = "localhost_only"          # 127.0.0.1 — current, safe
    LAN_DISABLED = "lan_disabled"              # Same Wi-Fi — blocked
    TAILSCALE_DISABLED = "tailscale_disabled"  # VPN — blocked
    USB_REVERSE_DISABLED = "usb_reverse_disabled"  # ADB reverse — blocked
    EXTERNAL_BLOCKED = "external_blocked"      # Public internet — hard blocked


@dataclass
class ConnectivityOption:
    """Description of a connectivity option."""

    name: str
    mode: ConnectivityMode
    enabled: bool
    description: str
    pros: list[str]
    risks: list[str]
    requirements: list[str]
    approval_gates: list[str]
    forbidden: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name, "mode": self.mode.value,
            "enabled": self.enabled, "description": self.description,
            "pros": self.pros, "risks": self.risks,
            "requirements": self.requirements,
            "approval_gates": self.approval_gates,
            "forbidden": self.forbidden,
        }


# ── Pre-defined options ──

CONNECTIVITY_OPTIONS: list[ConnectivityOption] = [
    ConnectivityOption(
        name="Localhost Only (текущий)",
        mode=ConnectivityMode.LOCALHOST_ONLY,
        enabled=True,
        description="Сервер слушает только 127.0.0.1. Доступ только с этого ПК.",
        pros=["Максимальная безопасность", "Нет сетевых рисков", "Работает без настроек"],
        risks=["Недоступно с телефона"],
        requirements=["Никаких"],
        approval_gates=["Не требуется"],
        forbidden=["Внешний доступ невозможен"],
    ),
    ConnectivityOption(
        name="Same Wi-Fi / LAN",
        mode=ConnectivityMode.LAN_DISABLED,
        enabled=False,
        description="Сервер слушает LAN IP (192.168.x.x). Доступ из домашней сети.",
        pros=["Простая настройка", "Без VPN"],
        risks=["Открывает порт в локальной сети", "Другие устройства в сети могут сканировать"],
        requirements=["APPROVE_LAN_MODE", "Статический IP или hostname"],
        approval_gates=["APPROVE_LAN_MODE", "APPROVE_PHONE_PAIRING"],
        forbidden=["0.0.0.0 запрещён", "Публичный IP запрещён", "Без pairing запрещён"],
    ),
    ConnectivityOption(
        name="Tailscale / VPN",
        mode=ConnectivityMode.TAILSCALE_DISABLED,
        enabled=False,
        description="Доступ через Tailscale mesh VPN. Безопасное шифрованное соединение.",
        pros=["Сквозное шифрование", "Не открывает порты на роутере", "Работает из любой сети"],
        risks=["Требует установки Tailscale на ПК и телефон"],
        requirements=["Tailscale установлен", "APPROVE_TAILSCALE_MODE"],
        approval_gates=["APPROVE_TAILSCALE_MODE", "APPROVE_PHONE_PAIRING"],
        forbidden=["Без pairing запрещён"],
    ),
    ConnectivityOption(
        name="USB Reverse Port Forward",
        mode=ConnectivityMode.USB_REVERSE_DISABLED,
        enabled=False,
        description="adb reverse tcp:8514 tcp:8514 — проброс порта через USB.",
        pros=["Физическое подключение", "Нет сетевых рисков"],
        risks=["Только для разработчиков", "Требует USB-отладку"],
        requirements=["Android SDK", "USB-отладка включена", "USB-кабель"],
        approval_gates=["APPROVE_USB_DEBUG_MODE"],
        forbidden=["Только для dev-тестирования"],
    ),
    ConnectivityOption(
        name="Публичный интернет",
        mode=ConnectivityMode.EXTERNAL_BLOCKED,
        enabled=False,
        description="Прямой доступ из интернета. PERMANENTLY BLOCKED.",
        pros=["Доступ отовсюду"],
        risks=["Экстремальный риск безопасности", "DDoS", "Сканирование портов", "Несанкционированный доступ"],
        requirements=["НИКОГДА не включать"],
        approval_gates=["PERMANENTLY BLOCKED"],
        forbidden=["ВСЁ запрещено"],
    ),
]


class PhoneConnectivityPolicy:
    """Security policy for phone connectivity.

    Enforces safe-local defaults. Blocks all real external access.
    """

    def __init__(self) -> None:
        self._current_mode = ConnectivityMode.LOCALHOST_ONLY
        self._options = {o.mode: o for o in CONNECTIVITY_OPTIONS}

    @property
    def current_mode(self) -> ConnectivityMode:
        return self._current_mode

    @property
    def is_localhost_only(self) -> bool:
        return self._current_mode == ConnectivityMode.LOCALHOST_ONLY

    @property
    def is_lan_enabled(self) -> bool:
        return self._current_mode == ConnectivityMode.LAN_DISABLED

    @property
    def is_external_blocked(self) -> bool:
        return True  # Hard blocked — never changes

    def get_option(self, mode: ConnectivityMode) -> ConnectivityOption | None:
        return self._options.get(mode)

    def list_options(self) -> list[ConnectivityOption]:
        return list(CONNECTIVITY_OPTIONS)

    def list_enabled(self) -> list[ConnectivityOption]:
        return [o for o in CONNECTIVITY_OPTIONS if o.enabled]

    def list_disabled(self) -> list[ConnectivityOption]:
        return [o for o in CONNECTIVITY_OPTIONS if not o.enabled]

    def can_bind_to(self, host: str) -> tuple[bool, str]:
        """Check if binding to a given host is allowed."""
        host = host.strip()
        if host in ("127.0.0.1", "localhost"):
            return True, "OK — localhost is always allowed."
        if host == "0.0.0.0":
            return False, "BLOCKED — 0.0.0.0 is permanently blocked."
        if host.startswith("192.168.") or host.startswith("10.") or host.startswith("172."):
            return False, "BLOCKED — LAN mode requires APPROVE_LAN_MODE and APPROVE_PHONE_PAIRING."
        return False, "BLOCKED — external/public addresses are permanently blocked."

    def status_report(self) -> dict[str, Any]:
        """Generate a status report."""
        return {
            "current_mode": self._current_mode.value,
            "localhost_only": self.is_localhost_only,
            "lan_enabled": self.is_lan_enabled,
            "external_blocked": self.is_external_blocked,
            "pairing_real_enabled": False,
            "pairing_dry_run_allowed": True,
            "total_options": len(CONNECTIVITY_OPTIONS),
            "enabled_options": len(self.list_enabled()),
            "disabled_options": len(self.list_disabled()),
            "next_step": (
                "Для подключения телефона: "
                "1) APPROVE_LAN_MODE или APPROVE_TAILSCALE_MODE, "
                "2) APPROVE_PHONE_PAIRING, "
                "3) Изменить API URL на IP ПК."
            ),
        }


# Singleton
_default_policy = PhoneConnectivityPolicy()


def get_default_policy() -> PhoneConnectivityPolicy:
    return _default_policy
