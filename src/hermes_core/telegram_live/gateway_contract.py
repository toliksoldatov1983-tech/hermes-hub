"""Telegram Live Gateway — readiness-only contract.

All modes disabled by default. No token reads. No API calls.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any


class TelegramLiveMode(Enum):
    DISABLED = "disabled"
    DRY_RUN_ONLY = "dry_run_only"
    READINESS_ONLY = "readiness_only"
    APPROVAL_REQUIRED = "approval_required"
    LIVE_POLLING_FUTURE = "live_polling_future"
    LIVE_WEBHOOK_FUTURE = "live_webhook_future"
    BLOCKED = "blocked"


@dataclass
class TelegramLiveGatewayConfig:
    """Configuration for live Telegram gateway. All disabled by default."""

    mode: TelegramLiveMode = TelegramLiveMode.READINESS_ONLY
    token_required: bool = True
    token_read_allowed: bool = False
    polling_allowed: bool = False
    webhook_allowed: bool = False
    send_message_allowed: bool = False
    receive_message_allowed: bool = False
    dry_run_allowed: bool = True
    approval_required: bool = True
    safe_local: bool = True
    blocked_reason: str = "Live Telegram is disabled. All actions require approval gates."
    audit_metadata: dict[str, Any] = field(default_factory=lambda: {
        "gateway_version": "1.0",
        "mode": "readiness_only",
        "token_read": False,
        "token_value_known": False,
        "env_read": False,
        "api_called": False,
        "polling_started": False,
        "webhook_started": False,
        "message_sent": False,
        "message_received": False,
        "network_called": False,
    })

    def to_dict(self) -> dict:
        return {
            "mode": self.mode.value,
            "token_read_allowed": self.token_read_allowed,
            "polling_allowed": self.polling_allowed,
            "webhook_allowed": self.webhook_allowed,
            "send_message_allowed": self.send_message_allowed,
            "receive_message_allowed": self.receive_message_allowed,
            "dry_run_allowed": self.dry_run_allowed,
            "approval_required": self.approval_required,
            "safe_local": self.safe_local,
            "blocked_reason": self.blocked_reason,
            "audit_metadata": self.audit_metadata,
        }


@dataclass
class TelegramApprovalGate:
    """An approval gate for live Telegram features."""

    gate_id: str
    title: str
    risk_level: str  # low, medium, high, critical
    default_state: str = "CLOSED"
    required_user_confirmation: bool = True
    allowed_actions_if_closed: list[str] = field(default_factory=list)
    blocked_actions_if_closed: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "gate_id": self.gate_id, "title": self.title,
            "risk_level": self.risk_level, "default_state": self.default_state,
            "required_user_confirmation": self.required_user_confirmation,
        }


APPROVAL_GATES: list[TelegramApprovalGate] = [
    TelegramApprovalGate(
        "APPROVE_TELEGRAM_TOKEN_READ", "Чтение Telegram токена",
        "high", blocked_actions_if_closed=["token_read", "live_telegram_start"],
    ),
    TelegramApprovalGate(
        "APPROVE_TELEGRAM_POLLING_START", "Запуск Telegram polling",
        "high", blocked_actions_if_closed=["polling_start", "live_receive"],
    ),
    TelegramApprovalGate(
        "APPROVE_TELEGRAM_WEBHOOK_START", "Запуск Telegram webhook",
        "critical", blocked_actions_if_closed=["webhook_start", "public_endpoint", "port_open"],
    ),
    TelegramApprovalGate(
        "APPROVE_TELEGRAM_SEND_MESSAGE", "Отправка сообщений в Telegram",
        "medium", blocked_actions_if_closed=["send_message", "live_response"],
    ),
    TelegramApprovalGate(
        "APPROVE_TELEGRAM_RECEIVE_MESSAGE", "Приём сообщений из Telegram",
        "high", blocked_actions_if_closed=["receive_message", "live_polling"],
    ),
    TelegramApprovalGate(
        "APPROVE_REAL_ORDER_EXPORT", "Создание реальных export-файлов",
        "medium", blocked_actions_if_closed=["real_export", "file_write"],
    ),
    TelegramApprovalGate(
        "APPROVE_PRODUCTION_DATABASE", "Production база данных",
        "critical", blocked_actions_if_closed=["db_write", "persistent_storage"],
    ),
    TelegramApprovalGate(
        "APPROVE_EXTERNAL_AI_PROVIDER", "Реальные AI-провайдеры (Gemini/DeepSeek)",
        "high", blocked_actions_if_closed=["external_api", "gemini", "deepseek"],
    ),
    TelegramApprovalGate(
        "APPROVE_GOOGLE_DRIVE_ACCESS", "Доступ к Google Drive",
        "high", blocked_actions_if_closed=["google_drive_write", "google_drive_read"],
    ),
    TelegramApprovalGate(
        "APPROVE_NETWORK_CHANGE", "Изменение сетевых настроек",
        "critical", blocked_actions_if_closed=["network_change", "firewall_change", "0.0.0.0_bind"],
    ),
]


class TelegramTokenPolicy:
    """Token policy — never reads token. Only describes rules."""

    TOKEN_VAR_NAME = "TELEGRAM_BOT_TOKEN"  # documentation only, never read

    @staticmethod
    def is_token_readable() -> bool:
        return False

    @staticmethod
    def policy_text() -> str:
        return """
Политика Telegram токена:

1. Токен НЕ читается в dry-run/readiness режиме.
2. Для чтения нужен APPROVE_TELEGRAM_TOKEN_READ.
3. Токен никогда не логируется.
4. Токен никогда не выводится.
5. Токен никогда не сохраняется в коде.
6. Имя переменной: TELEGRAM_BOT_TOKEN (документация only).
7. os.environ НЕ вызывается для реального токена.
8. В dry-run используется только fake session.
"""
