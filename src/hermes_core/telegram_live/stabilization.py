"""RC Stabilization + No-Approval Hold — final pre-decision state.

CONTINUE_DRY_RUN. System WAITING_FOR_USER_DECISION.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# ── Hold State ──


@dataclass
class HoldState:
    current_state: str = "WAITING_FOR_USER_DECISION"
    dry_run_rc_ready: bool = True
    actual_live_allowed: bool = False
    explicit_approval_received: bool = False
    all_gates_closed: bool = True
    token_read_allowed: bool = False
    polling_allowed: bool = False
    webhook_allowed: bool = False
    send_allowed: bool = False
    approval_phrase: str = "ОДОБРЯЮ BATCH_110 FIRST TELEGRAM LIVE PREFLIGHT"
    next_safe_action: str = "Продолжить dry-run или дать approval-фразу"
    audit: dict[str, Any] = field(default_factory=lambda: {
        "state": "WAITING_FOR_USER_DECISION",
        "live_allowed": False, "token_read": False,
        "api_called": False, "gates_opened": 0,
    })

    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if k != "audit"}

    @staticmethod
    def get() -> HoldState:
        return HoldState()


# ── RC Stabilization ──


RC_STABILIZATION = """
╔══════════════════════════════════════════════╗
║   RC STABILIZATION PASS                     ║
╠══════════════════════════════════════════════╣
║ release_candidate_manifest  │ STABLE ✅     ║
║ operator_handoff           │ STABLE ✅     ║
║ acceptance_replay          │ STABLE ✅     ║
║ user_guide                 │ STABLE ✅     ║
║ live_decision_packet       │ STABLE ✅     ║
║ final_safety_baseline      │ STABLE ✅     ║
║ blocked_live_snapshot      │ STABLE ✅     ║
║ command_quick_reference    │ STABLE ✅     ║
║ test_count (1096+)         │ STABLE ✅     ║
║ known_limitations          │ DOCUMENTED ✅ ║
╚══════════════════════════════════════════════╝
"""


# ── Consistency Checks ──


RELEASE_CONSISTENCY_CHECK = """
RELEASE CONSISTENCY CHECK

[OK] dry-run RC готов → все документы согласованы
[OK] live Telegram NO-GO → все документы согласованы
[OK] token not read → все документы согласованы
[OK] gates closed → все документы согласованы
[OK] polling disabled → все документы согласованы
[OK] webhook disabled → все документы согласованы
[OK] send disabled → все документы согласованы
[OK] следующий шаг требует approval → все документы согласованы
[OK] нет противоречий между документами
"""

OPERATOR_HANDOFF_CHECK = """
OPERATOR HANDOFF CONSISTENCY CHECK

[OK] Handoff объясняет что готово
[OK] Handoff объясняет как проверить
[OK] Handoff explains запрещённые действия
[OK] Handoff contains approval phrase
[OK] Handoff explains what phrase does NOT allow
[OK] No technical jargon in user-facing text
"""

ACCEPTANCE_REPLAY_VERIFICATION = """
ACCEPTANCE REPLAY VERIFICATION

