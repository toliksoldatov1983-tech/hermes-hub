# Next Tasks

Date: 2026-06-21
Status: MASTER_MAP_LEVELS_1_10_COMPLETED

## TOP-10 ближайших задач (Hermes markdown-only)

| # | Задача | Файл |
|---|--------|------|
| 1 | Regression checklist | `docs/REGRESSION_CHECKLIST.md` |
| 2 | Единый WHAT_NEXT | `WHAT_NEXT.md` |
| 3 | Единый TASK_QUEUE | `TASK_QUEUE.md` |
| 4 | SYNC_CHECKLIST | `docs/SYNC_CHECKLIST.md` |
| 5 | Telegram safe commands | `docs/TELEGRAM_SAFE_COMMANDS.md` |
| 6 | Telegram approval flow | `docs/TELEGRAM_APPROVAL_FLOW.md` |
| 7 | Health check дизайн | `docs/HEALTH_CHECK_DESIGN.md` |
| 8 | Commit policy | `docs/COMMIT_POLICY.md` |
| 9 | Obsidian long memory rules | `docs/OBSIDIAN_LONG_MEMORY_RULES.md` |
| 10 | Obsidian short memory rules | `docs/OBSIDIAN_SHORT_MEMORY_RULES.md` |

## User decisions needed

| # | Вопрос |
|---|--------|
| D1 | Нужен ли GitHub? |
| D2 | Autostart или ручной controlled start? |
| D3 | Нужна ли экономика сейчас? |
| D4 | Альтернатива для Vision? |

## Codex batch queue

| # | Batch | Status |
|---|-------|--------|
| P13 | BATCH_014: Malyarka Clean Core | Ready |
| P14 | BATCH_015: Agent Implementation | Ready |
| P15 | BATCH_010: Phase 2 Dry-Run Retry | Blocked |
| P16 | BATCH_012: Export Regression Tests | Ready |
| P17 | BATCH_016: Old Archive Review | Ready |
| P18 | BATCH_013: GitHub Setup | Needs D1 |

## Current Status

- Bot: active/running, autostart disabled
- Feature flag: OFF
- Production: NOT enabled
- Phase 2: NOT started
- Server gates 1-9: completed
- SSH/Phase 2 access: requires separate verification

## Routing

| Р—РѕРЅР° | РљРѕРјСѓ |
|------|------|
| Micro checks, read-only | Hermes / DeepSeek |
| Code, tests, multi-file | Codex (batch, 5-10 РїСѓРЅРєС‚РѕРІ) |
| Decisions | РџРѕР»СЊР·РѕРІР°С‚РµР»СЊ + ChatGPT |
| Prompt workflow | РўРµРєСЃС‚ РІ ChatGPT в†’ РєРѕРїРёСЏ РІ Codex/Hermes |

## Next Steps

1. Markdown cleanup вЂ” done вњ…
2. Phase 2 dry-run prep вЂ” requires separate user decision
3. Server SSH diagnostic вЂ” if Phase 2 is chosen

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

## 2026-06-20 — PHASE2_FAILURE_INVESTIGATION_READY

Status:

```text
PHASE2_FAILURE_INVESTIGATION_READY
```

Source failure:

```text
PHASE2_DRY_RUN_FAILED_ROLLBACK_DONE
```

Finding:

`700 x 500` is order-like production-size input and must remain under Malyarka order flow. During Phase 2 dry-run the Hermes adapter diverted it to generic English clarification (`What is 700 x 500 for?`), so Phase 2 remains blocked.

Likely failure point:

```text
malyarka_core/adapters/telegram.py / malyarka_core/adapters/hermes_adapter.py boundary
```

Expected rule:

- order-like input -> adapter returns `fallback_required=true`;
- existing Telegram router/parser handles order flow;
- adapter must not replace parser in order mode;
- no generic English clarification for dimensions.

Investigation report:

```text
E:\Hermes-Hub\docs\HERMES_ADAPTER_PHASE2_FAILURE_INVESTIGATION.md
```

Next safe Codex batch:

```text
BATCH_PHASE2_ADAPTER_ORDER_LIKE_FALLBACK_FIX_PLAN
```

No-touch: no server/SSH/service/feature flag/Phase 2 runtime, no secrets/DB/logs/orders, no `.py` changes, no git.

## 2026-06-20 — ORDER_LIKE_FALLBACK_FIX_PLAN_ONLY

