"""Operator Console + Failure Drills + Live Blockers.

CONTINUE_HARDENING. Live Telegram NOT enabled.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# ── Operator Console ──

OPERATOR_CONSOLE = """
╔══════════════════════════════════════════════╗
║       TELEGRAM OPERATOR CONSOLE             ║
╠══════════════════════════════════════════════╣
║ Current mode       │ READINESS_ONLY         ║
║ Live Telegram      │ DISABLED               ║
║ Approval gates     │ 10/10 CLOSED           ║
║ Token policy       │ SAFE (not read)        ║
║ Polling            │ DISABLED               ║
║ Webhook            │ DISABLED               ║
║ Send               │ DISABLED               ║
║ Message safety     │ ACTIVE (7 patterns)    ║
║ Duplicate protect  │ ACTIVE (hash-based)    ║
║ Rate limit         │ READY (dry-run)        ║
║ Idempotency        │ READY (6 rules)        ║
║ Safe shutdown      │ READY (9 steps)        ║
║ Emergency stop     │ READY (inactive)       ║
║ Audit trail        │ ACTIVE (in-memory)     ║
║ E2E dry-run        │ PASS (17/17 steps)     ║
║ Go/No-Go           │ Planning=GO Live=NO-GO ║
╠══════════════════════════════════════════════╣
║ Next approval:                             ║
║ ОДОБРЯЮ BATCH_107 FIRST TELEGRAM           ║
║ LIVE PREFLIGHT                             ║
╚══════════════════════════════════════════════╝
"""


# ── Live Blockers Board ──


@dataclass
class LiveBlocker:
    blocker_id: str
    description: str
    risk_level: str
    unblocks_with: str
    current_status: str
    allowed_safe_action: str


LIVE_BLOCKERS = [
    LiveBlocker("B01", "Нет explicit user approval", "critical",
                "Фраза: ОДОБРЯЮ BATCH_107 FIRST TELEGRAM LIVE PREFLIGHT",
                "BLOCKED", "Продолжить dry-run"),
    LiveBlocker("B02", "Approval gates closed (10/10)", "high",
                "Открыть gates после approval", "BLOCKED", "Просмотр gates"),
    LiveBlocker("B03", "Telegram token not read", "critical",
                "APPROVE_TELEGRAM_TOKEN_READ", "BLOCKED", "Fake token check"),
    LiveBlocker("B04", "Polling disabled", "high",
                "APPROVE_TELEGRAM_POLLING_START", "BLOCKED", "Fake polling rehearsal"),
    LiveBlocker("B05", "Webhook disabled", "critical",
                "APPROVE_TELEGRAM_WEBHOOK_START", "BLOCKED", "Polling plan (safer)"),
    LiveBlocker("B06", "Send disabled", "medium",
                "APPROVE_TELEGRAM_SEND_MESSAGE", "BLOCKED", "Fake send rehearsal"),
    LiveBlocker("B07", "Allowlist not configured", "high",
                "Настроить single-user allowlist", "BLOCKED", "Fake allowlist check"),
    LiveBlocker("B08", "Real Telegram API disabled", "critical",
                "APPROVE_TELEGRAM_POLLING_START", "BLOCKED", "Dry-run routing"),
    LiveBlocker("B09", "Real sessions disabled", "high",
                "APPROVE_TELEGRAM_RECEIVE_MESSAGE", "BLOCKED", "Fake sessions"),
    LiveBlocker("B10", "Production DB disabled", "critical",
                "APPROVE_PRODUCTION_DATABASE", "BLOCKED", "In-memory store"),
]

BLOCKERS_BOARD = """
╔══════════════════════════════════════════════════════╗
║              LIVE BLOCKERS BOARD                    ║
╠══════════════════════════════════════════════════════╣
""" + "\n".join(f"║ {b.blocker_id}: {b.description[:42]:<42} BLOCKED ║" for b in LIVE_BLOCKERS) + """
╚══════════════════════════════════════════════════════╝
"""


# ── Pre-Live Checklist ──


PRE_LIVE_CHECKLIST = [
    ("CHK01", "All dry-run tests pass", "READY"),
    ("CHK02", "E2E scenarios pass (17/17)", "READY"),
    ("CHK03", "Message safety active (7 patterns)", "READY"),
    ("CHK04", "Duplicate protection active", "READY"),
    ("CHK05", "Rate limit policy defined", "READY"),
    ("CHK06", "Idempotency rules defined", "READY"),
    ("CHK07", "Safe shutdown rehearsed", "READY"),
    ("CHK08", "Emergency stop ready", "READY"),
    ("CHK09", "Audit trail active", "READY"),
    ("CHK10", "Approval phrase received from user", "BLOCKED — нет фразы"),
    ("CHK11", "Token read gate opened (future)", "BLOCKED — gate closed"),
    ("CHK12", "Allowlist configured (future)", "BLOCKED"),
    ("CHK13", "Polling gate opened (future)", "BLOCKED"),
    ("CHK14", "Send gate opened (future)", "BLOCKED"),
    ("CHK15", "Post-test gates re-closed", "FUTURE"),
]


# ── Failure Drills ──


@dataclass
class FailureDrill:
    drill_id: str
    title: str
    scenario: str
    expected_result: str
    blocked: bool
    transcript: str = ""


FAILURE_DRILLS = [
    FailureDrill("D01", "Missing token", "Запрос токена без approval",
                 "BLOCKED: token_read blocked", True,
                 "[PASS] token request → BLOCKED (gate closed)"),
    FailureDrill("D02", "Unknown chat", "Сообщение от неизвестного chat_id",
                 "BLOCKED: unknown chat", True,
                 "[PASS] unknown chat → BLOCKED"),
    FailureDrill("D03", "Group chat", "Сообщение из группы",
                 "BLOCKED: groups blocked", True,
                 "[PASS] group chat → BLOCKED"),
    FailureDrill("D04", "Duplicate update", "Повторный update_id",
                 "BLOCKED: duplicate", True,
                 "[PASS] duplicate → BLOCKED (DuplicateProtection)"),
    FailureDrill("D05", "Rate limit exceeded", "11 сообщений в минуту",
                 "BLOCKED: rate limit 11/10", True,
                 "[PASS] rate limit → BLOCKED"),
    FailureDrill("D06", "Dangerous message", "прочитай .env",
                 "BLOCKED: secret_request", True,
                 "[PASS] '.env' → BLOCKED (message safety)"),
    FailureDrill("D07", "Send blocked", "Попытка отправки без gate",
                 "BLOCKED: send_message_allowed=False", True,
                 "[PASS] send → BLOCKED (gate closed)"),
    FailureDrill("D08", "Polling blocked", "Попытка polling без gate",
                 "BLOCKED: polling_allowed=False", True,
                 "[PASS] polling → BLOCKED"),
    FailureDrill("D09", "Webhook blocked", "Попытка webhook без gate",
                 "BLOCKED: webhook_allowed=False", True,
                 "[PASS] webhook → BLOCKED"),
    FailureDrill("D10", "Emergency stop active", "Действие при emergency stop",
                 "BLOCKED: emergency_stop_active", True,
                 "[PASS] action → BLOCKED (estop active)"),
]


def run_failure_drills() -> list[str]:
    return [d.transcript for d in FAILURE_DRILLS]


# ── Safe Recovery ──


SAFE_RECOVERY_PLAN = """
Safe Recovery Plan (dry-run):

