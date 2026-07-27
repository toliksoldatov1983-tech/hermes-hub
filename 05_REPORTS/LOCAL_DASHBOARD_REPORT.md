# LOCAL_DASHBOARD_REPORT

## Блок

BATCH_031_SAFE_LOCAL_DASHBOARD

## Что создано

Добавлен единый локальный dashboard Hermes-Clean:

- `src/hermes_core/dashboard.py`;
- CLI-команда `scripts\hermes.cmd dashboard`;
- тесты `tests/test_dashboard.py`;
- output `05_REPORTS/LOCAL_DASHBOARD.md`.

## Что включает

- core status;
- smoke status;
- Malyarka synthetic/local status;
- Telegram dry-run status;
- pending approvals preview.

## Ограничения

Dashboard локальный. Секреты, live Telegram, Google Drive, реальные заказы и старые архивы не читались и не менялись.
