# LOCAL_APP_RUNTIME_REPORT

## Блок

BATCH_026_PREPARE_LOCAL_APP_RUNTIME

## Что создано

Подготовлен локальный runtime Hermes-Clean:

- `scripts/start_hermes.cmd`;
- `scripts/smoke.cmd`;
- `scripts/export_status.cmd`;
- `scripts/release_checklist.cmd`;
- `docs/LOCAL_APP_RUNTIME.md`;
- обновлены `README.md`, `START_HERE.md`, `docs/WINDOWS_COMMANDS.md`.

## Что делает runtime

- запускает короткую стартовую сводку;
- запускает локальный smoke-test;
- обновляет локальный status export;
- обновляет локальный release checklist;
- запускает unit tests.

## Ограничения

Runtime работает только внутри Hermes-Clean. Он не вызывает внешние API, не читает Google Drive, старые архивы, секреты, `.env`, реальные заказы и не запускает live Telegram.

## Проверки

- `scripts\start_hermes.cmd` — OK;
- `scripts\smoke.cmd` — OK;
- `scripts\export_status.cmd` — OK;
- `scripts\release_checklist.cmd` — OK;
- `scripts\run_tests.cmd` — OK.

## Следующий крупный блок

BATCH_027_CONTINUE_SAFE_LOCAL_DEVELOPMENT_OR_PICK_APPROVAL_GATE
