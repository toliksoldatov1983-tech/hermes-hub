# MALYARKA_FILE_DOWNLOAD_FAILURE_INVESTIGATION

Дата: 2026-06-20

Batch:

```text
BATCH_MALYARKA_FILE_DOWNLOAD_READ_ONLY_INVESTIGATION
```

Итоговый статус:

```text
MALYARKA_FILE_DOWNLOAD_INVESTIGATION_READY
```

## Scope

Это read-only investigation.

Код не менялся. Серверные файлы не менялись. Service не трогался. Feature flag не менялся. Phase 2 не запускалась.

## Current context

Order-like fallback live patch passed sanity:

```text
ORDER_LIKE_FALLBACK_LIVE_PATCH_APPLIED_SANITY_PASSED
```

Separate blocker:

```text
Файл Малярки не скачивается
```

This is treated as a separate export/callback/file-delivery issue, not as a failure of the order-like fallback patch.

## What was checked

Read-only local/staging files:

- `malyarka_telegram/keyboards.py`;
- `malyarka_telegram/app.py`;
- `malyarka_core/services/orders.py`;
- existing server inventory/report markdown.

Read-only server `.py` files:

- `/opt/malyarka-telegram-bot/malyarka_core/exports/corel.py`;
- `/opt/malyarka-telegram-bot/malyarka_core/exports/malyarka_file.py`;
- `/opt/malyarka-telegram-bot/malyarka_core/exports/malyarka.py`.

Read-only server `requirements.txt` package names were checked only for relevant dependency names.

## Button and callback mapping

Button constant:

```text
MALYARKA_FILE_ACTION = "download_malyarka_file"
```

Button label:

```text
Скачать Файл Малярки
```

Button is built in:

```text
malyarka_telegram/keyboards.py
build_copy_keyboard_for_preview(...)
```

Callback registration:

```text
@dispatcher.callback_query(lambda callback: callback.data == MALYARKA_FILE_ACTION)
async def _handle_malyarka_file_callback(callback):
    await handle_malyarka_file_callback(callback, config=config)
```

Handler:

```text
malyarka_telegram/app.py
handle_malyarka_file_callback(...)
```

File preparation:

```text
prepare_malyarka_file_for_user(...)
```

Export function:

```text
malyarka_core.exports.malyarka_file.export_malyarka_file_xlsx(...)
```

Telegram send:

```text
message.answer_document(build_document(prepared.path), caption="Файл Малярки")
```

## Expected Malyarka File flow

1. User sends clean order text.
2. Bot builds preview with export buttons.
3. `_remember_corel_excel_rows(...)` stores clean rows in runtime memory:

```text
_RUNTIME_COREL_ROWS[user_id]
```

4. User clicks `Скачать Файл Малярки`.
5. `handle_malyarka_file_callback(...)` calls `prepare_malyarka_file_for_user(...)`.
6. `prepare_malyarka_file_for_user(...)` builds:

```text
tempdir / malyarka_file_{user_id}.xlsx
```

7. `export_malyarka_file_xlsx(...)` writes the file.
8. Handler sends it through Telegram `answer_document`.

## Difference from Excel/Corel flow

Corel flow:

```text
malyarka_core.exports.corel.export_corel_xlsx(...)
```

Implementation uses only Python standard library:

```text
zipfile.ZipFile
```

Malyarka File flow:

```text
malyarka_core.exports.malyarka_file.export_malyarka_file_xlsx(...)
```

Implementation imports:

```text
from openpyxl import Workbook
```

Read-only requirements check found:

```text
aiogram>=3,<4
```

and did not show `openpyxl`.

## Most likely failure point

Most likely:

```text
malyarka_core.exports.malyarka_file.export_malyarka_file_xlsx(...)
```

Reason:

`Файл Малярки` uses `openpyxl`, while Corel export does not. If `openpyxl` is missing from the server virtual environment or not included in `requirements.txt`, the Malyarka file generation can fail before Telegram sends the document.

This explains why:

- preview/export buttons can appear;
- Corel Excel path can be structurally OK;
- Malyarka File can fail separately.

## Other possible failure points

Still possible and should be tested later:

1. Runtime rows missing:

```text
_RUNTIME_COREL_ROWS.get(user_id)
```

If the runtime memory does not contain rows, callback answers with a ValueError alert and no file.

2. File creation fails:

```text
tempfile.gettempdir()
target_dir.mkdir(...)
workbook.save(output_path)
```

3. Telegram document wrapper/send fails:

```text
_build_telegram_document(...)
FSInputFile(path, filename=path.name)
message.answer_document(...)
```

4. Callback message object does not support `answer_document`.

5. Callback-data mismatch is less likely, because `MALYARKA_FILE_ACTION` is defined and handler is registered with the same constant.

## Local contract tests needed before fix

Future tests should cover:

1. `build_copy_keyboard_for_preview(...)` creates both:
   - `download_corel_excel`;
   - `download_malyarka_file`.
2. `_remember_corel_excel_rows(...)` stores rows when Malyarka/Corel export buttons are present.
3. `prepare_malyarka_file_for_user(...)`:
   - succeeds when rows exist;
   - returns path `malyarka_file_{user_id}.xlsx`;
   - file exists after export;
   - raises clear `ValueError` when rows are missing.
4. `handle_malyarka_file_callback(...)`:
   - calls `answer_document(...)` when file exists;
   - answers alert when rows are missing;
   - answers alert if callback message is missing.
5. Dependency check:
   - `openpyxl` is declared where server dependencies are declared;
   - if not available, code gives a clear error path.
6. Regression:
   - Corel Excel callback remains unchanged.

## Files likely to change later

Do not change now.

Likely future files:

```text
/opt/malyarka-telegram-bot/requirements.txt
/opt/malyarka-telegram-bot/malyarka_core/exports/malyarka_file.py
/opt/malyarka-telegram-bot/malyarka_telegram/app.py
local tests for Malyarka file callback/export
```

Possible fix options:

1. Add `openpyxl` to server dependencies and install it in a controlled dependency batch.
2. Rewrite `export_malyarka_file_xlsx(...)` to use standard-library xlsx generation like Corel export.
3. Improve callback error handling so missing dependency/path failures return a clear Telegram alert.

## Recommended next safe batch

```text
BATCH_MALYARKA_FILE_DOWNLOAD_FIX_PLAN
```

Plan should decide between:

- controlled dependency fix (`openpyxl`);
- no-dependency exporter rewrite;
- callback error handling improvement;
- local tests first.

## No-touch confirmation

Not performed:

- `.py` code change;
- server file change;
- systemctl start/restart/stop/enable/disable;
- feature flag change;
- Phase 2 launch;
- production enable;
- `.env` read;
- `config.py` read;
- token read;
- `os.environ` read;
- database read;
- live log read;
- real order read;
- live Telegram test;
- git/commit/push.

