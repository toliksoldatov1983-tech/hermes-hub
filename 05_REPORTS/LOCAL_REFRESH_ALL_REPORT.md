# LOCAL_REFRESH_ALL_REPORT

## Блок

BATCH_032_SAFE_LOCAL_REFRESH_ALL

## Что создано

Добавлена локальная команда обновления сводных отчётов:

- `src/hermes_core/refresh_all.py`;
- CLI-команда `scripts\hermes.cmd refresh-all`;
- тесты `tests/test_refresh_all.py`;
- документация `docs/LOCAL_REFRESH_ALL.md`.

## Что обновляет

- `05_REPORTS/LOCAL_STATUS_EXPORT.md`;
- `05_REPORTS/LOCAL_RELEASE_CHECKLIST.md`;
- `05_REPORTS/TELEGRAM_DRY_RUN_STATUS.md`;
- `05_REPORTS/MALYARKA_MODULE_STATUS.md`;
- `05_REPORTS/LOCAL_DASHBOARD.md`.

## Ограничения

Команда локальная. Секреты, `.env`, live Telegram, Google Drive, реальные заказы и старые архивы не читаются и не меняются.

## Проверки

- `scripts\hermes.cmd refresh-all` — OK;
- `scripts\run_tests.cmd` — OK.

## Следующий крупный блок

BATCH_033_SAFE_LOCAL_USER_DOCS_POLISH
