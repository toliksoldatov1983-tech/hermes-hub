"""First Live Approval Plan — staged plan for controlled Telegram live test.

All stages disabled. No token reads. No API calls.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any


class LiveTestStage(Enum):
    STAGE_0_CURRENT = "stage_0_current"
    STAGE_1_USER_APPROVAL = "stage_1_user_approval"
    STAGE_2_TOKEN_READINESS = "stage_2_token_readiness"
    STAGE_3_SINGLE_USER_ALLOWLIST = "stage_3_single_user_allowlist"
    STAGE_4_FIRST_POLLING = "stage_4_first_polling"
    STAGE_5_ROLLBACK = "stage_5_rollback"


@dataclass
class ApprovalStep:
    stage: LiveTestStage
    title: str
    description: str
    requires_approval: bool
    approval_gate: str
    is_completed: bool
    is_blocked: bool
    blocked_reason: str
    safe_actions: list[str]
    blocked_actions: list[str]

    def to_dict(self) -> dict:
        return {
            "stage": self.stage.value, "title": self.title,
            "requires_approval": self.requires_approval,
            "is_completed": self.is_completed,
            "is_blocked": self.is_blocked,
        }


APPROVAL_PLAN: list[ApprovalStep] = [
    ApprovalStep(
        stage=LiveTestStage.STAGE_0_CURRENT,
        title="Текущее состояние — dry-run only",
        description="Все компоненты готовы. Live Telegram disabled. Dry-run работает.",
        requires_approval=False,
        approval_gate="",
        is_completed=True,
        is_blocked=False,
        blocked_reason="",
        safe_actions=["dry_run", "e2e_test", "mock_chat"],
        blocked_actions=["live_telegram", "polling", "webhook", "token_read"],
    ),
    ApprovalStep(
        stage=LiveTestStage.STAGE_1_USER_APPROVAL,
        title="Явное подтверждение пользователя",
        description="Пользователь должен явно подтвердить переход к live preflight.",
        requires_approval=True,
        approval_gate="APPROVE_LIVE_PREFLIGHT",
        is_completed=False,
        is_blocked=True,
        blocked_reason="Ждёт явного подтверждения пользователя.",
        safe_actions=["review_plan", "dry_run"],
        blocked_actions=["token_read", "polling", "live_send"],
    ),
    ApprovalStep(
        stage=LiveTestStage.STAGE_2_TOKEN_READINESS,
        title="Token readiness — будущий шаг",
        description="Только после отдельного approval. Token не выводится, не логируется.",
        requires_approval=True,
        approval_gate="APPROVE_TELEGRAM_TOKEN_READ",
        is_completed=False,
        is_blocked=True,
        blocked_reason="APPROVE_TELEGRAM_TOKEN_READ required.",
        safe_actions=["show_policy", "dry_run"],
        blocked_actions=["token_read", "env_read", "token_log"],
    ),
    ApprovalStep(
        stage=LiveTestStage.STAGE_3_SINGLE_USER_ALLOWLIST,
        title="Single-user allowlist — будущий шаг",
        description="Только один разрешённый пользователь. Группы/каналы blocked.",
        requires_approval=True,
        approval_gate="APPROVE_TELEGRAM_RECEIVE_MESSAGE",
        is_completed=False,
        is_blocked=True,
        blocked_reason="APPROVE_TELEGRAM_RECEIVE_MESSAGE required.",
        safe_actions=["configure_allowlist"],
        blocked_actions=["group_chat", "unknown_user", "mass_send"],
    ),
    ApprovalStep(
        stage=LiveTestStage.STAGE_4_FIRST_POLLING,
        title="Первый контролируемый polling тест — будущий шаг",
        description="Короткий polling. Один пользователь. Автостоп. Без export.",
        requires_approval=True,
        approval_gate="APPROVE_TELEGRAM_POLLING_START",
        is_completed=False,
        is_blocked=True,
        blocked_reason="APPROVE_TELEGRAM_POLLING_START required.",
        safe_actions=["status", "dry_run_chat"],
        blocked_actions=["real_export", "external_api", "google_drive"],
    ),
    ApprovalStep(
        stage=LiveTestStage.STAGE_5_ROLLBACK,
        title="Rollback — всегда доступен",
        description="Остановить polling, закрыть gates, вернуться в dry-run.",
        requires_approval=False,
        approval_gate="",
        is_completed=False,
        is_blocked=False,
        blocked_reason="",
        safe_actions=["stop_polling", "close_gates", "dry_run"],
        blocked_actions=[],
    ),
]


@dataclass
class GoNoGoDecision:
    """Go/No-Go decision for live Telegram test."""

    planning_preflight: str = "GO"
    actual_live_telegram: str = "NO-GO"
    reason: str = ""
    user_action_required: str = ""
    next_safe_step: str = ""

    def to_dict(self) -> dict:
        return {
            "planning_preflight": self.planning_preflight,
            "actual_live_telegram": self.actual_live_telegram,
            "reason": self.reason,
            "user_action_required": self.user_action_required,
            "next_safe_step": self.next_safe_step,
        }


def get_go_nogo() -> GoNoGoDecision:
    return GoNoGoDecision(
        planning_preflight="GO",
        actual_live_telegram="NO-GO",
        reason=(
            "All approval gates CLOSED. Token not read. Polling disabled. "
            "Dry-run and planning are safe. Live requires explicit user approval "
            "for each stage."
        ),
        user_action_required=(
            "Для перехода к live: явно подтвердить APPROVE_LIVE_PREFLIGHT, "
            "затем APPROVE_TELEGRAM_TOKEN_READ, APPROVE_TELEGRAM_POLLING_START."
        ),
        next_safe_step="Продолжить dry-run тестирование или дать команду на live preflight.",
    )


ALLOWLIST_POLICY = """
Single-User Allowlist Policy (будущее):

