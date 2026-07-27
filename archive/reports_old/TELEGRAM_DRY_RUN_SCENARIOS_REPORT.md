# TELEGRAM_DRY_RUN_SCENARIOS_REPORT

## Блок

BATCH_029_TELEGRAM_DRY_RUN_SCENARIOS

## Что создано

Добавлены Telegram dry-run scenarios:

- `src/hermes_core/telegram/scenarios.py`;
- CLI-команда `scripts\hermes.cmd telegram-scenarios`;
- тесты `tests/test_telegram_scenarios.py`;
- документация `docs/TELEGRAM_DRY_RUN_SCENARIOS.md`.

## Сценарии

- morning status;
- Malyarka check;
- project report;
- safety check.

## Ограничения

Live Telegram, токены, `.env`, webhook, polling, внешние API, Google Drive, реальные заказы и старые архивы не читались и не запускались.

## Проверки

- `scripts\hermes.cmd telegram-scenarios` — OK;
- `scripts\run_tests.cmd` — OK.

## Следующий крупный блок

BATCH_030_TELEGRAM_DRY_RUN_STATUS_REPORT