Batch:

```text
BATCH_PHASE2_ADAPTER_ORDER_LIKE_FALLBACK_FIX
```

Status:

```text
ORDER_LIKE_FALLBACK_FIX_PLAN_ONLY
```

Reason:

Safe local copies of the real adapter boundary files were not found:

```text
malyarka_core/adapters/telegram.py
malyarka_core/adapters/hermes_adapter.py
```

Only markdown draft/report mentions and local test doubles were available. Because server/SSH/service/feature flag/Phase 2 runtime were forbidden, no `.py` fix was applied.

Created/updated:

```text
E:\Hermes-Hub\docs\HERMES_ADAPTER_ORDER_LIKE_FALLBACK_FIX_REPORT.md
E:\Hermes-Hub\docs\HERMES_ADAPTER_PHASE2_FAILURE_INVESTIGATION.md
```

Next safe batch:

```text
BATCH_PHASE2_FETCH_OR_CREATE_LOCAL_ADAPTER_BOUNDARY_COPY_AND_TEST_PLAN
```

No-touch: server, SSH, service, feature flag, Phase 2, production, secrets, DB/logs/orders, real adapter code, Telegram live test and git were not touched.

## 2026-06-20 — ADAPTER_BOUNDARY_SNAPSHOT_READY

Batch:

```text
BATCH_PHASE2_FETCH_LOCAL_ADAPTER_BOUNDARY_COPY_AND_TEST_PLAN
```

Status:

```text
ADAPTER_BOUNDARY_SNAPSHOT_READY
```

Copied read-only from server:

```text
/opt/malyarka-telegram-bot/malyarka_core/adapters/telegram.py
/opt/malyarka-telegram-bot/malyarka_core/adapters/hermes_adapter.py
```

Saved locally as non-live snapshot:

```text
E:\Hermes-Hub\server_staging\adapter_boundary_snapshot\telegram.py
E:\Hermes-Hub\server_staging\adapter_boundary_snapshot\hermes_adapter.py
E:\Hermes-Hub\server_staging\adapter_boundary_snapshot\SNAPSHOT_MANIFEST.md
```

Created plans:

```text
E:\Hermes-Hub\docs\HERMES_ADAPTER_ORDER_LIKE_FALLBACK_LOCAL_FIX_PLAN.md
E:\Hermes-Hub\docs\HERMES_ADAPTER_ORDER_LIKE_FALLBACK_CONTRACT_TEST_PLAN.md
```

Next safe batch:

```text
BATCH_PHASE2_ORDER_LIKE_FALLBACK_LOCAL_FIX_AND_TESTS
```

No-touch: server files were not modified; service/systemctl/feature flag/Phase 2/production were not touched; secrets/DB/logs/orders were not read; live Telegram test and git were not used.

## 2026-06-20 — ORDER_LIKE_FALLBACK_FIX_CANDIDATE_TESTS_PASSED

Batch:

```text
BATCH_PHASE2_ORDER_LIKE_FALLBACK_LOCAL_FIX_AND_TESTS
```

Status:

```text
ORDER_LIKE_FALLBACK_FIX_CANDIDATE_TESTS_PASSED
```

Created fix-candidate:

```text
E:\Hermes-Hub\server_staging\adapter_boundary_fix_candidate\telegram.py
E:\Hermes-Hub\server_staging\adapter_boundary_fix_candidate\hermes_adapter.py
```

Changed locally only:

```text
E:\Hermes-Hub\server_staging\adapter_boundary_fix_candidate\hermes_adapter.py
```

Created tests:

```text
E:\Hermes-Hub\server_staging\adapter_boundary_tests\test_order_like_fallback.py
```

Checks:

```text
python -m pytest server_staging\adapter_boundary_tests -q -> 10 passed
python -m py_compile fix-candidate files -> exit 0
```

Report:

```text
E:\Hermes-Hub\docs\HERMES_ADAPTER_ORDER_LIKE_FALLBACK_LOCAL_FIX_AND_TESTS_REPORT.md
```

Next safe batch:

```text
BATCH_PHASE2_ORDER_LIKE_FALLBACK_LIVE_PATCH_PLAN
```

No-touch: server, SSH, service, live feature flag, Phase 2, production, secrets, DB/logs/orders, live server files, live Telegram test and git were not touched.

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

## 2026-06-20 — MALYARKA_FILE_DOWNLOAD_INVESTIGATION_READY

