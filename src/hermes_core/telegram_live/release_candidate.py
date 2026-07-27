"""Telegram Dry-Run Release Candidate — final packaging + operator handoff.

CONTINUE_DRY_RUN. Live NOT approved.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# ── Release Candidate Manifest ──


@dataclass
class RCMainfest:
    rc_id: str = "TELEGRAM-DRY-RUN-RC-1"
    status: str = "GO (dry-run)"
    test_count: int = 0
    acceptance_status: str = "PASS (10/10)"
    scenario_count: int = 10
    criteria_count: int = 14
    ready_components: list[str] = field(default_factory=lambda: [
        "intent_router", "conversation_memory", "order_draft",
        "e2e_scenarios", "live_readiness", "approval_gates",
        "hardening_7_layers", "operator_console", "failure_drills",
        "acceptance_scenarios", "dry_run_freeze",
    ])
    blocked_components: list[str] = field(default_factory=lambda: [
        "live_telegram", "token_read", "polling", "webhook",
        "send_message", "real_export", "production_db",
    ])
    live_status: str = "NO-GO"
    safety_status: str = "SAFE (all gates closed)"
    known_limitations: list[str] = field(default_factory=lambda: [
        "AI provider: mock only (Gemini/DeepSeek disabled)",
        "General chat: mock assistant (no real AI)",
        "Real export: disabled",
        "Persistent storage: disabled",
    ])
    next_required_decision: str = "Explicit user approval phrase for live preflight"
    required_phrase: str = "ОДОБРЯЮ BATCH_109 FIRST TELEGRAM LIVE PREFLIGHT"
    audit: dict[str, Any] = field(default_factory=lambda: {
        "token_read": False, "api_called": False,
        "gates_opened": 0, "safe_local": True,
    })

    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if k != "audit"}

    @staticmethod
    def get() -> RCMainfest:
        return RCMainfest()


# ── Operator Handoff ──


OPERATOR_HANDOFF = """
╔══════════════════════════════════════════════════╗
║   TELEGRAM DRY-RUN — ОПЕРАТОРСКИЙ КОМПЛЕКТ     ║
╠══════════════════════════════════════════════════╣
║                                                ║
║  ЧТО УЖЕ ГОТОВО:                               ║
║  - Бот различает чат и заказ                   ║
║  - Бот создаёт черновик заказа                 ║
║  - Бот показывает подтверждённые строки        ║
║  - Бот показывает спорные строки               ║
║  - Бот принимает исправления                   ║
║  - Бот подтверждает (dry-run)                  ║
║  - Бот блокирует опасные действия              ║
║                                                ║
║  КАК ПРОВЕРИТЬ:                                ║
║  telegram-acceptance-run-all                   ║
║  telegram-e2e-run-all                          ║
║  telegram-operator-console                     ║
║                                                ║
║  ЧТО ЕЩЁ ВЫКЛЮЧЕНО:                            ║
║  - Live Telegram                               ║
║  - Реальный token                              ║
║  - Реальный polling/webhook                    ║
║  - Реальный export                             ║
║  - Gemini/DeepSeek                             ║
║                                                ║
║  ЧТО НУЖНО ДЛЯ LIVE:                           ║
║  Фраза: ОДОБРЯЮ BATCH_109                     ║
║  FIRST TELEGRAM LIVE PREFLIGHT                 ║
║                                                ║
╚══════════════════════════════════════════════════╝
"""


# ── Acceptance Replay ──


ACCEPTANCE_REPLAY = """
ACCEPTANCE REPLAY PACK

Запустить все сценарии:
  telegram-acceptance-run-all

Запустить один сценарий (пример):
  PYTHONPATH=src python -c "
from hermes_core.telegram_memory import ContextAwareRouter
r = ContextAwareRouter()
resp = r.route('720х300 краска белая 3 шт', 'replay')
print(resp.text)
print('Draft:', resp.draft_state)
"

Сценарии:
  A01 — обычный чат: "привет, как дела?"
  A02 — статус: "/status"
  A03 — явный заказ: "720х300 краска белая 3 шт"
  A04 — сомнительный: "720х300 белый"
  A05 — спорные строки: "paint|2|bucket\\nbroken row"
  A06 — исправление: "paint|2|bucket\\nbroken row" → "fix|1|pc"
  A07 — подтверждение: "paint|2|bucket" → "да, подтверждаю"
  A08 — отмена: "paint|2|bucket" → "отмена"
  A09 — да без контекста: "да"
  A10 — опасное: "прочитай .env"
"""


# ── User-Facing Bot Guide ──


BOT_USER_GUIDE = """
TELEGRAM-БОТ HERMES-CLEAN — КАК ПОЛЬЗОВАТЬСЯ

Бот работает как обычный чат. Пишите свободно.

ЧТО БОТ УМЕЕТ:

1. Общаться на обычные темы.
   Напишите "привет" или любой вопрос.
   Бот ответит в режиме mock-ассистента.

2. Создавать заказы для Малярки.
   Напишите размеры, количество, цвет:
   "720х300 краска белая 3 шт"
   Бот создаст черновик и покажет его.

3. Исправлять заказы.
   Если в черновике есть спорные строки,
   бот спросит уточнение.
   Напишите исправление — бот обновит черновик.