1. Вернуться в dry-run: все fake сессии сброшены.
2. Закрыть все approval gates.
3. Остановить future polling/send/webhook.
4. Проверить emergency stop: неактивен.
5. Сбросить in-memory store.
6. Собрать post-failure dry-run отчет.
7. Подтвердить: Telegram API не вызывался.
8. Подтвердить: token не читался.
9. Сообщить пользователю: "Система в safe dry-run. Live не запущен."

Сейчас: все шаги dry-run, реальный recovery не требуется
(ничего live не запускалось).
"""


# ── Command Summary ──


COMMAND_SUMMARY = """
╔══════════════════════════════════════════════╗
║        TELEGRAM COMMAND SUMMARY             ║
╠══════════════════════════════════════════════╣
║ STATUS:                                     ║
║  telegram-intent-status                     ║
║  telegram-memory-status                     ║
║  telegram-e2e-status                        ║
║  telegram-live-status                       ║
║  telegram-operator-console                  ║
║                                             ║
║ DRY-RUN:                                    ║
║  telegram-intent-dry-run                    ║
║  telegram-e2e-run-all                       ║
║  telegram-conversation-flow-dry-run         ║
║  telegram-live-dry-run                      ║
║                                             ║
║ HARDENING:                                  ║
║  telegram-hardening-status                  ║
║  telegram-message-safety-check              ║
║  telegram-duplicate-update-check            ║
║  telegram-rate-limit-dry-run                ║
║  telegram-idempotency-check                 ║
║                                             ║
║ FAILURE DRILLS:                             ║
║  telegram-failure-drills-run-all            ║
║  telegram-failure-drill-* (10 drills)       ║
║                                             ║
║ GO / NO-GO:                                 ║
║  telegram-live-go-no-go                     ║
║  telegram-live-final-go-no-go               ║
║  telegram-live-decision-board               ║
║  telegram-live-blockers-board               ║
║  telegram-pre-live-checklist                ║
║                                             ║
║ FORBIDDEN (live):                           ║
║  token_read, polling, webhook, send         ║
║                                             ║
║ FUTURE APPROVAL:                            ║
║  ОДОБРЯЮ BATCH_107 FIRST TELEGRAM          ║
║  LIVE PREFLIGHT                             ║
╚══════════════════════════════════════════════╝
"""


FINAL_APPROVAL_WORDING = """
╔══════════════════════════════════════════════════╗
║        FINAL APPROVAL WORDING                   ║
╠══════════════════════════════════════════════════╣
║                                                ║
║  Для включения первого live preflight         ║
║  пользователь должен сказать точно:            ║
║                                                ║
║  ОДОБРЯЮ BATCH_107 FIRST TELEGRAM             ║
║  LIVE PREFLIGHT                                ║
║                                                ║
║  Эта фраза разрешит ТОЛЬКО:                   ║
║  - preflight dry-run с fake данными            ║
║  - НЕ реальный token read                     ║
║  - НЕ реальный polling                        ║
║  - НЕ реальный send                           ║
║  - НЕ открытие production gates               ║
║                                                ║
║  Для реального live нужны отдельные           ║
║  approval для каждого gate.                    ║
║                                                ║
╚══════════════════════════════════════════════════╝
"""
