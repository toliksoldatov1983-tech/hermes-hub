"""System Hardening — safety layers for future Telegram live.

All policies are dry-run only. No real API. No token reads.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from datetime import datetime
from hashlib import sha256


# ── Message Safety ──


@dataclass
class MessageSafetyResult:
    allowed: bool = True
    blocked_reason: str = ""
    risk_level: str = "low"
    requires_approval: bool = False
    safe_response_hint: str = ""
    audit_metadata: dict[str, Any] = field(default_factory=lambda: {
        "safe_local": True, "env_read": False, "token_checked": False,
    })

    def to_dict(self) -> dict:
        return {"allowed": self.allowed, "blocked_reason": self.blocked_reason,
                "risk_level": self.risk_level, "requires_approval": self.requires_approval}


BLOCKED_MESSAGE_PATTERNS = [
    (["token", "api_key", ".env", "secret"], "secret_request", "critical", "Секреты недоступны в safe mode."),
    (["delete", "удал", "remove file"], "delete_request", "high", "Удаление файлов заблокировано."),
    (["live", "включи polling", "включи вебхук", "start bot"], "live_enable", "critical",
     "Live-функции требуют явного APPROVE."),
    (["export", "экспорт", "save order", "сохрани заказ"], "export_request", "medium",
     "Реальный export заблокирован. Используйте preview."),
    (["сеть", "network", "firewall", "порт", "0.0.0.0"], "network_change", "critical",
     "Сетевые изменения заблокированы."),
    (["gemini", "deepseek", "gpt", "openai"], "external_ai", "high", "Внешние AI отключены. Используется mock."),
    (["google drive", "гугл диск", "drive"], "drive_request", "high", "Google Drive заблокирован."),
]


def check_message_safety(text: str) -> MessageSafetyResult:
    """Check a message for safety issues."""
    lowered = text.lower()
    for patterns, req_type, risk, hint in BLOCKED_MESSAGE_PATTERNS:
        if any(p in lowered for p in patterns):
            return MessageSafetyResult(
                allowed=False, blocked_reason=f"{req_type} blocked: {hint}",
                risk_level=risk, requires_approval=True, safe_response_hint=hint,
            )
    return MessageSafetyResult()


# ── Duplicate Protection ──


@dataclass
class UpdateFingerprint:
    update_id: str = ""
    chat_id: str = ""
    text_hash: str = ""
    timestamp: str = ""

    @staticmethod
    def from_text(text: str, update_id: str = "", chat_id: str = "") -> UpdateFingerprint:
        return UpdateFingerprint(
            update_id=update_id, chat_id=chat_id,
            text_hash=sha256(text.encode()).hexdigest()[:16],
            timestamp=datetime.utcnow().isoformat(),
        )


class DuplicateProtection:
    """In-memory duplicate update protection. No persistent DB."""

    def __init__(self) -> None:
        self._processed: set[str] = set()
        self._max_entries = 1000

    def is_duplicate(self, fingerprint: UpdateFingerprint) -> bool:
        key = f"{fingerprint.update_id}:{fingerprint.text_hash}"
        if key in self._processed:
            return True
        self._processed.add(key)
        if len(self._processed) > self._max_entries:
            self._processed.clear()  # Rotate — in-memory only
        return False

    def clear(self) -> None:
        self._processed.clear()


# ── Rate Limit ──


@dataclass
class RateLimitPolicy:
    max_per_minute: int = 10
    max_order_parse_per_minute: int = 5
    max_dangerous_per_session: int = 3
    max_send_per_minute: int = 5
    max_unknown_chat: int = 0  # blocked entirely

    def is_allowed(self, count: int, limit: int) -> tuple[bool, str]:
        if count > limit:
            return False, f"Rate limit exceeded: {count}/{limit}"
        return True, ""


# ── Idempotency ──


IDEMPOTENCY_RULES = {
    "create_draft": "Повторный create не создаёт второй draft для того же текста.",
    "correct_draft": "Повторный correct к уже исправленной строке безопасен.",
    "confirm_draft": "Повторный confirm не создаёт повторный export.",
    "cancel_draft": "Повторный cancel безопасен.",
    "show_status": "Повторный show_status безопасен.",
    "fake_send": "Повторный send не отправляет реальное сообщение.",
}


def check_idempotency(action: str, already_done: bool) -> tuple[bool, str]:
    if not already_done:
        return True, "ok"
    return True, f"Idempotent: {IDEMPOTENCY_RULES.get(action, 'safe repeat')}"


# ── Safe Shutdown ──


SAFE_SHUTDOWN_PLAN = """
Safe Shutdown Plan (dry-run):

