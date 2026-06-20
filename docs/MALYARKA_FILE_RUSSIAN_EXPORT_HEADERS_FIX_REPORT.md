# MALYARKA_FILE_RUSSIAN_EXPORT_HEADERS_FIX_REPORT

Date: 2026-06-20

Batch:

```text
BATCH_MALYARKA_FILE_RUSSIAN_EXPORT_HEADERS_FIX
```

Final status:

```text
MALYARKA_FILE_RUSSIAN_EXPORT_HEADERS_FIX_BLOCKED
```

## Summary

The local candidate changed only the Malyarka File export labels/status strings in `malyarka_file.py`.

Local checks passed:

- `python -m pytest server_staging\malyarka_file_russian_export_fix -q`
- result: `1 passed`
- `python -m py_compile server_staging\malyarka_file_russian_export_fix\malyarka_file.py`
- result: passed

Live patch was applied once to:

```text
/opt/malyarka-telegram-bot/malyarka_core/exports/malyarka_file.py
```

Backup was created:

```text
/opt/malyarka-telegram-bot/malyarka_core/exports/malyarka_file.py.20260620_075550.before_russian_headers
```

Server-side safe checks passed after patch:

- `py_compile` passed.
- A dummy `.xlsx` export was created successfully in a temporary directory.

Controlled service restart was performed because the live process may have already imported the export module.

## Telegram Sanity Result

User reported:

```text
не скачивается
```

Meaning: after the Russian headers live patch, `Файл Малярки` did not download in Telegram.

This is treated as a regression of the Russian export patch, not as a failure of the earlier `openpyxl` dependency fix.

## Rollback

Rollback was performed immediately from backup:

```text
/opt/malyarka-telegram-bot/malyarka_core/exports/malyarka_file.py.20260620_075550.before_russian_headers
```

The live target was restored:

```text
/opt/malyarka-telegram-bot/malyarka_core/exports/malyarka_file.py
```

`py_compile` passed after rollback, and controlled service restart was performed.

Final runtime check after rollback:

```text
service: active/running
autostart: disabled
Hermes adapter feature flag: OFF
production: OFF
Phase 2: OFF
```

## Files Changed

Local staging:

```text
E:\Hermes-Hub\server_staging\malyarka_file_russian_export_fix\malyarka_file.py
E:\Hermes-Hub\server_staging\malyarka_file_russian_export_fix\test_malyarka_file_russian_headers.py
```

Live server:

- `malyarka_file.py` was patched once.
- Then it was rolled back from backup after Telegram sanity failed.

## Open Blocker

```text
MALYARKA_FILE_RUSSIAN_EXPORT_HEADERS_FIX_BLOCKED
```

Observed contradiction:

- Local pytest passed.
- Server-side dummy export created `.xlsx`.
- Telegram callback did not download the file after live patch.

Next investigation must determine why the live callback/file delivery path fails with the Russian-label export while the direct export function succeeds.

## Next Safe Batch

```text
BATCH_MALYARKA_FILE_RUSSIAN_EXPORT_CALLBACK_FAILURE_INVESTIGATION
```

Recommended mode:

- read-only first;
- do not change code;
- do not read secrets, DB, live logs, or real orders;
- compare callback send path, generated filename, MIME/document sending, and exception handling around `download_malyarka_file`.

## No-Touch Confirmation

- Hermes adapter feature flag was not changed.
- Phase 2 was not launched.
- Production was not enabled.
- `.env`, `config.py`, token, `os.environ`, databases, live logs, and real orders were not read.
- Adapter logic was not changed.
- Git commit/push was not performed.

## Fresh Preview Retest Closure

User performed a fresh Telegram test with a new order preview and a newly generated `Скачать Файл Малярки` button.

Result:

```text
fresh preview: yes
new button pressed: yes
file downloaded: yes
headers: English
```

Final status for the Russian-header batch:

```text
MALYARKA_FILE_RUSSIAN_EXPORT_HEADERS_FIX_NEEDS_CODE_REVIEW
```

Interpretation:

- The file download path works.
- The issue is not caused by an old pre-restart callback button.
- The issue is not caused by missing `openpyxl`.
- The live export still produces English technical headers/statuses, or Telegram uses a second export path.

Next safe batch:

```text
BATCH_MALYARKA_FILE_RUSSIAN_EXPORT_CODE_REVIEW_AND_SECOND_PATH_INVESTIGATION
```

## Final Reapply Result

The later approved reapply batch fixed the issue:

```text
MALYARKA_FILE_RUSSIAN_EXPORT_REAPPLY_PASSED
```

Fresh Telegram test result:

- fresh preview created: yes;
- new `Скачать файл Малярки` button pressed: yes;
- file downloaded: yes;
- headers/statuses: Russian;
- forbidden English technical fields: absent.
