# Sync Done Log

Date: 2026-06-20

## Done

- `HERMES_PACKET_INBOX` installed.
- Runtime reconciliation documented.
- Controlled startup gated plan created.
- Controlled start performed after approval.
- Telegram phone test passed.
- Post-start stabilization documented.
- Codex/Hermes sync layer created.

## Current Status

```text
CODEX_HERMES_SYNC_LAYER_READY
```


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
## 2026-06-20 — Russian Malyarka File export patch attempted and rolled back

Status:

```text
MALYARKA_FILE_RUSSIAN_EXPORT_HEADERS_FIX_BLOCKED
```

Summary:

- Local candidate/test passed.
- Live patch was applied once to `malyarka_file.py`.
- Backup was created at `/opt/malyarka-telegram-bot/malyarka_core/exports/malyarka_file.py.20260620_075550.before_russian_headers`.
- Telegram sanity failed: file did not download.
- Rollback was performed from backup.
- Final state: service active/running, autostart disabled, feature flag OFF, production OFF, Phase 2 OFF.

## 2026-06-20 — Fresh Malyarka File export retest completed

Status:

```text
MALYARKA_FILE_RUSSIAN_EXPORT_HEADERS_FIX_NEEDS_CODE_REVIEW
```

Result:

- Fresh order preview was created.
- New `Скачать Файл Малярки` button was pressed.
- File downloaded successfully.
- Headers/statuses are still English technical fields.

Conclusion:

- Download path works.
- Old pre-restart button is not the cause.
- `openpyxl` is not the cause.
- Code review is needed to find whether live Telegram uses a second export path or an unpatched file.

## 2026-06-20 — Malyarka File Russian export reapply passed

Status:

```text
MALYARKA_FILE_RUSSIAN_EXPORT_REAPPLY_PASSED
```

Result:

- Reapplied Russian export patch to actual path.
- Backup: `/opt/malyarka-telegram-bot/malyarka_core/exports/malyarka_file.py.20260620_083303.before_russian_headers_reapply`.
- Checks passed locally and on server.
- Fresh Telegram test passed.
- File downloads with Russian headers/statuses.
- Forbidden English technical fields are absent.
- Rollback was not needed.
