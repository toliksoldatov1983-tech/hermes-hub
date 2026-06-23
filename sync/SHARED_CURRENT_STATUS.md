# Shared Current Status вЂ” Codex / Hermes Sync

Date: 2026-06-20

## Runtime

| Item | Status |
|------|--------|
| Server | hermes (178.104.95.187) |
| Bot | active/running |
| Service | malyarka-telegram-bot |
| Autostart | disabled |
| Feature flag | OFF |
| Adapter | installed, tested |
| Production | NOT enabled |
| Phase 2 | NOT started |

## Routing Rule

- Micro в†’ Hermes/DeepSeek
- Batch (5-10 items) в†’ Codex
- Decisions в†’ User + ChatGPT
- Prompt workflow: text in ChatGPT в†’ copy to Codex/Hermes
- Codex limit: ~18%, use only for large batch or risk

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

## 2026-06-20 — MALYARKA_FILE_DOWNLOAD_FIX_DEPENDENCY_INSTALLED_TEST_PASSED

Batch:

```text
APPROVE_MALYARKA_FILE_DOWNLOAD_FIX_ONCE
```

Status:

```text
MALYARKA_FILE_DOWNLOAD_FIX_DEPENDENCY_INSTALLED_TEST_PASSED
```

Result:

- Backup created: `/opt/malyarka-telegram-bot/requirements.txt.20260620_024027.before_openpyxl`.
- `openpyxl` added to server `requirements.txt`.
- `openpyxl` installed into server `.venv`.
- Installed version: `3.1.5`.
- Service restart was not performed.
- User Telegram sanity test passed: `Файл Малярки` now downloads.

New separate blocker:

```text
MALYARKA_FILE_EXPORT_USES_ENGLISH_HEADERS_AND_STATUSES
```

This is not a failure of the dependency fix. The downloaded file contains English headers/statuses and needs a separate export-format batch.

Report:

```text
E:\Hermes-Hub\docs\MALYARKA_FILE_DOWNLOAD_FIX_REPORT.md
```

Next safe batch:

```text
BATCH_MALYARKA_FILE_RUSSIAN_EXPORT_HEADERS_FIX
```

No-touch: `.py` code was not changed; feature flag was not changed; Phase 2 was not launched; production was not enabled; secrets/DB/logs/orders were not read; git was not used.

## 2026-06-20 — MALYARKA_FILE_RUSSIAN_EXPORT_HEADERS_FIX_BLOCKED

Batch:

```text
BATCH_MALYARKA_FILE_RUSSIAN_EXPORT_HEADERS_FIX
```

Status:

```text
MALYARKA_FILE_RUSSIAN_EXPORT_HEADERS_FIX_BLOCKED
```

Result:

- Local Russian-header candidate and test were created.
- Local checks passed: `1 passed`, `py_compile` passed.
- Live `malyarka_file.py` was backed up and patched once.
- Backup path: `/opt/malyarka-telegram-bot/malyarka_core/exports/malyarka_file.py.20260620_075550.before_russian_headers`.
- Server-side safe dummy export created an `.xlsx`.
- User Telegram sanity reported: `Файл Малярки` did not download.
- Rollback was performed immediately from the backup.

Final verified state after rollback:

```text
service: active/running
autostart: disabled
feature flag: OFF
production: OFF
Phase 2: OFF
```

Open blocker:

```text
MALYARKA_FILE_RUSSIAN_EXPORT_HEADERS_FIX_BLOCKED
```

Next safe batch:

```text
BATCH_MALYARKA_FILE_RUSSIAN_EXPORT_CALLBACK_FAILURE_INVESTIGATION
```

No-touch: feature flag was not changed; Phase 2 was not launched; production was not enabled; secrets/DB/logs/orders were not read; adapter logic was not changed; git was not used.

## 2026-06-20 — MALYARKA_FILE_RUSSIAN_EXPORT_HEADERS_FIX_NEEDS_CODE_REVIEW

Fresh Telegram retest:

```text
fresh preview: yes
new button pressed: yes
file downloaded: yes
headers: English
```

Conclusion:

```text
MALYARKA_FILE_RUSSIAN_EXPORT_HEADERS_FIX_NEEDS_CODE_REVIEW
```

The file download dependency/callback works, but the newly downloaded Excel still contains English technical headers/statuses. The problem is not the old button and not `openpyxl`.

Likely directions:

- patch was applied to a file/path not used by the live callback;
- another export path exists;
- there is another Malyarka export function/file producing the downloaded workbook.

Next safe batch:

```text
BATCH_MALYARKA_FILE_RUSSIAN_EXPORT_CODE_REVIEW_AND_SECOND_PATH_INVESTIGATION
```

## 2026-06-20 — MALYARKA_FILE_RUSSIAN_EXPORT_REAPPLY_PASSED

Status:

```text
MALYARKA_FILE_RUSSIAN_EXPORT_REAPPLY_PASSED
```

Result:

- Actual live export path was patched: `/opt/malyarka-telegram-bot/malyarka_core/exports/malyarka_file.py`.
- Backup created: `/opt/malyarka-telegram-bot/malyarka_core/exports/malyarka_file.py.20260620_083303.before_russian_headers_reapply`.
- Local pytest passed: `1 passed`.
- Local and server `py_compile` passed.
- Server dummy workbook check passed: Russian values present, forbidden English values absent.
- Controlled service restart was performed.
- Fresh Telegram test passed: file downloaded with Russian headers/statuses.

Final runtime:

```text
service: active/running
autostart: disabled
feature flag: OFF
Phase 2: OFF
production: OFF
rollback: not needed
```
## 2026-06-23 — TELEGRAM_ORDER_PREVIEW_LOOP_AND_BUTTONS_FIX_CONFIRMED

Runtime:

| Item | Status |
|------|--------|
| Server | hermes (178.104.95.187) |
| Bot | active/running |
| Service | malyarka-telegram-bot.service |
| Local clean runtime | `E:\Hermes-Hub\projects\malyarka-runtime-clean` |
| Live runtime | `/opt/malyarka-telegram-bot` |
| Tests | `441 passed` |
| Order-like neutral input | parses immediately |
| Extra three-button keyboard | removed from fallback |
| User sanity | preview confirmed OK |

Important rule:

```text
Normal order text must go straight to preview. Do not reintroduce /заказ gating or generic mode buttons for obvious size input.
```
