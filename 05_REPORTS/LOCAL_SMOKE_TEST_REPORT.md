# LOCAL_SMOKE_TEST_REPORT

## Блок

BATCH_022_BUILD_LOCAL_SMOKE_TEST_COMMAND

## Что создано

Добавлен локальный smoke-test Hermes-Clean:

- `src/hermes_core/smoke.py`;
- CLI-команда `scripts\hermes.cmd smoke`;
- тесты `tests/test_smoke.py`;
- документация `docs/LOCAL_SMOKE_TEST.md`.

## Что проверяет команда

- `start-summary`;
- `health`;
- `reports`;
- `tasks`;
- `memory`;
- `help-local`;
- Telegram message dry-run;
- Malyarka preview contract;
- disabled Gemini provider gate;
- disabled DeepSeek review gate;
- `safety delete`.

## Ограничения

Команда выполняет только локальные проверки контрактов. Внешние API, Google Drive, старые архивы, реальные заказы, секреты и `.env` не читаются.

## Проверки

- `scripts\hermes.cmd smoke` — OK;
- `scripts\run_tests.cmd` — OK.

## Следующий крупный блок

BATCH_023_BUILD_LOCAL_STATUS_EXPORT
