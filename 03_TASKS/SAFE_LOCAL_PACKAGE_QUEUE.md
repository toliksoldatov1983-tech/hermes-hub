# SAFE_LOCAL_PACKAGE_QUEUE

## Режим

Грузить Hermes-Clean максимально, но безопасно.

Codex может выполнять эти пакеты подряд без дополнительных уточнений, пока работа остаётся внутри `C:\Users\user\Desktop\Hermes-Clean` и не упирается в опасный gate.

## Общие запреты для всех пакетов

- не удалять файлы;
- не читать `.env`, токены, ключи, пароли;
- не запускать live Telegram;
- не запускать Gemini / DeepSeek / DeepSig API;
- не менять Google Drive;
- не читать реальные заказы;
- не читать клиентские документы;
- не открывать `[удалён]`;
- не читать и не распаковывать `«Гермес Клин».zip [архив]` и `[архив] архивный zip-файл`;
- не импортировать старые архивы как рабочий проект;
- не экспортировать реальные Excel-файлы.

## BATCH_063_SAFE_LOCAL_MALYARKA_FULL_HARDENING_PACK

Цель: усилить Malyarka на synthetic/manual input.

Состав:

- validation layer;
- synthetic fixtures expansion;
- dispute resolver contract;
- export gate hardening;
- Telegram dry-run Malyarka scenarios;
- docs and command coverage;
- tests and smoke.

Проверки:

- `scripts\hermes.cmd help-local`
- `scripts\hermes.cmd malyarka-fixtures`
- `scripts\hermes.cmd malyarka-disputes`
- `scripts\hermes.cmd malyarka-combined`
- `scripts\hermes.cmd telegram-scenarios`
- `scripts\hermes.cmd project-audit`
- `scripts\hermes.cmd smoke`
- `scripts\run_tests.cmd`

## BATCH_064_SAFE_LOCAL_FINAL_REFRESH_AFTER_MALYARKA_FULL_HARDENING

Цель: итоговый refresh после большого Malyarka hardening pack.

Состав:

- refresh-all;
- dashboard;
- app-status;
- daily-report;
- project-audit;
- smoke;
- full tests;
- итоговый отчёт.

## BATCH_065_SAFE_LOCAL_RUNTIME_SAFETY_GATE_AND_AUDIT_LOG

Цель: усилить runtime safety: единый gate и локальный audit log без внешних сервисов.

Состав:

- расширить `src\hermes_core\safety`;
- добавить локальный audit log contract;
- логировать только безопасные synthetic/local события;
- не писать секреты и реальные данные;
- добавить CLI-команду или отчёт проверки gate;
- добавить тесты на blocked/confirm/safe decisions.

Проверки:

- `scripts\hermes.cmd safety delete`
- `scripts\hermes.cmd project-audit`
- `scripts\hermes.cmd smoke`
- `scripts\run_tests.cmd`

## BATCH_066_SAFE_LOCAL_TELEGRAM_DRY_RUN_DEEPENING_PACK

Цель: сильно углубить Telegram dry-run без live Telegram.

Состав:

- расширить command router;
- добавить сценарии order/status/report/disputes/fix/export-blocked;
- добавить blocked actions list;
- улучшить telegram-status;
- добавить тесты, что нет token/env/network/polling/webhook;
- обновить docs.

Проверки:

- `scripts\hermes.cmd message /status`
- `scripts\hermes.cmd message /malyarka-combined`
- `scripts\hermes.cmd telegram-scenarios`
- `scripts\hermes.cmd telegram-status`
- `scripts\hermes.cmd smoke`
- `scripts\run_tests.cmd`

## BATCH_067_SAFE_LOCAL_AI_PROVIDER_MOCK_AND_SECRET_GATE_HARDENING

Цель: усилить AI provider layer без реальных API.

Состав:

- углубить mock Gemini provider;
- углубить mock DeepSeek / DeepSig review provider;
- добавить secret gate checklist в код/тесты/доки;
- проверить, что real modes blocked;
- запретить `.env` и реальные ключи;
- запретить отправку реальных данных наружу.

Проверки:

- `scripts\hermes.cmd ai-provider --mode mock`
- `scripts\hermes.cmd ai-provider --mode gemini-disabled`
- `scripts\hermes.cmd review-provider --mode mock-review`
- `scripts\hermes.cmd review-provider --mode deepseek-disabled`
- `scripts\hermes.cmd smoke`
- `scripts\run_tests.cmd`

## BATCH_068_SAFE_LOCAL_PROJECT_AUDIT_AND_COMMAND_COVERAGE_MAX

Цель: максимально усилить локальный audit и command coverage.

Состав:

- project-audit проверяет все ключевые docs/reports/commands;
- проверяет, что next task задан;
- проверяет disabled subsystems;
- проверяет отсутствие `.env` в Hermes-Clean;
- проверяет docs coverage для новых команд;
- добавляет отчёт с actionable findings.

Проверки:

- `scripts\hermes.cmd project-audit`
- `scripts\hermes.cmd help-local`
- `scripts\hermes.cmd dashboard`
- `scripts\hermes.cmd smoke`
- `scripts\run_tests.cmd`

## BATCH_069_SAFE_LOCAL_DASHBOARD_AND_DAILY_REPORT_MAX

Цель: сделать dashboard/daily-report максимально полезными для ежедневного управления.

Состав:

- dashboard показывает next tasks queue;
- dashboard показывает pending approvals;
- dashboard показывает Malyarka readiness;
- dashboard показывает Telegram dry-run readiness;
- daily-report показывает последние проверки;
- daily-report показывает safe commands;
- docs updated.

Проверки:

- `scripts\hermes.cmd dashboard`
- `scripts\hermes.cmd daily-report`
- `scripts\hermes.cmd refresh-all`
- `scripts\hermes.cmd smoke`
- `scripts\run_tests.cmd`

## BATCH_070_SAFE_LOCAL_DOCS_POLISH_AND_USER_RUNBOOK

Цель: собрать понятный русский runbook для пользователя.

Состав:

- обновить `START_HERE.md`;
- обновить `README.md`;
- создать/обновить `docs\USER_RUNBOOK_RU.md`;
- создать/обновить `docs\SAFE_LOCAL_OPERATIONS_RU.md`;
- описать ежедневный запуск;
- описать что запрещено;
- описать что делать при следующем approval gate.

Проверки:

- `scripts\hermes.cmd help-local`
- `scripts\hermes.cmd project-audit`
- `scripts\hermes.cmd smoke`
- `scripts\run_tests.cmd`

## BATCH_071_SAFE_LOCAL_RELEASE_CANDIDATE_PREP

Цель: подготовить Hermes-Clean как локальный release candidate без live-функций.

Состав:

- release checklist max;
- known limitations;
- disabled subsystem matrix;
- local acceptance criteria;
- test report;
- user next directions.

Проверки:

- `scripts\hermes.cmd release-checklist`
- `scripts\hermes.cmd project-audit`
- `scripts\hermes.cmd smoke`
- `scripts\run_tests.cmd`

## BATCH_072_SAFE_LOCAL_FINAL_MASTER_REFRESH_AND_NEXT_DECISION

Цель: финальный мастер-refresh после серии safe local hardening пакетов.

Состав:

- refresh-all;
- dashboard;
- daily-report;
- app-status;
- project-audit;
- smoke;
- full tests;
- final local report;
- next decision menu.

Следующее решение после пакета:

1. Продолжить Malyarka.
2. Углубить Telegram dry-run.
3. Подготовить secret setup checklist.
4. Вернуться к Google Drive только планом.
5. Готовить локальное приложение/UI без live-сервисов.
