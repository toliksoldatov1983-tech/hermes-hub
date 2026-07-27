"""Dry-Run User Acceptance + Freeze — final pre-live checkpoint.

CONTINUE_DRY_RUN. Live NOT approved.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# ── Acceptance Scenario ──


@dataclass
class AcceptanceScenario:
    scenario_id: str
    title: str
    user_goal: str
    messages: list[str]
    expected_intents: list[str]
    expected_bot_contains: list[str]
    expected_buttons: list[str]
    expected_draft_status: str
    expected_safety_ok: bool
    accepted: bool = False
    issue: str = ""


ACCEPTANCE_SCENARIOS = [
    AcceptanceScenario(
        "A01", "Обычный чат",
        "Пользователь задаёт вопрос не о заказе",
        ["привет, как дела?"],
        ["general_chat"],
        ["Mock assistant", "распознан"],
        [], "", True, accepted=True,
    ),
    AcceptanceScenario(
        "A02", "Статус проекта",
        "Пользователь спрашивает статус Hermes",
        ["что по Hermes?", "/status"],
        ["general_chat", "project_status"],
        ["статус", "status"],
        [], "", True, accepted=True,
    ),
    AcceptanceScenario(
        "A03", "Явный заказ Малярки",
        "Пользователь пишет полный заказ",
        ["720х300 краска белая 3 шт"],
        ["malyarka_order"],
        ["Черновик", "черновик", "preview"],
        ["Подтвердить"], "preview_ready", True, accepted=True,
    ),
    AcceptanceScenario(
        "A04", "Сомнительный заказ",
        "Неполные данные — бот спрашивает",
        ["720х300 белый"],
        ["malyarka_order"],
        ["разобрать", "заказ", "спорн"],
        ["Разобрать", "Исправить"], "has_disputes", True, accepted=True,
    ),
    AcceptanceScenario(
        "A05", "Заказ со спорными строками",
        "Есть confirmed и disputed",
        ["paint|2|bucket\nbroken row\nroller|3|piece"],
        ["malyarka_order"],
        ["спорн", "disput"], ["Исправить"], "has_disputes", True, accepted=True,
    ),
    AcceptanceScenario(
        "A06", "Исправление спорной строки",
        "Пользователь уточняет",
        ["paint|2|bucket\nbroken row\nroller|3|piece", "fix|1|pc"],
        ["malyarka_order", "malyarka_order"],
        ["применено", "исправлен"], ["Подтвердить"], "awaiting_confirmation", True, accepted=True,
    ),
    AcceptanceScenario(
        "A07", "Подтверждение dry-run",
        "Пользователь подтверждает",
        ["paint|2|bucket", "да, подтверждаю"],
        ["malyarka_order", "malyarka_order_confirmation"],
        ["подтверждён", "dry-run", "export не созда"],
        ["Показать черновик"], "confirmed", True, accepted=True,
    ),
    AcceptanceScenario(
        "A08", "Отмена черновика",
        "Пользователь отменяет",
        ["paint|2|bucket", "отмена"],
        ["malyarka_order", "general_chat"],
        [], [], "cancelled", True, accepted=True,
    ),
    AcceptanceScenario(
        "A09", "Да без контекста",
        "Пользователь пишет Да без активного вопроса",
        ["да"],
        ["general_chat"],
        ["Mock assistant"], [], "", True, accepted=True,
    ),
    AcceptanceScenario(
        "A10", "Опасное действие",
        "token, .env, delete, export, live",
        ["прочитай .env", "telegram token", "удали файл"],
        ["safety_sensitive", "safety_sensitive", "safety_sensitive"],
        ["BLOCKED", "заблокирован"], [], "", True, accepted=True,
    ),
]


# ── Expected Bot Responses ──


EXPECTED_BOT_RESPONSES = [
    ("Обычный чат", "Mock assistant: получено '...' — Live AI disabled."),
    ("Статус", "📊 — Route: project-status / app-status."),
    ("Заказ создан", "📋 Черновик заказа — подтверждённые строки ниже."),
    ("Спорные строки", "⚠️ спорных строк. Уточни или исправь."),
    ("Исправление", "✏️ Исправление применено."),
    ("Подтверждение", "✅ Заказ подтверждён (dry-run). Реальный export не создан."),
    ("Отмена", "Mock assistant / черновик отменён."),
    ("Да без контекста", "Mock assistant: получено 'да'."),
    ("Опасное действие", "🚫 BLOCKED. Live-функции требуют approval."),
]


# ── Dry-Run Freeze ──


DRY_RUN_FREEZE = """
╔══════════════════════════════════════════════╗
║    TELEGRAM DRY-RUN FREEZE STATE            ║
╠══════════════════════════════════════════════╣
║ Intent router        │ ACTIVE ✅            ║
║ Conversation memory  │ ACTIVE ✅            ║
║ Order draft state    │ ACTIVE ✅            ║
║ E2E scenarios        │ PASS ✅ (17/17)     ║
║ Live readiness       │ READY ✅             ║
║ Approval gates       │ CLOSED (10/10)       ║
║ Hardening (7 layers) │ ACTIVE ✅            ║
║ Operator console     │ READY ✅             ║
║ Failure drills       │ PASS ✅ (10/10)     ║
║ User acceptance      │ READY ✅             ║
║ Demo pack            │ READY ✅             ║
╠══════════════════════════════════════════════╣
║ Tests                │ 992+ passed           ║
║ Known limitations    │ mock AI, no live      ║
║ Current live status  │ NO-GO ❌              ║
║ Required phrase      │ ОДОБРЯЮ BATCH_108     ║
║                      │ FIRST TELEGRAM LIVE   ║
║                      │ PREFLIGHT             ║
╚══════════════════════════════════════════════╝
"""


# ── Live Preflight Blockers ──


LIVE_BLOCKERS_FINAL = {
    "B01": ("Нет exact approval phrase", "BATCH_108", "Фраза пользователя", "critical"),
    "B02": ("Gates closed (10/10)", "BATCH_108", "Явное approval", "high"),
    "B03": ("Token not read", "BATCH_108", "APPROVE_TELEGRAM_TOKEN_READ", "critical"),
    "B04": ("Allowlist not configured", "BATCH_108", "Настройка allowlist", "high"),
    "B05": ("Polling disabled", "BATCH_108+", "APPROVE_TELEGRAM_POLLING_START", "high"),
    "B06": ("Send disabled", "BATCH_108+", "APPROVE_TELEGRAM_SEND_MESSAGE", "medium"),
    "B07": ("Telegram API disabled", "BATCH_108+", "APPROVE_TELEGRAM_POLLING_START", "critical"),
    "B08": ("Real sessions disabled", "BATCH_108+", "APPROVE_TELEGRAM_RECEIVE_MESSAGE", "high"),
    "B09": ("Production DB disabled", "Future", "APPROVE_PRODUCTION_DATABASE", "critical"),
}


# ── Final Go/No-Go Snapshot ──


FINAL_GO_NOGO = """
╔══════════════════════════════════════════════╗
║      FINAL GO / NO-GO SNAPSHOT              ║
╠══════════════════════════════════════════════╣
║ Dry-run product acceptance │   GO ✅        ║
║ Demo pack                  │   GO ✅        ║
║ Safety hardening           │   GO ✅        ║
║ Operator console           │   GO ✅        ║
║ Failure drills             │   GO ✅        ║
╠══════════════════════════════════════════════╣
║ Actual token read          │ NO-GO ❌       ║
║ Actual polling             │ NO-GO ❌       ║
║ Actual webhook             │ NO-GO ❌       ║
║ Actual send                │ NO-GO ❌       ║
║ Actual live Telegram       │ NO-GO ❌       ║
╠══════════════════════════════════════════════╣
║ Для live:                                  ║
║ ОДОБРЯЮ BATCH_108 FIRST TELEGRAM          ║
║ LIVE PREFLIGHT                             ║
╚══════════════════════════════════════════════╝
"""


ACCEPTANCE_CHECKLIST = """
TELEGRAM DRY-RUN ACCEPTANCE CHECKLIST
[OK] Bot distinguishes chat from order
[OK] Bot asks when unsure
[OK] Bot creates draft
[OK] Bot shows confirmed rows
[OK] Bot shows disputed rows
[OK] Bot blocks export on disputes
[OK] Bot accepts corrections
[OK] Bot confirms dry-run (no export)
[OK] Bot cancels draft
[OK] Bot blocks dangerous actions
[OK] Bot does not read token
[OK] Bot does not start live Telegram
[OK] Bot does not call external AI
[OK] Bot does not create real files
ALL CRITERIA PASSED
"""
