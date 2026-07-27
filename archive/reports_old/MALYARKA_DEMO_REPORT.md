# MALYARKA_DEMO_REPORT

## Блок

BATCH_027F_MALYARKA_CLI_OUTPUT_POLISH

## Что создано

Добавлена локальная demo-команда Malyarka:

- `src/hermes_modules/malyarka/demo.py`;
- CLI-команда `scripts\hermes.cmd malyarka-demo`;
- тесты `tests/test_malyarka_demo.py`;
- документация `docs/MALYARKA_DEMO.md`.

## Что показывает команда

- количество synthetic fixtures;
- ready/disputed fixture counts;
- workflow status;
- future export columns;
- export gate status.

## Ограничения

Команда использует только локальные synthetic data. Реальные заказы, Excel, Google Drive, старые архивы, клиентские документы, токены, ключи и `.env` не читались.

## Проверки

- `scripts\hermes.cmd malyarka-demo` — OK;
- `scripts\run_tests.cmd` — OK.

## Следующий крупный блок

BATCH_027G_MALYARKA_APPROVAL_OR_LOCAL_NEXT_STEP
