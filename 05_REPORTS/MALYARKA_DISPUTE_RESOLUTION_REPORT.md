# MALYARKA_DISPUTE_RESOLUTION_REPORT

## Блок

BATCH_027B_MALYARKA_DISPUTE_RESOLUTION_CONTRACT

## Что создано

Добавлен локальный контракт исправления спорной строки Malyarka:

- `src/hermes_modules/malyarka/resolution_contract.py`;
- CLI-команда `scripts\hermes.cmd malyarka-resolve`;
- тесты `tests/test_malyarka_resolution.py`;
- документация `docs/MALYARKA_DISPUTE_RESOLUTION_CONTRACT.md`.

## Правило

Спорная строка может быть исправлена только явной replacement-строкой формата:

`item | quantity | unit`

Финальный экспорт всё равно остаётся gated и требует отдельного future approval.

## Ограничения

Реальные заказы, Excel, Google Drive, старые архивы, клиентские документы, токены, ключи и `.env` не читались.

## Проверки

- `scripts\hermes.cmd malyarka-resolve "paint 2 bucket" --replacement "paint | 2 | bucket"` — OK;
- `scripts\run_tests.cmd` — OK.

## Следующий крупный блок

BATCH_027C_MALYARKA_LOCAL_WORKFLOW_SUMMARY
