"""Dry-Run RC Acceptance + Closeout — final hold state.

ACCEPT_DRY_RUN_RC_AND_CLOSEOUT_HOLD. Live NOT approved.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# ── Signoff ──


DRY_RUN_SIGNOFF = """
╔══════════════════════════════════════════════════╗
║    TELEGRAM DRY-RUN ACCEPTANCE SIGN-OFF         ║
╠══════════════════════════════════════════════════╣
║                                                ║
║  Telegram dry-run RC: ACCEPTED ✅              ║
║  Dry-run user acceptance: PASS ✅              ║
║  Acceptance scenarios: 10/10 PASS ✅           ║
║  Acceptance criteria: 14/14 PASS ✅            ║
║  Safety checks: ALL PASS ✅                    ║
║  Operator handoff: READY ✅                    ║
║  RC stabilization: STABLE ✅                   ║
║                                                ║
║  ──────────────────────────────────────        ║
║                                                ║
║  Actual live Telegram: NOT APPROVED ❌         ║
║  Actual live Telegram: NOT ENABLED ❌          ║
║  Token: NOT READ ❌                            ║
║  Polling: DISABLED ❌                          ║
║  Webhook: DISABLED ❌                          ║
║  Send: DISABLED ❌                             ║
║                                                ║
║  Dry-run accepted. Live not approved.          ║
║                                                ║
╚══════════════════════════════════════════════════╝
"""


# ── RC Closeout Manifest ──


RC_CLOSEOUT = """
╔══════════════════════════════════════════════════╗
║    TELEGRAM DRY-RUN RC CLOSEOUT MANIFEST        ║
╠══════════════════════════════════════════════════╣
║ RC ID: TELEGRAM-DRY-RUN-RC-1                    ║
║ Status: CLOSED (dry-run accepted)               ║
║ Test count: ~710+ passed                        ║
║ Acceptance: PASS (10/10 scenarios)              ║
║                                                ║
║ ACCEPTED SCOPE:                                 ║
║ intent_router, conversation_memory,             ║
║ order_draft, Malyarka_dry_run, e2e_scenarios,  ║
║ acceptance_pack, operator_handoff,              ║
║ safety_7_layers, operator_console,              ║
║ failure_drills_10, rc_stabilization             ║
║                                                ║
║ NOT ACCEPTED SCOPE (LIVE):                      ║
║ live_telegram, token_read, polling,             ║
║ webhook, send_message, real_export,             ║
║ production_db, external_ai, google_drive         ║
║                                                ║
║ NEXT DECISIONS:                                 ║
║ 1. Dry-run HOLD (default)                       ║
║ 2. Live preflight approval                      ║
║ 3. Switch project line                          ║
╚══════════════════════════════════════════════════╝
"""


# ── Final Hold State ──


FINAL_HOLD_STATE = """
╔══════════════════════════════════════════════════╗
║    TELEGRAM FINAL HOLD STATE                    ║
╠══════════════════════════════════════════════════╣
║ current_state: DRY_RUN_ACCEPTED_WAITING         ║
║ dry_run_rc_accepted: TRUE                       ║
║ actual_live_allowed: FALSE                      ║
║ explicit_approval_received: FALSE               ║
║ all_gates_closed: TRUE                          ║
║ token_read_allowed: FALSE                       ║
║ polling_allowed: FALSE                          ║
║ webhook_allowed: FALSE                          ║
║ send_allowed: FALSE                             ║
╚══════════════════════════════════════════════════╝
"""


# ── Operator Decision Board ──


OPERATOR_DECISION_BOARD = """
╔══════════════════════════════════════════════════╗
║        OPERATOR DECISION BOARD                  ║
╠══════════════════════════════════════════════════╣
║                                                ║
║  Вариант A: Оставить Telegram в dry-run HOLD  ║
║  Безопасно. Ничего live не включается.         ║
║  → BATCH_111_CONTINUE_DRY_RUN_HOLD             ║
║                                                ║
║  Вариант B: Дать approval на live preflight    ║
║  Требуется точная фраза:                       ║
║  ОДОБРЯЮ BATCH_111 FIRST TELEGRAM             ║
║  LIVE PREFLIGHT                                ║
║  → BATCH_111_FIRST_TELEGRAM_LIVE_PREFLIGHT     ║
║                                                ║
║  Вариант C: Mobile / Tailscale                 ║
║  → BATCH_111_TAILSCALE_PHONE_ACCESS            ║
║                                                ║
║  Вариант D: Malyarka export dry-run            ║
║  → BATCH_111_MALYARKA_EXPORT_DRY_RUN           ║
║                                                ║
║  Вариант E: AI provider real integration plan  ║
║  → BATCH_111_AI_PROVIDER_REAL_PLAN             ║
║                                                ║
║  ПО УМОЛЧАНИЮ (без approval):                  ║
║  → BATCH_111_CONTINUE_DRY_RUN_HOLD             ║
║                                                ║
╚══════════════════════════════════════════════════╝
"""


# ── Next Path Selector ──


NEXT_PATH_SELECTOR = """
NEXT PATH SELECTOR