Batch:

```text
BATCH_MALYARKA_FILE_DOWNLOAD_READ_ONLY_INVESTIGATION
```

Status:

```text
MALYARKA_FILE_DOWNLOAD_INVESTIGATION_READY
```

Finding:

`Скачать Файл Малярки` uses callback action `download_malyarka_file`, handler `handle_malyarka_file_callback(...)`, and export function `malyarka_core.exports.malyarka_file.export_malyarka_file_xlsx(...)`.

Most likely failure point:

```text
malyarka_core.exports.malyarka_file.export_malyarka_file_xlsx(...)
```

Reason:

Corel export writes xlsx via Python standard library `zipfile`; Malyarka File export imports `openpyxl`. Server `requirements.txt` check showed `aiogram>=3,<4` and did not show `openpyxl`, so missing dependency is a likely cause.

Report:

```text
E:\Hermes-Hub\docs\MALYARKA_FILE_DOWNLOAD_FAILURE_INVESTIGATION.md
```

Next safe batch:

```text
BATCH_MALYARKA_FILE_DOWNLOAD_FIX_PLAN
```

No-touch: no code changes, no server file changes, no service/systemctl changes, no feature flag/Phase 2/production, no secrets/DB/logs/orders, no live Telegram test, no git.

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

## Next — BATCH_MALYARKA_FILE_RUSSIAN_EXPORT_CALLBACK_FAILURE_INVESTIGATION

Context:

```text
MALYARKA_FILE_RUSSIAN_EXPORT_HEADERS_FIX_BLOCKED
```

Goal:

Investigate why Telegram `Файл Малярки` did not download after the Russian-header live patch, even though local tests and server-side dummy export passed.

Constraints:

- read-only first;
- no secrets/DB/logs/orders;
- no feature flag/Phase 2/production;
- no adapter logic changes;
- no git.

## Next — BATCH_MALYARKA_FILE_RUSSIAN_EXPORT_HEADERS_RETEST_WITH_FRESH_PREVIEW_PLAN

Prepare a controlled plan to reattempt the Russian-header export patch with a corrected Telegram sanity procedure:

1. apply tested candidate;
2. restart only if required;
3. create a fresh order preview after restart;
4. press the new `Скачать Файл Малярки` button;
5. verify Russian headers and no English technical fields.

Reason:

`_RUNTIME_COREL_ROWS` is in-memory and old export buttons become invalid after service restart.

## Next — BATCH_MALYARKA_FILE_RUSSIAN_EXPORT_CODE_REVIEW_AND_SECOND_PATH_INVESTIGATION

Fresh retest result:

```text
fresh preview: yes
new button pressed: yes
file downloaded: yes
headers: English
```

Task:

Perform read-only/code-review investigation to locate the exact live export path that creates the downloaded Malyarka File workbook.

Do not:

- change code;
- change feature flag;
- launch Phase 2;
- enable production;
- read secrets/DB/logs/orders;
- use git.

## Next — BATCH_MALYARKA_FILE_RUSSIAN_EXPORT_SECOND_PATH_FIX

Objective:

Apply a controlled fix to the actual export path:

```text
malyarka_core/exports/malyarka_file.py
```

Reason:

Read-only investigation found no second path. The previous fresh retest showed English headers because the Russian patch had already been rolled back.

Required:

- backup live file;
- apply tested candidate;
- verify Russian headers/statuses;
- fresh Telegram preview after any restart.

## Completed — Malyarka File Russian export

Status:

```text
MALYARKA_FILE_RUSSIAN_EXPORT_REAPPLY_PASSED
```

The blocker is closed. Do not continue to Phase 2 or production without explicit user approval. Next safe task should be selected separately.

## Next — Hermes Master Map Level 1

Status:

```text
HERMES_HUB_RECONNECT_READY
```

Task:

Use Hermes as dispatcher to build the master project map.

Read:

```text
E:\Hermes-General\HERMES_OPERATING_SYSTEM.md
E:\Hermes-General\START_HERE_FOR_HERMES_HUB_MALYARKA.md
E:\Hermes-Hub\PROJECT_MASTER_MAP_MALYARKA_HERMES.md
E:\Hermes-Hub\docs\HERMES_MASTER_MAP_LEVELS_AND_PROMPTS.md
```

First level:

```text
LEVEL 1 — Inventory sources
```

No code, no server, no secrets, no git.
