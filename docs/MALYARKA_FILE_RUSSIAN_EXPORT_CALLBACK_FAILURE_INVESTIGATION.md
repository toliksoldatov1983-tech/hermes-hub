# MALYARKA_FILE_RUSSIAN_EXPORT_CALLBACK_FAILURE_INVESTIGATION

Date: 2026-06-20

Batch:

```text
BATCH_MALYARKA_FILE_RUSSIAN_EXPORT_CALLBACK_FAILURE_INVESTIGATION
```

Status:

```text
MALYARKA_FILE_RUSSIAN_EXPORT_CALLBACK_FAILURE_INVESTIGATION_READY
```

## Context

The previous batch attempted to translate `Файл Малярки` Excel headers/statuses to Russian.

Observed result:

- local pytest passed;
- local `py_compile` passed;
- live patch was applied once;
- server-side dummy export created `.xlsx`;
- controlled service restart was performed;
- Telegram sanity reported: file did not download;
- patch was rolled back from backup.

Rollback backup:

```text
/opt/malyarka-telegram-bot/malyarka_core/exports/malyarka_file.py.20260620_075550.before_russian_headers
```

Final runtime after rollback:

```text
service: active/running
autostart: disabled
Hermes adapter feature flag: OFF
production: OFF
Phase 2: OFF
```

## Read-Only Code Findings

Button:

```text
MALYARKA_FILE_ACTION = "download_malyarka_file"
label = "Скачать Файл Малярки"
```

Callback registration:

```text
dispatcher.callback_query(lambda callback: callback.data == MALYARKA_FILE_ACTION)
```

Handler:

```text
handle_malyarka_file_callback(...)
```

Preparation function:

```text
prepare_malyarka_file_for_user(...)
```

Export function:

```text
malyarka_core.exports.malyarka_file.export_malyarka_file_xlsx(...)
```

Telegram send path:

```text
message.answer_document(_build_telegram_document(prepared.path), caption="Файл Малярки")
```

## Most Likely Cause

The live callback depends on in-memory rows:

```text
_RUNTIME_COREL_ROWS
```

`prepare_malyarka_file_for_user(...)` reads:

```text
rows = _RUNTIME_COREL_ROWS.get(user_id)
```

If rows are absent, it raises:

```text
Нет подготовленного чистого заказа для Файла Малярки.
```

The Russian-header patch required a controlled service restart because the export module could already be imported in the live process. That restart clears process memory, including `_RUNTIME_COREL_ROWS`.

Therefore, pressing an old pre-restart `Скачать Файл Малярки` button after restart can fail even if the export function itself is correct.

This explains the contradiction:

- direct server dummy export succeeded;
- Telegram callback did not download after restart.

## Secondary Risks

1. The handler catches `ValueError` from preparation, but not generic send/export exceptions around `answer_document`.
2. The current callback flow has no durable order snapshot; export buttons depend on process memory.
3. Restarting service between preview generation and file download invalidates the export buttons.
4. The previous sanity procedure may not have guaranteed a fresh post-restart order preview before pressing `Скачать Файл Малярки`.

## What Was Not Checked

The investigation did not read:

- `.env`;
- `config.py`;
- token;
- `os.environ`;
- databases;
- live logs;
- real orders.

No code was changed.

## Recommended Next Safe Batch

```text
BATCH_MALYARKA_FILE_RUSSIAN_EXPORT_HEADERS_RETEST_WITH_FRESH_PREVIEW_PLAN
```

Purpose:

Plan a second Russian-header patch attempt only if the test procedure first regenerates a fresh order preview after any service restart.

Required test sequence:

1. Apply patch from a tested candidate.
2. Restart service only if required.
3. After restart, user must create a new clean order preview:
   - `/start`
   - `Новый заказ`
   - `700 x 500`
4. Press the new `Скачать Файл Малярки` button from that fresh preview.
5. Verify:
   - file downloads;
   - headers are Russian;
   - English technical headers are absent.

## Future Fix Options

If fresh-preview retest still fails, prepare a separate code fix plan for:

- better callback exception reporting without leaking secrets;
- local callback-level tests for `handle_malyarka_file_callback`;
- optionally storing export-ready rows in a safer short-lived order context instead of relying only on `_RUNTIME_COREL_ROWS`.

## No-Touch Confirmation

- Server files were not modified.
- Service was not restarted/stopped/started/enabled in this investigation.
- Hermes adapter feature flag was not changed.
- Phase 2 was not launched.
- Production was not enabled.
- `.env`, `config.py`, token, `os.environ`, DB, live logs, and real orders were not read.
- Git commit/push was not used.

## Fresh Preview Retest Result

User performed a fresh Telegram test with a new order preview after the rollback/investigation:

```text
fresh preview: yes
new button pressed: yes
file downloaded: yes
headers: English
```

Observed English technical fields in the newly downloaded Excel:

- `row_number` / `row_num`
- `height`
- `width`
- `quantity`
- `item_area`
- `row_area`
- `row_status` / `row_statu`
- `raw_text`
- `dispute_reason`
- `TOTAL_CONFIRMED`
- `confirmed`
- `confirmed_total`

Conclusion:

```text
MALYARKA_FILE_RUSSIAN_EXPORT_HEADERS_FIX_NEEDS_CODE_REVIEW
```

The problem is not the old pre-restart button and not `openpyxl`. The file downloads from a fresh callback, but live export still produces English headers/statuses. Either the previous patch was applied to the wrong export path, or there is a second export path used by Telegram.

Next safe batch:

```text
BATCH_MALYARKA_FILE_RUSSIAN_EXPORT_CODE_REVIEW_AND_SECOND_PATH_INVESTIGATION
```
