# LOCAL_RELEASE_CHECKLIST_REPORT

## Блок

BATCH_024_BUILD_LOCAL_RELEASE_CHECKLIST

## Что создано

Добавлен локальный checklist готовности Hermes-Clean:

- `src/hermes_core/release_checklist.py`;
- CLI-команда `scripts\hermes.cmd release-checklist`;
- тесты `tests/test_release_checklist.py`;
- документация `docs/LOCAL_RELEASE_CHECKLIST.md`.

## Что создаёт команда

- `05_REPORTS/LOCAL_RELEASE_CHECKLIST.md`.

## Что входит в checklist

- readiness status;
- готовые локальные команды;
- пройденные проверки;
- открытые approval gates;
- pending approvals preview;
- варианты следующего направления.

## Ограничения

Команда пишет только локальный markdown-файл внутри Hermes-Clean. Внешние API, Google Drive, старые архивы, реальные заказы, секреты и `.env` не читаются.

## Проверки

- `scripts\hermes.cmd release-checklist` — OK;
- `scripts\run_tests.cmd` — OK.

## Следующий крупный блок

BATCH_025_USER_DECIDES_NEXT_ACTIVE_DIRECTION
