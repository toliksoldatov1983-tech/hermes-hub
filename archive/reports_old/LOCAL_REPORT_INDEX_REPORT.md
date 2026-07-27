# LOCAL_REPORT_INDEX_REPORT

## Блок

BATCH_019_BUILD_LOCAL_REPORT_INDEX

## Что создано

Добавлен локальный индекс отчётов Hermes-Clean:

- `src/hermes_core/report_index.py`;
- CLI-команда `scripts\hermes.cmd reports`;
- тесты `tests/test_report_index.py`;
- тест CLI-контракта для команды `reports`.

## Что показывает команда

- количество markdown-отчётов в `05_REPORTS`;
- ключевые отчёты проекта;
- последние изменённые отчёты;
- текущий active batch;
- следующий task;
- количество завершённых блоков;
- preview pending approvals.

## Ограничения

Команда читает только локальные markdown-отчёты внутри Hermes-Clean. Google Drive, старые архивы, старые проекты, реальные заказы, токены, ключи и `.env` не читаются.

## Проверки

- `scripts\hermes.cmd reports` — OK;
- `scripts\run_tests.cmd` — OK.

## Следующий крупный блок

BATCH_020_BUILD_LOCAL_START_COMMAND_SUMMARY