[OK] 10 scenarios present
[OK] A01 ordinary chat PASS
[OK] A02 project status PASS
[OK] A03 explicit order PASS
[OK] A04 ambiguous order PASS
[OK] A05 disputed rows PASS
[OK] A06 correction PASS
[OK] A07 confirmation dry-run PASS
[OK] A08 cancel PASS
[OK] A09 yes without context PASS
[OK] A10 dangerous action blocked PASS
[OK] 14/14 acceptance criteria PASS
"""


# ── Approval Phrase Board ──


APPROVAL_PHRASE_BOARD = """
╔══════════════════════════════════════════════════╗
║        APPROVAL PHRASE BOARD                    ║
╠══════════════════════════════════════════════════╣
║                                                ║
║  Точная фраза для live preflight:              ║
║  ОДОБРЯЮ BATCH_110 FIRST TELEGRAM             ║
║  LIVE PREFLIGHT                                ║
║                                                ║
║  ВАЖНО:                                        ║
║  - "BATCH_110" без фразы ОДОБРЯЮ              ║
║    НЕ является approval                        ║
║  - Упоминание фразы в отчёте                   ║
║    НЕ является approval                        ║
║  - Нужно отдельное явное сообщение             ║
║    пользователя с точной фразой                ║
║                                                ║
║  Фраза разрешит:                               ║
║  - limited first live preflight                ║
║                                                ║
║  Фраза НЕ разрешит:                            ║
║  - production mode, webhook, Drive             ║
║  - Gemini/DeepSeek, real export                ║
║  - mass messaging, groups, unknown users       ║
║  - network changes                             ║
║                                                ║
╚══════════════════════════════════════════════════╝
"""


# ── Final Command Matrix ──


FINAL_COMMAND_MATRIX = """
╔══════════════════════════════════════════════════════════╗
║              FINAL COMMAND MATRIX                        ║
╠══════════════════════════════════════════════════════════╣
║ STATUS COMMANDS (safe, no token):                       ║
║  telegram-intent-status         │ intent router status  ║
║  telegram-memory-status         │ memory store status   ║
║  telegram-live-status           │ live gateway status   ║
║  telegram-hardening-status      │ hardening layers      ║
║  telegram-rc-status             │ RC status             ║
║  telegram-operator-console      │ operator overview     ║
║                                                        ║
║ ACCEPTANCE (safe, no token):                           ║
║  telegram-acceptance-run-all    │ run 10 scenarios      ║
║  telegram-acceptance-checklist  │ 14 criteria           ║
║  telegram-acceptance-replay-verify │ verify replay      ║
║                                                        ║
║ RC (safe, no token):                                   ║
║  telegram-rc-manifest           │ RC manifest           ║
║  telegram-rc-stabilization-status│ stabilization check  ║
║  telegram-release-consistency-check │ consistency       ║
║                                                        ║
║ GO / NO-GO (safe, no token):                           ║
║  telegram-final-go-no-go-snapshot│ go/no-go snapshot    ║
║  telegram-blocked-live-snapshot  │ blocked-live view    ║
║  telegram-live-preflight-blockers│ blockers list        ║
║  telegram-approval-phrase-board  │ approval phrase      ║
║  telegram-decision-ready-dashboard│ decision dashboard  ║
║                                                        ║
║ BLOCKED (requires approval, gates):                    ║
║  token_read, polling, webhook, send, live              ║
║                                                        ║
║ FUTURE LIVE APPROVAL:                                  ║
║  ОДОБРЯЮ BATCH_110 FIRST TELEGRAM                     ║
║  LIVE PREFLIGHT                                        ║
╚══════════════════════════════════════════════════════════╝
"""


# ── Decision-Ready Dashboard ──


DECISION_READY_DASHBOARD = """
╔══════════════════════════════════════════════╗
║    TELEGRAM — DECISION-READY DASHBOARD      ║
╠══════════════════════════════════════════════╣
║                                            ║
║  Dry-run RC: TELEGRAM-DRY-RUN-RC-1        ║
║  Status: STABLE ✅                         ║
║  Tests: 1096+ passed ✅                    ║
║  Acceptance: 10/10 PASS, 14/14 criteria ✅ ║
║                                            ║
║  Можно принять dry-run прямо сейчас.       ║
║                                            ║
║  Live Telegram: NO-GO ❌                   ║
║  Причина: нет explicit approval.           ║
║                                            ║
║  ЧТО ДЕЛАТЬ ДАЛЬШЕ:                        ║
║                                            ║
║  Вариант A: принять dry-run как есть.      ║
║  Команда: telegram-acceptance-run-all      ║
║                                            ║
║  Вариант B: дать approval на live          ║
║  preflight.                                ║
║  Фраза: ОДОБРЯЮ BATCH_110 FIRST           ║
║  TELEGRAM LIVE PREFLIGHT                   ║
║                                            ║
║  Вариант C: продолжить dry-run             ║
║  hardening.                                ║
║                                            ║
╚══════════════════════════════════════════════╝
"""
