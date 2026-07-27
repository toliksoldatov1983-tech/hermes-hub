# MALYARKA_LOCAL_WORKFLOW_REPORT

## Блок

BATCH_027C_MALYARKA_LOCAL_WORKFLOW_SUMMARY

## Что создано

Добавлена локальная сводка workflow Malyarka:

- `src/hermes_modules/malyarka/workflow.py`;
- CLI-команда `scripts\hermes.cmd malyarka-workflow`;
- тесты `tests/test_malyarka_workflow.py`;
- документация `docs/MALYARKA_LOCAL_WORKFLOW.md`.

## Workflow

`parse -> preview -> disputes -> resolution -> export gate`

## Ограничения

Workflow использует только синтетические данные. Реальные заказы, Excel, Google Drive, старые архивы, клиентские документы, токены, ключи и `.env` не читались.

## Проверки

- `scripts\hermes.cmd malyarka-workflow` — OK;
- `scripts\run_tests.cmd` — OK.

## Следующий крупный блок

BATCH_027D_MALYARKA_MODULE_STATUS_REPORT
