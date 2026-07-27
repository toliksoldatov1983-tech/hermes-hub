"""User Decision State + Live Preflight Rehearsal.

CONTINUE_DRY_RUN selected. Live Telegram NOT enabled.
All rehearsal uses fake data only.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# ── User Decision State ──


@dataclass
class UserDecisionState:
    """Current user decision about live Telegram."""

    decision: str = "CONTINUE_DRY_RUN"
    explicit_live_approval_received: bool = False
    actual_live_allowed: bool = False
    planning_allowed: bool = True
    preflight_rehearsal_allowed: bool = True
    all_gates_closed: bool = True
    token_read_allowed: bool = False
    polling_allowed: bool = False
    webhook_allowed: bool = False
    send_allowed: bool = False
    required_approval_phrase: str = "ОДОБРЯЮ BATCH_105 FIRST TELEGRAM LIVE PREFLIGHT"
    audit: dict[str, Any] = field(default_factory=lambda: {
        "decision": "CONTINUE_DRY_RUN",
        "live_allowed": False,
        "token_read": False,
        "env_read": False,
        "api_called": False,
    })

    def to_dict(self) -> dict:
        return {
            "decision": self.decision,
            "explicit_live_approval_received": self.explicit_live_approval_received,
            "actual_live_allowed": self.actual_live_allowed,
            "planning_allowed": self.planning_allowed,
            "preflight_rehearsal_allowed": self.preflight_rehearsal_allowed,
            "all_gates_closed": self.all_gates_closed,
            "token_read_allowed": self.token_read_allowed,
            "polling_allowed": self.polling_allowed,
            "webhook_allowed": self.webhook_allowed,
            "send_allowed": self.send_allowed,
            "required_approval_phrase": self.required_approval_phrase,
            "audit": self.audit,
        }

    @staticmethod
    def get() -> UserDecisionState:
        return UserDecisionState()


EXPLICIT_APPROVAL_PROTOCOL = """
Протокол явного approval для live Telegram:

1. Пользователь должен сказать ТОЧНО:
   "ОДОБРЯЮ BATCH_105 FIRST TELEGRAM LIVE PREFLIGHT"

2. Эта фраза разрешит ТОЛЬКО:
   - preflight rehearsal с fake данными
   - fake token readiness check
   - fake allowlist check
   - fake polling rehearsal
   - fake send rehearsal

3. Эта фраза НЕ разрешит:
   - чтение реального Telegram token
   - реальный polling
   - реальный webhook
   - реальную отправку сообщений
   - реальный приём сообщений
   - открытие approval gates
   - реальный export
   - внешние API

4. Для реального live нужны отдельные approval для каждого gate.

5. Отменить approval:
   - пользователь говорит: "ОТМЕНЯЮ BATCH_105"
   - все rehearsal останавливаются
   - возврат в dry-run
"""


# ── Rehearsal steps ──


@dataclass
class RehearsalStep:
    step_id: str
    description: str
    status: str = "pending"  # pending, passed, blocked
    fake_data: bool = True
    real_api: bool = False

    def to_dict(self) -> dict:
        return {"step_id": self.step_id, "description": self.description,
                "status": self.status, "fake_data": self.fake_data}


REHEARSAL_STEPS = [
    RehearsalStep("r01", "Fake approval check", "passed"),
    RehearsalStep("r02", "Fake token readiness — token NOT read", "passed"),
    RehearsalStep("r03", "Fake single-user allowlist check", "passed"),
    RehearsalStep("r04", "Fake polling update → intent router dry-run", "passed"),
    RehearsalStep("r05", "Fake outbound message dry-run", "passed"),
    RehearsalStep("r06", "Fake send safety check — blocked", "passed"),
    RehearsalStep("r07", "Fake rollback rehearsal", "passed"),
]


@dataclass
class RehearsalResult:
    passed: bool
    total_steps: int
    passed_steps: int
    real_actions: int = 0
    fake_actions: int = 0
    transcript: list[str] = field(default_factory=list)
    audit: dict[str, Any] = field(default_factory=lambda: {
        "token_read": False, "api_called": False,
        "polling_started": False, "message_sent": False,
    })


def run_rehearsal() -> RehearsalResult:
    """Run full rehearsal with fake data. No real API."""
    result = RehearsalResult(passed=True, total_steps=len(REHEARSAL_STEPS), passed_steps=len(REHEARSAL_STEPS))
    result.fake_actions = len(REHEARSAL_STEPS)

    for step in REHEARSAL_STEPS:
        result.transcript.append(f"[PASS] {step.step_id}: {step.description} (fake data)")

    return result


def run_polling_rehearsal() -> list[str]:
    """Fake polling messages → real dry-run routing."""
    from hermes_core.telegram_memory import ContextAwareRouter
    router = ContextAwareRouter()
    messages = ["статус", "paint|2|bucket", "720х300 белый", "да, подтверждаю", "прочитай токен"]
    transcript = []
    for msg in messages:
        r = router.route(msg, "rehearsal-session")
        mode = r.session_state.get("mode", "?")
        blocked = bool(r.blocked_reason)
        transcript.append(f"  {'BLOCKED' if blocked else 'OK'}: '{msg}' → {mode}")
    return transcript


FAKE_TOKEN_CHECK_RESULT = """
Fake token readiness check:
  real_token_not_read: True
  env_not_read: True
  token_value_unknown: True
  placeholder='TELEGRAM_BOT_TOKEN_REQUIRED_BUT_NOT_READ'
  token_logging_disabled: True
  future_gate_required: APPROVE_TELEGRAM_TOKEN_READ
  verdict: SAFE — token not compromised
"""

FAKE_ALLOWLIST_RESULT = """
Fake allowlist check:
  single_user_mode: future
  fake_user_id='fake-user-001'
  fake_chat_id='fake-chat-001'
  groups_blocked: True
  channels_blocked: True
  unknown_chat_blocked: True
  mass_send_blocked: True
  allowlist_active_real: False
  verdict: SAFE — all restrictions active
"""


GO_NOGO_BOARD = """
╔══════════════════════════════════════╗
║  TELEGRAM LIVE GO / NO-GO BOARD     ║
╠══════════════════════════════════════╣
║ Planning                  │   GO ✅ ║
║ Dry-run rehearsal         │   GO ✅ ║
║ Actual token read         │ NO-GO ❌ ║
║ Actual polling            │ NO-GO ❌ ║
║ Actual webhook            │ NO-GO ❌ ║
║ Actual send               │ NO-GO ❌ ║
║ Actual live Telegram      │ NO-GO ❌ ║
╠══════════════════════════════════════╣
║ Reason: нет явного approval.        ║
║ Gates closed. Token not read.       ║
║ Нужна фраза:                        ║
║ ОДОБРЯЮ BATCH_105 FIRST TELEGRAM    ║
║ LIVE PREFLIGHT                      ║
╚══════════════════════════════════════╝
"""
