# MALYARKA_FILE_RUSSIAN_EXPORT_REAPPLY_REPORT

Date: 2026-06-20

Batch:

```text
BATCH_MALYARKA_FILE_RUSSIAN_EXPORT_REAPPLY_AND_FRESH_TEST
```

Approval phrase:

```text
APPROVE_MALYARKA_FILE_RUSSIAN_EXPORT_REAPPLY_ONCE
```

Final status:

```text
MALYARKA_FILE_RUSSIAN_EXPORT_REAPPLY_PASSED
```

## Live Target

The controlled patch was applied to the confirmed live export path:

```text
/opt/malyarka-telegram-bot/malyarka_core/exports/malyarka_file.py
```

Backup created before patch:

```text
/opt/malyarka-telegram-bot/malyarka_core/exports/malyarka_file.py.20260620_083303.before_russian_headers_reapply
```

## What Changed

The Malyarka File export workbook output was changed from English technical labels/statuses to Russian labels/statuses.

Headers/statuses covered:

- `row_number` → `№`
- `height` → `Высота`
- `width` → `Ширина`
- `quantity` → `Количество`
- `item_area_m2` / `item_area` → `Площадь детали, м²`
- `row_area_m2` / `row_area` → `Площадь строки, м²`
- `row_status` → `Статус`
- `raw_text` → `Исходный текст`
- `dispute_reason` → `Причина спора`
- `confirmed` → `подтверждено`
- `confirmed_total` → `итого подтверждено`
- `TOTAL_CONFIRMED` → `ИТОГО ПОДТВЕРЖДЕНО`

## Checks

Local checks:

```text
python -m pytest server_staging\malyarka_file_russian_export_fix -q
1 passed

python -m py_compile server_staging\malyarka_file_russian_export_fix\malyarka_file.py
passed
```

Server checks:

- `py_compile` for live `malyarka_file.py`: passed.
- Dummy `.xlsx` export in server `.venv`: passed.
- Server workbook content check:
  - Russian expected values present: yes.
  - forbidden English technical values present: no.

Controlled service restart:

```text
performed
```

Reason: ensure live polling process loads the updated export module.

## Fresh Telegram Test

User performed a fresh Telegram test with a new order preview:

```text
/start: answered
fresh order preview: created
new Скачать файл Малярки button: pressed
file downloaded: yes
headers: Russian
```

Forbidden English fields were absent:

- `row_number`
- `height`
- `width`
- `quantity`
- `item_area`
- `row_area`
- `row_status`
- `raw_text`
- `dispute_reason`
- `TOTAL_CONFIRMED`
- `confirmed`
- `confirmed_total`

Visible Russian values included:

- `№`
- `Высота`
- `Ширина`
- `Количество`
- `Площадь`
- `Статус`
- `Исходный`
- `Причина спора`
- `ИТОГО ПОДТВЕРЖДЕНО`
- `подтверждено`
- `итого подтверждено`

## Final Runtime State

Read-only runtime confirmation:

```text
service: active/running
autostart: disabled
Hermes adapter feature flag: OFF
Phase 2: OFF
production: OFF
rollback: not needed
```

## No-Touch Confirmation

- Hermes adapter feature flag was not changed.
- Phase 2 was not launched.
- Production was not enabled.
- `.env`, `config.py`, token, `os.environ`, databases, live logs, and real orders were not read.
- Unrelated `.py` files were not changed.
- Adapter logic was not changed.
- Git commit/push was not performed.
