# LOCAL_COMMAND_HELP_REPORT

## Блок

BATCH_021_BUILD_LOCAL_COMMAND_HELP

## Что создано

Добавлена локальная справка по CLI-командам Hermes-Clean:

- `src/hermes_core/command_help.py`;
- CLI-команда `scripts\hermes.cmd help-local`;
- тесты `tests/test_command_help.py`;
- документация `docs/LOCAL_COMMAND_HELP.md`.

## Что показывает команда

- список локальных команд;
- назначение каждой команды;
- режим выполнения: local/read-only, dry-run или gated;
- approval gates.

## Ограничения

Команда не меняет Google Drive, не читает секреты, не запускает live Telegram, не трогает реальные заказы, старые проекты и архивы.

## Проверки

- `scripts\hermes.cmd help-local` — OK;
- `scripts\run_tests.cmd` — OK.

## Следующий крупный блок

BATCH_022_BUILD_LOCAL_SMOKE_TEST_COMMAND