1. Первый live тест — только ОДИН разрешённый пользователь.
2. chat_id задаётся вручную (не читается автоматически).
3. Групповые чаты — ЗАБЛОКИРОВАНЫ.
4. Каналы — ЗАБЛОКИРОВАНЫ.
5. Неизвестные chat_id — ЗАБЛОКИРОВАНЫ.
6. Массовая рассылка — ЗАБЛОКИРОВАНА.
7. Allowlist хранится в конфигурации (не в коде).
8. Изменение allowlist требует APPROVE_TELEGRAM_RECEIVE_MESSAGE.
"""


FIRST_POLLING_PLAN = """
Первый контролируемый polling тест (будущее):

1. Duration limit: 5 минут.
2. Message count limit: 5 сообщений.
3. Только один разрешённый пользователь (из allowlist).
4. Только безопасные ответы (статус, dry-run чат, Malyarka preview).
5. НИКАКОГО реального export.
6. НИКАКИХ внешних AI (Gemini/DeepSeek).
7. НИКАКОГО Google Drive.
8. Автостоп после лимита или ошибки.
9. Ручной стоп в любой момент.
10. Rollback: остановить polling, закрыть gates.
"""


WEBHOOK_FUTURE_PLAN = """
Webhook — будущий вариант (НЕ первый):

1. Webhook НЕ рекомендуется для первого live теста.
2. Требует public endpoint или tunnel (ngrok/Cloudflare).
3. Требует HTTPS + сертификат.
4. Требует APPROVE_TELEGRAM_WEBHOOK_START.
5. Требует APPROVE_NETWORK_CHANGE.
6. Выше риск, чем polling.
7. Polling безопаснее для первого теста.
"""


SEND_GUARDRAILS = """
Send Message Guardrails (будущее):

Перед отправкой live сообщения проверять:
  ✓ approval gate открыт (APPROVE_TELEGRAM_SEND_MESSAGE)
  ✓ chat_id в allowlist
  ✓ текст безопасен (нет секретов, токенов, ключей)
  ✓ не real export файл
  ✓ не опасная инструкция
  ✓ не массовая рассылка
  ✓ rate limit соблюдён (future)
  ✓ audit metadata записано
"""


ROLLBACK_PLAN = """
Rollback Plan:

1. Остановить polling немедленно.
2. Закрыть APPROVE_TELEGRAM_POLLING_START.
3. Закрыть APPROVE_TELEGRAM_RECEIVE_MESSAGE.
4. Закрыть APPROVE_TELEGRAM_SEND_MESSAGE.
5. Вернуться в readiness_only.
6. Подтвердить dry-run работает.
7. Сообщить пользователю результат.
"""