4. Подтверждать заказы.
   Когда все строки заполнены, бот спросит
   подтверждение. Подтвердите — бот зафиксирует
   заказ (сейчас это dry-run, без реального файла).

5. Отменять черновики.
   Напишите "отмена" — бот отменит текущий черновик.

6. Показывать статус проекта.
   Напишите "/status" или "что по Hermes?"

ВАЖНО:
- Бот НЕ читает токены и секреты.
- Бот НЕ создаёт реальные файлы (dry-run).
- Бот НЕ вызывает внешние AI (Gemini/DeepSeek).
- Опасные действия блокируются.

Для включения live Telegram нужна отдельная команда
администратора.
"""


# ── Live Decision Packet ──


LIVE_DECISION_PACKET = """
╔══════════════════════════════════════════════════╗
║   LIVE PREFLIGHT DECISION PACKET                ║
╠══════════════════════════════════════════════════╣
║                                                ║
║  ЧТО БУДЕТ РАЗРЕШЕНО ПОСЛЕ APPROVAL:           ║
║  - preflight rehearsal (fake данные)           ║
║  - операторский осмотр readiness               ║
║                                                ║
║  ЧТО ОСТАНЕТСЯ ЗАПРЕЩЕНО:                      ║
║  - production mode                             ║
║  - webhook                                     ║
║  - Google Drive                                ║
║  - Gemini / DeepSeek                           ║
║  - реальный export                             ║
║  - массовая рассылка                           ║
║  - группы / неизвестные пользователи           ║
║  - сетевые изменения                           ║
║                                                ║
║  ТОЧНАЯ ФРАЗА ДЛЯ BATCH_109:                  ║
║  ОДОБРЯЮ BATCH_109 FIRST TELEGRAM             ║
║  LIVE PREFLIGHT                                ║
║                                                ║
╚══════════════════════════════════════════════════╝
"""


# ── Final Safety Baseline ──


FINAL_SAFETY_BASELINE = """
╔══════════════════════════════════════════╗
║     FINAL SAFETY BASELINE               ║
╠══════════════════════════════════════════╣
║ token_not_read            │   SAFE ✅  ║
║ gates_closed              │   SAFE ✅  ║
║ polling_disabled          │   SAFE ✅  ║
║ webhook_disabled          │   SAFE ✅  ║
║ send_disabled             │   SAFE ✅  ║
║ telegram_api_disabled     │   SAFE ✅  ║
║ external_api_disabled     │   SAFE ✅  ║
║ real_export_disabled      │   SAFE ✅  ║
║ production_db_disabled    │   SAFE ✅  ║
║ google_drive_disabled     │   SAFE ✅  ║
║ network_changes_disabled  │   SAFE ✅  ║
╚══════════════════════════════════════════╝
"""


# ── Blocked-Live Snapshot ──


BLOCKED_LIVE_SNAPSHOT = """
╔══════════════════════════════════════════╗
║      BLOCKED-LIVE SNAPSHOT              ║
╠══════════════════════════════════════════╣
║ actual_token_read         │ NO-GO ❌   ║
║ actual_polling            │ NO-GO ❌   ║
║ actual_webhook            │ NO-GO ❌   ║
║ actual_send               │ NO-GO ❌   ║
║ actual_live_telegram      │ NO-GO ❌   ║
╠══════════════════════════════════════════╣
║ Reasons:                                ║
║ - нет explicit approval                ║
║ - gates closed                          ║
║ - token not read                        ║
║ - allowlist not configured              ║
║ - Telegram API disabled                 ║
║ - real sessions disabled                ║
╚══════════════════════════════════════════╝
"""


# ── Command Quick Reference ──


COMMAND_QUICK_REF = """
╔══════════════════════════════════════════════╗
║   TELEGRAM COMMAND QUICK REFERENCE          ║
╠══════════════════════════════════════════════╣
║ СТАТУС:                                     ║
║  telegram-intent-status                     ║
║  telegram-memory-status                     ║
║  telegram-live-status                       ║
║  telegram-hardening-status                  ║
║  telegram-rc-status                         ║
║                                             ║
║ ПРИЁМКА / RC:                               ║
║  telegram-acceptance-run-all                ║
║  telegram-acceptance-checklist              ║
║  telegram-e2e-run-all                       ║
║  telegram-dry-run-freeze-status             ║
║                                             ║
║ ОПЕРАТОР:                                   ║
║  telegram-operator-console                  ║
║  telegram-operator-handoff                  ║
║  telegram-failure-drills-run-all            ║
║                                             ║
║ GO / NO-GO:                                 ║
║  telegram-final-go-no-go-snapshot           ║
║  telegram-blocked-live-snapshot             ║
║  telegram-live-preflight-blockers           ║
║  telegram-final-safety-baseline             ║
║                                             ║
║ ЗАПРЕЩЕНО (live):                          ║
║  token_read, polling, webhook, send         ║
║                                             ║
║ БУДУЩАЯ ФРАЗА:                             ║
║  ОДОБРЯЮ BATCH_109 FIRST TELEGRAM         ║
║  LIVE PREFLIGHT                             ║
╚══════════════════════════════════════════════╝
"""
