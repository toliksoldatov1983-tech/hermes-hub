# MALYARKA_FILE_RUSSIAN_EXPORT_SECOND_PATH_INVESTIGATION

Date: 2026-06-20

Batch:

```text
BATCH_MALYARKA_FILE_RUSSIAN_EXPORT_CODE_REVIEW_AND_SECOND_PATH_INVESTIGATION
```

Status:

```text
MALYARKA_FILE_RUSSIAN_EXPORT_SECOND_PATH_INVESTIGATION_READY
```

## Current Context

Fresh Telegram retest result:

```text
fresh preview: yes
new button pressed: yes
file downloaded: yes
headers: English
```

Conclusion before this investigation:

```text
MALYARKA_FILE_RUSSIAN_EXPORT_HEADERS_FIX_NEEDS_CODE_REVIEW
```

## Actual Callback Path

Button action:

```text
malyarka_telegram/keyboards.py
MALYARKA_FILE_ACTION = "download_malyarka_file"
```

Button label:

```text
Скачать Файл Малярки
```

Callback registration:

```text
malyarka_telegram/app.py
dispatcher.callback_query(lambda callback: callback.data == MALYARKA_FILE_ACTION)
```

Callback handler:

```text
malyarka_telegram/app.py
handle_malyarka_file_callback(...)
```

Preparation function:

```text
malyarka_telegram/app.py
prepare_malyarka_file_for_user(...)
```

Actual export import:

```text
from malyarka_core.exports.malyarka_file import export_malyarka_file_xlsx
```

Actual export call:

```text
export_malyarka_file_xlsx(order, output_path)
```

Actual live export path:

```text
/opt/malyarka-telegram-bot/malyarka_core/exports/malyarka_file.py
```

## Where English Fields Are Now

Read-only grep found the English technical fields in:

```text
/opt/malyarka-telegram-bot/malyarka_core/exports/malyarka_file.py
```

Current live file contains:

```text
MALYARKA_FILE_HEADERS = [
    "row_number",
    "height",
    "width",
    "quantity",
    "item_area_m2",
    "row_area_m2",
    "row_status",
    "raw_text",
    "dispute_reason",
]
```

Current live summary/status values:

```text
TOTAL_CONFIRMED
confirmed_total
confirmed
disputed
```

These are the same English technical values observed in the downloaded workbook.

## Second Export Path Check

The related export module exists:

```text
/opt/malyarka-telegram-bot/malyarka_core/exports/malyarka.py
```

It has Russian painting-workshop headers and exports via:

```text
export_malyarka_xlsx(...)
```

However, the Telegram callback for `download_malyarka_file` does not import or call `export_malyarka_xlsx(...)`.

No second live path for the button was found in this read-only review. The actual Telegram button path is:

```text
download_malyarka_file
→ handle_malyarka_file_callback(...)
→ prepare_malyarka_file_for_user(...)
→ malyarka_core.exports.malyarka_file.export_malyarka_file_xlsx(...)
```

## Why The Previous Patch Did Not Appear In Fresh Retest

The previous Russian-header live patch was rolled back after the first Telegram sanity failure.

Rollback restored:

```text
/opt/malyarka-telegram-bot/malyarka_core/exports/malyarka_file.py
```

from backup:

```text
/opt/malyarka-telegram-bot/malyarka_core/exports/malyarka_file.py.20260620_075550.before_russian_headers
```

Therefore, during the later fresh-preview retest, live code was already back to the original English `malyarka_file.py`.

This explains why the freshly downloaded file still had English headers:

- not because of `openpyxl`;
- not because of an old callback button;
- not because of a second export path;
- but because the Russian patch had already been rolled back and was no longer live.

## Local Candidate State

The local candidate remains in:

```text
E:\Hermes-Hub\server_staging\malyarka_file_russian_export_fix\malyarka_file.py
```

It contains Russian headers:

```text
№
Высота
Ширина
Количество
Площадь детали, м²
Площадь строки, м²
Статус
Исходный текст
Причина спора
```

It also translates status/summary values in the local candidate.

## What Must Change In The Next Fix

Next fix should change:

```text
/opt/malyarka-telegram-bot/malyarka_core/exports/malyarka_file.py
```

Specifically:

1. `MALYARKA_FILE_HEADERS`
2. `MalyarkaFileRow.as_list()` or row status mapping
3. summary row label `TOTAL_CONFIRMED`
4. summary row status `confirmed_total`
5. status values:
   - `confirmed`
   - `disputed`
   - `confirmed_total`

No adapter logic is needed for this fix.

## Tests Needed

Before the next live patch:

1. Unit test actual `export_malyarka_file_xlsx(...)` from `malyarka_file.py`.
2. Verify workbook first row has Russian headers.
3. Verify workbook has no English technical fields:
   - `row_number`
   - `height`
   - `width`
   - `quantity`
   - `TOTAL_CONFIRMED`
   - `confirmed`
   - `confirmed_total`
4. Verify Russian statuses are present:
   - `подтверждено`
   - `итого подтверждено`
   - optionally `спорно`
5. Add callback-level local test or harness for `prepare_malyarka_file_for_user(...)` if possible.
6. After live patch and restart, fresh Telegram test must create a new order preview before pressing `Скачать Файл Малярки`.

## Next Safe Batch

```text
BATCH_MALYARKA_FILE_RUSSIAN_EXPORT_SECOND_PATH_FIX
```

Recommended mode:

- controlled patch of `malyarka_core/exports/malyarka_file.py`;
- backup first;
- apply tested local candidate;
- run `py_compile`;
- run direct dummy export;
- controlled restart only if needed;
- user fresh-preview Telegram retest.

## No-Touch Confirmation

- No `.py` code was changed.
- No server files were modified.
- No files were copied to the server.
- Service was not started/restarted/stopped/enabled/disabled.
- Hermes adapter feature flag was not changed.
- Phase 2 was not launched.
- Production was not enabled.
- `.env`, `config.py`, token, `os.environ`, DB, live logs, and real orders were not read.
- Git commit/push was not used.

## Follow-Up Result

The approved reapply batch was completed successfully:

```text
MALYARKA_FILE_RUSSIAN_EXPORT_REAPPLY_PASSED
```

The actual export path `malyarka_core/exports/malyarka_file.py` was patched again, verified with local/server checks, and confirmed by a fresh Telegram test. The downloaded Malyarka File now has Russian headers/statuses and no forbidden English technical fields.
