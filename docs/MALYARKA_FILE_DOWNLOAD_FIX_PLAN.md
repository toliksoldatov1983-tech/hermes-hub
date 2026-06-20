# MALYARKA_FILE_DOWNLOAD_FIX_PLAN

Дата: 2026-06-20

Batch:

```text
BATCH_MALYARKA_FILE_DOWNLOAD_FIX_PLAN
```

Итоговый статус:

```text
MALYARKA_FILE_DOWNLOAD_FIX_PLAN_READY_DEPENDENCY_MISSING
```

## Read-only checks

### `openpyxl` in server `.venv`

Command type: read-only import check.

Result:

```text
ModuleNotFoundError: No module named 'openpyxl'
OPENPYXL_IMPORT_EXIT=1
```

Conclusion:

```text
openpyxl is not installed in /opt/malyarka-telegram-bot/.venv
```

### `openpyxl` in `requirements.txt`

Read-only grep result:

```text
REQUIREMENTS_GREP_EXIT=1
```

Conclusion:

```text
openpyxl is not declared in /opt/malyarka-telegram-bot/requirements.txt
```

### Where `openpyxl` is imported

Read-only references:

```text
/opt/malyarka-telegram-bot/malyarka_core/exports/malyarka.py: from openpyxl import Workbook
/opt/malyarka-telegram-bot/malyarka_core/exports/malyarka_file.py: from openpyxl import Workbook
```

## Confirmed likely cause

`Скачать Файл Малярки` fails because `malyarka_core.exports.malyarka_file.export_malyarka_file_xlsx(...)` imports `openpyxl`, but `openpyxl` is neither installed in the server virtual environment nor declared in `requirements.txt`.

Corel export can still work because it creates `.xlsx` through Python standard library `zipfile` and does not require `openpyxl`.

## Future controlled fix

Future approval phrase:

```text
APPROVE_MALYARKA_FILE_DOWNLOAD_FIX_ONCE
```

Suggested controlled fix path:

1. Read-only precheck:
   - service status;
   - autostart status;
   - feature flag OFF;
   - production OFF;
   - confirm `openpyxl` missing.
2. Backup:
   - `/opt/malyarka-telegram-bot/requirements.txt`.
3. Add `openpyxl` to `requirements.txt`.
4. Install into `.venv` with controlled dependency command.
5. Verify:

```text
/opt/malyarka-telegram-bot/.venv/bin/python -c "import openpyxl; print(openpyxl.__version__)"
```

6. Run safe import/export function check with dummy order only, no real orders.
7. Controlled service restart only if needed.
8. User performs Telegram sanity test for `Скачать Файл Малярки`.
9. Record result.

## Alternative fix path

If avoiding dependency is preferred:

1. Rewrite `malyarka_file.py` exporter to use standard-library xlsx generation, similar to `corel.py`.
2. Add local tests.
3. Apply as separate code patch after approval.

This is larger than adding the missing dependency.

## Rollback plan

If `requirements.txt` is changed:

- restore from backup;
- do not leave undocumented dependency state.

If dependency install fails:

- stop;
- do not restart service unless already approved and necessary;
- report exact failure.

If dependency install succeeds but Telegram file still fails:

- keep `openpyxl` only if user approves dependency retention;
- otherwise restore `requirements.txt` from backup and plan cleanup.

If callback/export code is changed in a later batch:

- backup changed files first;
- restore backup on syntax/test failure;
- keep feature flag OFF and production OFF.

## Tests needed before or during fix

Local/server-safe tests:

1. `openpyxl` import check.
2. `export_malyarka_file_xlsx(...)` with dummy clean order writes `.xlsx`.
3. `prepare_malyarka_file_for_user(...)` creates `malyarka_file_{user_id}.xlsx` when rows exist.
4. Missing rows returns clear `ValueError`.
5. `handle_malyarka_file_callback(...)` calls `answer_document(...)` with fake callback.
6. Corel export still works.

## No-touch confirmation

Not performed:

- dependency install;
- `requirements.txt` change;
- `.py` code change;
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

## 2026-06-20 — Fix applied and sanity passed

Result:

```text
MALYARKA_FILE_DOWNLOAD_FIX_DEPENDENCY_INSTALLED_TEST_PASSED
```

Report:

```text
E:\Hermes-Hub\docs\MALYARKA_FILE_DOWNLOAD_FIX_REPORT.md
```

Dependency installed:

```text
openpyxl 3.1.5
```

Telegram sanity result:

```text
Файл Малярки теперь скачивается.
```

New separate blocker:

```text
MALYARKA_FILE_EXPORT_USES_ENGLISH_HEADERS_AND_STATUSES
```

Next safe batch:

```text
BATCH_MALYARKA_FILE_RUSSIAN_EXPORT_HEADERS_FIX
```