1. Остановить future polling.
2. Закрыть APPROVE_TELEGRAM_POLLING_START.
3. Закрыть APPROVE_TELEGRAM_RECEIVE_MESSAGE.
4. Закрыть APPROVE_TELEGRAM_SEND_MESSAGE.
5. Сбросить in-memory sessions.
6. Сохранить dry-run отчет.
7. Подтвердить send disabled.
8. Вернуться в readiness_only.
9. Сообщить пользователю.
"""


def run_shutdown_rehearsal() -> list[str]:
    return [
        "[PASS] polling stopped (fake)",
        "[PASS] gates closed (fake)",
        "[PASS] sessions cleared (fake)",
        "[PASS] report saved (dry-run)",
        "[PASS] send disabled confirmed",
        "[PASS] mode: readiness_only restored",
    ]


# ── Emergency Stop ──


@dataclass
class EmergencyStopState:
    active: bool = False
    reason: str = ""
    blocked_actions: list[str] = field(default_factory=lambda: [
        "polling", "webhook", "send", "token_read",
        "real_export", "external_api", "drive", "network_change",
    ])
    audit: dict[str, Any] = field(default_factory=lambda: {
        "safe_local": True, "live_blocked": True,
    })

    def activate(self, reason: str) -> None:
        self.active = True
        self.reason = reason

    def deactivate(self) -> None:
        self.active = False
        self.reason = ""


# ── Audit Trail ──


@dataclass
class AuditEvent:
    event_id: str = ""
    event_type: str = ""
    safe_local: bool = True
    dry_run: bool = True
    action: str = ""
    allowed: bool = True
    blocked_reason: str = ""
    risk_level: str = "low"
    session_id: str = ""
    draft_id: str = ""
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    metadata: dict[str, Any] = field(default_factory=lambda: {
        "no_token": True, "no_keys": True, "no_secrets": True,
        "no_real_data": True, "no_env": True,
    })

    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items()}


class AuditTrail:
    """In-memory audit trail. No persistent DB. No secrets."""

    def __init__(self) -> None:
        self._events: list[AuditEvent] = []

    def log(self, event_type: str, action: str, allowed: bool = True,
            blocked_reason: str = "", risk: str = "low") -> AuditEvent:
        event = AuditEvent(
            event_id=f"audit-{len(self._events) + 1:04d}",
            event_type=event_type, action=action,
            allowed=allowed, blocked_reason=blocked_reason, risk_level=risk,
        )
        self._events.append(event)
        return event

    def count(self) -> int:
        return len(self._events)

    def recent(self, n: int = 10) -> list[AuditEvent]:
        return self._events[-n:]

    def clear(self) -> None:
        self._events.clear()


# ── Live Readiness Board ──


READINESS_BOARD = """
╔════════════════════════════════════════╗
║     TELEGRAM LIVE READINESS BOARD     ║
╠════════════════════════════════════════╣
║ Dry-run scenarios          │   GO ✅  ║
║ Approval gates (10)        │ CLOSED   ║
║ Token policy               │ SAFE ✅  ║
║ Send guardrails            │ READY ✅ ║
║ Message safety hardening   │ READY ✅ ║
║ Duplicate protection       │ READY ✅ ║
║ Rate limit policy          │ READY ✅ ║
║ Idempotency policy         │ READY ✅ ║
║ Safe shutdown plan         │ READY ✅ ║
║ Emergency stop             │ READY ✅ ║
║ Audit trail model          │ READY ✅ ║
╠════════════════════════════════════════╣
║ Planning / hardening       │   GO ✅  ║
║ Actual live Telegram       │ NO-GO ❌  ║
╚════════════════════════════════════════╝
"""
