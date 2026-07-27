# LOCAL_STATUS_EXPORT_REPORT

## Блок

BATCH_023_BUILD_LOCAL_STATUS_EXPORT

## Что создано

Добавлен локальный markdown-экспорт статуса Hermes-Clean:

- `src/hermes_core/status_export.py`;
- CLI-команда `scripts\hermes.cmd export-status`;
- тесты `tests/test_status_export.py`;
- документация `docs/LOCAL_STATUS_EXPORT.md`.

## Что создаёт команда

- `05_REPORTS/LOCAL_STATUS_EXPORT.md`.

## Что входит в экспорт

- health status;
- smoke status;
- active batch;
- next task;
- done count;
- reports count;
- safe commands;
- pending approvals preview.

## Ограничения

Команда пишет только локальный markdown-файл внутри Hermes-Clean. Внешние API, Google Drive, старые архивы, реальные заказы, секреты и `.env` не читаются.

## Проверки

- `scripts\hermes.cmd export-status` — OK;
- `scripts\run_tests.cmd` — OK.

## Следующий крупный блок

BATCH_024_BUILD_LOCAL_RELEASE_CHECKLIST
