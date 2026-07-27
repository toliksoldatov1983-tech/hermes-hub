# MALYARKA_SYNTHETIC_FIXTURES_REPORT

## Блок

BATCH_027A_MALYARKA_SYNTHETIC_FIXTURES

## Что создано

Добавлены безопасные синтетические fixtures для Malyarka:

- `src/hermes_modules/malyarka/fixtures.py`;
- CLI-команда `scripts\hermes.cmd malyarka-fixtures`;
- тесты `tests/test_malyarka_fixtures.py`;
- документация `docs/MALYARKA_SYNTHETIC_FIXTURES.md`.

## Что покрыто

- валидная одна строка;
- валидный многострочный заказ;
- строка без разделителя;
- нечисловое количество;
- отрицательное количество.

## Ограничения

Fixtures полностью синтетические. Реальные заказы, старые архивы, Google Drive, Excel, токены, ключи и `.env` не читались.

## Проверки

- `scripts\hermes.cmd malyarka-fixtures` — OK;
- `scripts\run_tests.cmd` — OK.

## Следующий крупный блок

BATCH_027B_MALYARKA_DISPUTE_RESOLUTION_CONTRACT
