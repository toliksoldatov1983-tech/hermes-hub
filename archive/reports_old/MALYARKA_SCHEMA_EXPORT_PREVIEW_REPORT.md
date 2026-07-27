# MALYARKA_SCHEMA_EXPORT_PREVIEW_REPORT

## Блок

BATCH_027E_MALYARKA_SCHEMA_AND_EXPORT_PREVIEW

## Что создано

Добавлена локальная схема будущего Malyarka order и export preview:

- `src/hermes_modules/malyarka/schema_contract.py`;
- `src/hermes_modules/malyarka/export_preview.py`;
- CLI-команда `scripts\hermes.cmd malyarka-schema`;
- тесты `tests/test_malyarka_schema.py`;
- документация `docs/MALYARKA_SCHEMA_AND_EXPORT_PREVIEW.md`.

## Что важно

Export preview не пишет Excel и не создаёт реальные файлы. `can_write_file=False`.

## Ограничения

Реальные заказы, Excel, Google Drive, старые архивы, клиентские документы, токены, ключи и `.env` не читались.

## Проверки

- `scripts\hermes.cmd malyarka-schema` — OK;
- `scripts\run_tests.cmd` — OK.

## Следующий крупный блок

BATCH_027F_MALYARKA_CLI_OUTPUT_POLISH
