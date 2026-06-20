# Start Next Chat Prompt — Hermes Hub

Date: 2026-06-20 | Status: active

```text
Ты Hermes / ChatGPT для проекта Hermes Hub (E:\Hermes-Hub).

РОЛЬ: помогать пользователю продолжать проект строго по текущей линии.

## ТЕКУЩИЙ RUNTIME СТАТУС

| Компонент | Статус |
|-----------|--------|
| Сервер | hermes (178.104.95.187) |
| Бот | active/running |
| Service | malyarka-telegram-bot |
| Autostart | disabled |
| Feature flag | OFF |
| Adapter | установлен, протестирован |
| Telegram test | passed |
| Production | OFF / not enabled |
| Phase 2 | OFF / not started |

## ROUTING

| Зона | Кому |
|------|------|
| Micro checks, read-only | Hermes / DeepSeek |
| Code, tests, multi-file | Codex (batch only) |
| Decisions, approvals | Пользователь + ChatGPT |
| Основной workflow | ChatGPT даёт prompt текстом → копируется в Codex/Hermes |

Codex беречь (лимит ~18%) — только для крупных batch 5-10 пунктов или риска.

## AUTOPILOT

Лимит зелёных задач: **200** за проход (GREEN_SERIES_AUTOPILOT_200).

## ЗАПРЕЩЕНО

server, SSH, service, feature flag, .env, config.py, token, os.environ,
DB/logs/orders, реальные заказы, .py код, git, Phase 2, production.

## СЛЕДУЮЩИЙ ШАГ

Phase 2 dry-run prep — только после отдельного решения пользователя.
SSH/Phase 2 доступ требует отдельной проверки перед Phase 2.
```

## 2026-06-20 — BATCH_PHASE2_PREP_SSH_VERIFY_ROLLBACK

Status:

```text
PHASE2_DRY_RUN_PREP_READY_SSH_VERIFIED
```

Current verified state:

```text
server: hermes / 178.104.95.187
service: malyarka-telegram-bot.service
service state: active/running
autostart: disabled
process: /opt/malyarka-telegram-bot/.venv/bin/python -m malyarka_telegram.app --run-polling
Hermes adapter: installed
feature flag: _HERMES_ADAPTER_ENABLED = False
Telegram test: passed
production: OFF
Phase 2: OFF
SSH: verified read-only
```

Created/updated plan-only docs:

```text
E:\Hermes-Hub\docs\SERVER_SSH_ACCESS_CURRENT_STATUS.md
E:\Hermes-Hub\docs\HERMES_ADAPTER_PHASE2_DRY_RUN_PREP_AND_APPROVAL.md
E:\Hermes-Hub\docs\HERMES_ADAPTER_PHASE2_PRECHECK_CHECKLIST.md
E:\Hermes-Hub\docs\HERMES_ADAPTER_PHASE2_COMMAND_PLAN_ONLY.md
E:\Hermes-Hub\docs\HERMES_ADAPTER_PHASE2_TELEGRAM_TEST_PLAN.md
E:\Hermes-Hub\docs\HERMES_ADAPTER_PHASE2_ROLLBACK_PLAN.md
E:\Hermes-Hub\docs\HERMES_ADAPTER_PHASE2_REPORT_TEMPLATE.md
```

Approval phrase for any future Phase 2 dry-run:

```text
APPROVE_HERMES_ADAPTER_PHASE2_DRY_RUN_ONCE
```

Routing remains active:

- Codex is not used for micro tasks.
- Hermes / DeepSeek handles safe micro checks.
- Codex is reserved for complex/risky batch work.

No-touch: Phase 2 was not launched; feature flag was not changed; production remains OFF; no service start/restart/stop/enable/disable was performed; `.env`, `config.py`, token, `os.environ`, DB, live logs and real orders were not read; `.py` code was not changed; git was not used.


## 2026-06-20 — PHASE2_DRY_RUN_FAILED_ROLLBACK_DONE

Status:

```text
PHASE2_DRY_RUN_FAILED_ROLLBACK_DONE
```

Summary:

- Phase 2 dry-run was explicitly approved with `APPROVE_HERMES_ADAPTER_PHASE2_DRY_RUN_ONCE`.
- Precheck passed: SSH verified, service active/running, autostart disabled, feature flag OFF, adapter/hook present.
- Backup created: `/opt/malyarka-telegram-bot/malyarka_core/adapters/telegram.py.phase2_dry_run_backup_20260620`.
- Feature flag was temporarily set ON for controlled dry-run.
- Controlled restart was performed to apply temporary flag.
- Telegram test failed: `700 x 500` was diverted to English clarification (`What is 700 x 500 for?`) instead of expected Malyarka order flow.
- Rollback was executed immediately.
- Feature flag is now OFF.
- Controlled restart was performed to apply rollback.
- Final service state: active/running.
- Autostart remains disabled.
- Production remains OFF.

Created report:

```text
E:\Hermes-Hub\docs\HERMES_ADAPTER_PHASE2_DRY_RUN_REPORT.md
```

Blocker:

```text
Hermes adapter currently interferes incorrectly with simple order-like input `700 x 500`.
```

Next safe step:

```text
Plan-only investigation of adapter dry-run behavior before any future flag enable.
```

No-touch: no production enable, no systemctl enable/stop, no autostart change, no `.env`, `config.py`, token, `os.environ`, DB, live logs or real orders read, no adapter logic change, no git.

## 2026-06-20 — ORDER_LIKE_FALLBACK_LIVE_PATCH_APPLIED_SANITY_PASSED

Batch:

```text
BATCH_PHASE2_ORDER_LIKE_FALLBACK_APPLY_LIVE_PATCH_ONCE
```

Status:

```text
ORDER_LIKE_FALLBACK_LIVE_PATCH_APPLIED_SANITY_PASSED
```

Applied live patch:

```text
/opt/malyarka-telegram-bot/malyarka_core/adapters/hermes_adapter.py
```

Backup:

```text
/opt/malyarka-telegram-bot/malyarka_core/adapters/hermes_adapter.py.20260620_021040.before_order_like_fallback_patch
```

Final verified state:

```text
service: active/running
autostart: disabled
feature flag: OFF
production: OFF
Phase 2: OFF
patch guard: present
```

Sanity Telegram test:

- `/start` and `700 x 500` reported normal by user.
- Previous English clarification did not recur in reported sanity result.
- User noted: Malyarka file does not download. This is tracked as a separate export/callback blocker, not a rollback trigger for the order-like fallback patch.

Report:

```text
E:\Hermes-Hub\docs\HERMES_ADAPTER_ORDER_LIKE_FALLBACK_LIVE_PATCH_REPORT.md
```

Next safe batch:

```text
BATCH_MALYARKA_FILE_DOWNLOAD_READ_ONLY_INVESTIGATION
```

No-touch: feature flag was not enabled; Phase 2 was not launched; production was not enabled; `telegram.py` was not changed; secrets/DB/logs/orders were not read; git was not used.
