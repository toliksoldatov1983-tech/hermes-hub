# LOCAL_HEALTH_CHECK_REPORT

## Блок

BATCH_018_BUILD_LOCAL_HEALTH_CHECK_REPORT

## Что создано

Добавлен локальный health-check Hermes-Clean:

- `src/hermes_core/health.py`;
- CLI-команда `scripts\hermes.cmd health`;
- тесты `tests/test_health_check.py`;
- тест CLI-контракта для команды `health`.

## Что проверяет команда

- наличие ключевых файлов и папок Hermes-Clean;
- отсутствие `.env` в известных локальных точках проекта;
- текущий task snapshot;
- текущий memory snapshot.

## Ограничения

Команда не читает содержимое `.env`, токены, ключи, старые архивы, Google Drive, реальные заказы и старые проекты.

## Проверки

- `scripts\hermes.cmd health` — OK;
- `scripts\run_tests.cmd` — OK, 42 tests.

## Следующий крупный блок

BATCH_019_BUILD_LOCAL_REPORT_INDEX