Default (no approval):
  BATCH_111_CONTINUE_DRY_RUN_HOLD_OR_SWITCH_TO_NEXT_PROJECT_LINE

If user says: ОДОБРЯЮ BATCH_111 FIRST TELEGRAM LIVE PREFLIGHT
  → BATCH_111_FIRST_TELEGRAM_LIVE_PREFLIGHT_IF_EXPLICITLY_APPROVED

If user says: переключаемся на mobile
  → BATCH_111_TAILSCALE_PHONE_ACCESS_USER_APPROVAL_PLAN

If user says: переключаемся на Malyarka export
  → BATCH_111_MALYARKA_EXPORT_DRY_RUN_AND_FILE_CONTRACTS

IMPORTANT: "BATCH_111" without ОДОБРЯЮ is NOT approval.
"""


# ── Approval Phrase ──


LIVE_APPROVAL_PHRASE = """
╔══════════════════════════════════════════════════╗
║    LIVE APPROVAL PHRASE BOARD (FINAL)           ║
╠══════════════════════════════════════════════════╣
║                                                ║
║  Точная фраза:                                 ║
║  ОДОБРЯЮ BATCH_111 FIRST TELEGRAM             ║
║  LIVE PREFLIGHT                                ║
║                                                ║
║  РАЗРЕШИТ:                                     ║
║  - limited first live preflight                ║
║                                                ║
║  НЕ РАЗРЕШИТ:                                  ║
║  - production mode, webhook, Drive             ║
║  - Gemini/DeepSeek, real export                ║
║  - mass messaging, groups, unknown users       ║
║  - network changes                             ║
║                                                ║
║  НЕ ЯВЛЯЕТСЯ APPROVAL:                         ║
║  - "BATCH_111" без ОДОБРЯЮ                     ║
║  - упоминание фразы в отчёте                   ║
║  - обсуждение live preflight                   ║
║                                                ║
╚══════════════════════════════════════════════════╝
"""


# ── Final User Summary ──


FINAL_USER_SUMMARY = """
╔══════════════════════════════════════════════════╗
║     TELEGRAM DRY-RUN — ИТОГОВАЯ СВОДКА         ║
╠══════════════════════════════════════════════════╣
║                                                ║
║  ЧТО ГОТОВО:                                   ║
║  - Бот различает чат и заказ ✅                ║
║  - Бот создаёт черновик и показывает preview ✅║
║  - Бот исправляет спорные строки ✅             ║
║  - Бот подтверждает заказы (dry-run) ✅         ║
║  - Бот блокирует опасные действия ✅            ║
║  - 10 acceptance сценариев PASS ✅              ║
║  - 14 acceptance критериев PASS ✅              ║
║  - Operator console + failure drills ✅         ║
║                                                ║
║  ЧТО ЗАПРЕЩЕНО:                                ║
║  - Live Telegram ❌                              ║
║  - Реальный token ❌                             ║
║  - Polling / webhook ❌                          ║
║  - Реальный export ❌                            ║
║  - Gemini / DeepSeek ❌                          ║
║  - Google Drive ❌                               ║
║                                                ║
║  КАК ПРОВЕРИТЬ:                                ║
║  telegram-acceptance-run-all                   ║
║  telegram-operator-console                     ║
║                                                ║
║  ЧТО ДАЛЬШЕ:                                   ║
║  - Оставить в dry-run HOLD                     ║
║  - Или дать approval на live:                  ║
║    ОДОБРЯЮ BATCH_111 FIRST TELEGRAM           ║
║    LIVE PREFLIGHT                              ║
║  - Или переключиться на mobile/export          ║
║                                                ║
╚══════════════════════════════════════════════════╝
"""
