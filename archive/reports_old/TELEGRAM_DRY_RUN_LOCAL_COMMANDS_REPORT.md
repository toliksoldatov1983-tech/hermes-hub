# TELEGRAM_DRY_RUN_LOCAL_COMMANDS_REPORT

## Блок

BATCH_028_TELEGRAM_DRY_RUN_LOCAL_COMMANDS

## Что создано

Telegram dry-run связан с локальными Hermes-Clean командами:

- `/status` -> local start summary;
- `/report` -> local report index;
- `/malyarka` -> local Malyarka demo/status;
- `/check` -> local smoke summary.

## Ограничения

Live Telegram не запускался. Токены, `.env`, webhook, polling, внешние API, Google Drive, реальные заказы и старые архивы не читались.

## Проверки

- `scripts\hermes.cmd message /status` — OK;
- `scripts\hermes.cmd message /malyarka` — OK;
- `scripts\hermes.cmd message /check` — OK;
- `scripts\run_tests.cmd` — OK.

## Следующий крупный блок

BATCH_029_TELEGRAM_DRY_RUN_SCENARIOS
