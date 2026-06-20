# Next Batch Queue

Date: 2026-06-20

## Next Possible Batch

```text
BATCH_HERMES_ADAPTER_PHASE2_DRY_RUN_PREP_AND_APPROVAL
```

Do not execute Phase 2 in this batch.

## Proposed Contents

- Phase 2 dry-run plan.
- Feature flag short enable plan.
- Telegram test plan.
- Forced flag OFF rollback plan.
- No production rule.
- Approval gate.

## Required Future Approval Phrase

```text
APPROVE_HERMES_ADAPTER_PHASE2_DRY_RUN_ONCE
```

## Other Possible Batch

```text
BATCH_SERVER_BOT_CONTROLLED_STOP_ONCE
```

Requires:

```text
APPROVE_SERVER_BOT_CONTROLLED_STOP_ONCE
```

## Workflow Infrastructure Batch

```text
BATCH_SCRIPT_LAUNCHER_WORKFLOW
```

Purpose:

- implement or update user-facing launcher scripts;
- avoid long manual CMD/PowerShell one-liners;
- preserve ZIP package flow for big context;
- generate `CODEX_PROMPT.txt` automatically.

Current rule status:

```text
SCRIPT_LAUNCHER_WORKFLOW_RULE_READY
```

## 2026-06-20 вЂ” SIMPLE_CHATGPT_TO_CODEX_PROMPT_WORKFLOW_RESTORED

Active status:

```text
SIMPLE_CHATGPT_TO_CODEX_PROMPT_WORKFLOW_RESTORED
```

Active workflow:

1. Main task transfer to Codex is prompt text directly in ChatGPT.
2. ZIP / launcher / HERMES_PACKET_INBOX / LATEST_TASK_PATH are not used by default.
3. Launcher scripts are no longer the main workflow.
4. HERMES_PACKET_INBOX is no longer the main workflow.
5. Long user-facing CMD/PowerShell one-liners are not the main workflow.
6. If large context is needed, first agree on a simple file/ZIP separately, but still provide the prompt text in ChatGPT.
7. Always additionally provide the prompt text in ChatGPT.

Superseded / not active by default:

- NO_MANUAL_CMD_ONE_LINERS_FOR_PACKET_WORKFLOW
- SCRIPT_LAUNCHER_WORKFLOW_RULE_READY
- HERMES_PACKET_INBOX as default workflow

Still active:

- E:\Hermes-Hub\sync
- Codex/Hermes/ChatGPT sync through markdown files
- Micro tasks -> Hermes / cheap agent
- Big batch -> Codex
- Shared state -> markdown sync/state/handoff files

No-touch: server, SSH, service, Telegram runtime, feature flag, secrets, DB/logs/orders, `.py` code, git, Phase 2 and production were not touched.

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

Reason:

```text
MALYARKA_FILE_RUSSIAN_EXPORT_HEADERS_FIX_BLOCKED
```

Scope:

- Read-only first.
- Determine why Telegram `download_malyarka_file` does not send the file after Russian-header patch.
- Compare direct export success vs callback/file delivery failure.
- Check generated filename/path/MIME/send_document/exception handling without reading secrets, DB, live logs, or real orders.

Do not:

- change `.py` code until a new fix plan is approved;
- change feature flag;
- launch Phase 2;
- enable production;
- read `.env`, `config.py`, token, `os.environ`, DB, logs, or real orders;
- use git commit/push.

## Next — BATCH_MALYARKA_FILE_RUSSIAN_EXPORT_HEADERS_RETEST_WITH_FRESH_PREVIEW_PLAN

Reason:

```text
MALYARKA_FILE_RUSSIAN_EXPORT_CALLBACK_FAILURE_INVESTIGATION_READY
```

Goal:

Prepare a controlled retest plan for the Russian-header export patch where the user creates a fresh order preview after any service restart before pressing `Скачать Файл Малярки`.

Key rule:

```text
Do not press old pre-restart export buttons.
```

Why:

The current export callback depends on `_RUNTIME_COREL_ROWS`, which is in-memory and is cleared by service restart.

## Next — BATCH_MALYARKA_FILE_RUSSIAN_EXPORT_CODE_REVIEW_AND_SECOND_PATH_INVESTIGATION

Reason:

```text
MALYARKA_FILE_RUSSIAN_EXPORT_HEADERS_FIX_NEEDS_CODE_REVIEW
```

Scope:

- read-only/code-review first;
- find exact export path used by Telegram for `Файл Малярки`;
- check whether there is a second export file/function/path;
- verify whether patch target should be `malyarka_core/exports/malyarka_file.py`, `malyarka_core/exports/malyarka.py`, or another path;
- do not change feature flag, Phase 2, production, secrets, DB, logs, real orders, or adapter logic.

## Next — BATCH_MALYARKA_FILE_RUSSIAN_EXPORT_SECOND_PATH_FIX

Reason:

```text
MALYARKA_FILE_RUSSIAN_EXPORT_SECOND_PATH_INVESTIGATION_READY
```

Scope:

- Patch the actual live export path: `malyarka_core/exports/malyarka_file.py`.
- Backup first.
- Apply tested Russian-header/status candidate.
- Run `py_compile` and direct dummy export.
- Restart only if needed.
- Telegram retest must use a fresh order preview and a newly generated button.

Important finding:

The previous fresh retest used rolled-back live code, so English headers were expected.

## Cleared — BATCH_MALYARKA_FILE_RUSSIAN_EXPORT_SECOND_PATH_FIX

Completed as:

```text
MALYARKA_FILE_RUSSIAN_EXPORT_REAPPLY_PASSED
```

The Russian Malyarka File export blocker is closed. Next batch should be selected by the user from the broader project queue; do not proceed into Phase 2 or production without explicit approval.
