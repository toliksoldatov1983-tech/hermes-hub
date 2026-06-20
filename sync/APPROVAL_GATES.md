# Approval Gates

Date: 2026-06-20

## Used Approval

```text
APPROVE_SERVER_BOT_CONTROLLED_START_ONCE
```

Meaning:

- one-time controlled start of `malyarka-telegram-bot.service`;
- already used;
- start succeeded;
- Telegram test passed.

## Future Approval

```text
APPROVE_SERVER_BOT_CONTROLLED_STOP_ONCE
```

Meaning:

- future one-time controlled stop;
- not used yet.

## Future Approval

```text
APPROVE_HERMES_ADAPTER_PHASE2_DRY_RUN_ONCE
```

Meaning:

- future Hermes adapter Phase 2 dry-run;
- not used yet;
- does not imply production.

## Non-Approval

The following are not enough for live/server actions:

```text
РґР°
+
РїСЂРѕРґРѕР»Р¶Р°Р№
РґРµР»Р°Р№ РґР°Р»СЊС€Рµ
РјРѕР¶РЅРѕ
```


## 2026-06-20 вЂ” BATCH_PHASE2_PREP_SSH_VERIFY_ROLLBACK

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


## 2026-06-20 — ORDER_LIKE_FALLBACK_LIVE_PATCH_PLAN_READY

Batch:

```text
BATCH_PHASE2_ORDER_LIKE_FALLBACK_LIVE_PATCH_PLAN
```

Status:

```text
ORDER_LIKE_FALLBACK_LIVE_PATCH_PLAN_READY
```

Created plan docs:

```text
E:\Hermes-Hub\docs\HERMES_ADAPTER_ORDER_LIKE_FALLBACK_LIVE_PATCH_PLAN.md
E:\Hermes-Hub\docs\HERMES_ADAPTER_ORDER_LIKE_FALLBACK_LIVE_PATCH_ROLLBACK_PLAN.md
E:\Hermes-Hub\docs\HERMES_ADAPTER_ORDER_LIKE_FALLBACK_LIVE_PATCH_PRECHECK.md
E:\Hermes-Hub\docs\HERMES_ADAPTER_ORDER_LIKE_FALLBACK_LIVE_PATCH_TEST_PLAN.md
```

Diff summary:

- `hermes_adapter.py` only.
- Added `re` import.
- Added order-like regex guard.
- `700 x 500` / `700х500` / `700 × 500` / `700*500` / `700 x 500 x 2` fallback to old Malyarka flow.
- `/start` falls back to existing router/menu flow.
- Safe generic text remains allowed.

Future approval phrase:

```text
APPROVE_ORDER_LIKE_FALLBACK_LIVE_PATCH_ONCE
```

Next live patch batch after approval:

```text
BATCH_PHASE2_ORDER_LIKE_FALLBACK_APPLY_LIVE_PATCH_ONCE
```

No-touch: server/SSH/systemctl/live files/feature flag/Phase 2/production/secrets/DB/logs/orders/live Telegram/git were not touched.

## 2026-06-20 — MALYARKA_FILE_DOWNLOAD_FIX_PLAN_READY_DEPENDENCY_MISSING

Batch:

```text
BATCH_MALYARKA_FILE_DOWNLOAD_FIX_PLAN
```

Status:

```text
MALYARKA_FILE_DOWNLOAD_FIX_PLAN_READY_DEPENDENCY_MISSING
```

Read-only checks:

- `openpyxl` import in server `.venv`: failed with `ModuleNotFoundError`.
- `openpyxl` in `requirements.txt`: not found.
- `openpyxl` imports found in:
  - `malyarka_core/exports/malyarka.py`;
  - `malyarka_core/exports/malyarka_file.py`.

Likely cause:

`Скачать Файл Малярки` requires `openpyxl`, but it is missing from `.venv` and not declared in requirements. Corel export can work because it uses standard-library `zipfile`.

Plan doc:

```text
E:\Hermes-Hub\docs\MALYARKA_FILE_DOWNLOAD_FIX_PLAN.md
```

Future approval phrase:

```text
APPROVE_MALYARKA_FILE_DOWNLOAD_FIX_ONCE
```

No-touch: no dependency install, no requirements change, no `.py` change, no service/systemctl, no feature flag/Phase 2/production, no secrets/DB/logs/orders, no live Telegram test, no git.
