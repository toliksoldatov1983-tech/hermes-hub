# LOCAL_START_SUMMARY_REPORT

## Блок

BATCH_020_BUILD_LOCAL_START_COMMAND_SUMMARY

## Что создано

Добавлена короткая локальная стартовая сводка Hermes-Clean:

- `src/hermes_core/start_summary.py`;
- CLI-команда `scripts\hermes.cmd start-summary`;
- тесты `tests/test_start_summary.py`;
- обновлён `START_HERE.md`.

## Что показывает команда

- project root;
- health status;
- active batch;
- next task;
- done count;
- reports count;
- `.env` presence check result;
- safe local commands.

## Ограничения

Команда использует только локальные данные Hermes-Clean. Google Drive, старые архивы, старые проекты, реальные заказы, токены, ключи и `.env` не читаются.

## Проверки

- `scripts\hermes.cmd start-summary` — OK;
- `scripts\run_tests.cmd` — OK.

## Следующий крупный блок

BATCH_021_BUILD_LOCAL_COMMAND_HELP
