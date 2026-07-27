# NEXT_10_HERMES_TASKS_AFTER_063C

## Статус

Подготовлена следующая серия из 10 больших задач для Hermes-Clean.

Эта серия начинается после `BATCH_063C_SAFE_PORT_MISSING_MALYARKA_HARDENING_TO_DESKTOP`.

## Общие запреты

- не удалять файлы;
- не читать `.env`, токены, ключи, пароли;
- не менять Google Drive;
- не запускать live Telegram;
- не запускать внешние AI API;
- не читать реальные заказы;
- не читать клиентские документы;
- не открывать `[удалён]`;
- не читать и не распаковывать старые архивы;
- не экспортировать реальные Excel-файлы.

## 1. BATCH_073_SAFE_LOCAL_MALYARKA_VALIDATION_REFRESH

Цель: итогово проверить и задокументировать Malyarka validation после BATCH_063C.

Сделать:

- обновить Malyarka validation docs;
- обновить Malyarka status report;
- проверить fixtures count;
- проверить export gate status;
- проверить dispute questions;
- добавить итоговый validation readiness report.

Проверки:

- `scripts\hermes.cmd malyarka-fixtures`
- `scripts\hermes.cmd malyarka-combined`
- `scripts\hermes.cmd project-audit`
- `scripts\hermes.cmd smoke`
- `scripts\run_tests.cmd`

## 2. BATCH_074_SAFE_LOCAL_MALYARKA_ORDER_STATE_MACHINE

Цель: описать и реализовать локальную state machine заказа Malyarka.

Состояния:

- `RAW_INPUT`
- `PARSED`
- `VALIDATED`
- `HAS_DISPUTES`
- `READY_FOR_PREVIEW`
- `EXPORT_BLOCKED`
- `READY_FOR_FUTURE_EXPORT`

Сделать:

- добавить contract/module для state machine;
- связать parser/validation/disputes/export gate;
- добавить synthetic tests;
- добавить docs.

## 3. BATCH_075_SAFE_LOCAL_MALYARKA_PREVIEW_REPORT_MAX

Цель: сделать Malyarka preview максимально понятным.

Сделать:

- preview показывает confirmed rows;
- disputed rows;
- validation issues;
- synthetic pricing;
- export block reasons;
- next safe action;
- Telegram dry-run friendly summary.

Без Excel и без реальных заказов.

## 4. BATCH_076_SAFE_LOCAL_TELEGRAM_MALYARKA_DIALOG_FLOW

Цель: углубить dry-run диалог Malyarka в Telegram.

Сделать:

- сценарий ввода заказа;
- сценарий спорных строк;
- сценарий уточнения;
- сценарий повторного preview;
- сценарий export blocked;
- сценарий status/report.

Проверки:

- `scripts\hermes.cmd telegram-scenarios`
- `scripts\hermes.cmd message /malyarka-combined`
- `scripts\hermes.cmd smoke`
- `scripts\run_tests.cmd`

## 5. BATCH_077_SAFE_LOCAL_TASK_QUEUE_AND_AUTO_NEXT_HARDENING

Цель: усилить task queue и auto-next.

Сделать:

- NEXT_TASK всегда валиден;
- DONE содержит последние выполненные блоки;
- ACTIVE_BATCH не отстаёт;
- pending approvals видны;
- dashboard показывает очередь;
- project-audit ловит пустой/битый next task.

## 6. BATCH_078_SAFE_LOCAL_MEMORY_DECISIONS_AND_PROHIBITIONS_SYNC

Цель: синхронизировать локальную память проекта.

Сделать:

- PROJECT_DECISIONS;
- PROJECT_PROHIBITIONS;
- pending approvals;
- safety rules;
- Malyarka decisions;
- AI provider decisions;
- Telegram decisions.

Только внутри Hermes-Clean.

## 7. BATCH_079_SAFE_LOCAL_SECRET_AND_ENV_GUARD_MAX

Цель: усилить защиту от секретов.

Сделать:

- проверить, что `.env` не создаётся;
- проверить, что docs не требуют реальные ключи;
- проверить, что mock providers не читают env;
- добавить отчёт secret guard max;
- добавить tests на forbidden secret access.

Без чтения настоящих `.env`.

## 8. BATCH_080_SAFE_LOCAL_GOOGLE_DRIVE_BLOCKED_STATUS_FREEZE

Цель: зафиксировать Google Drive как отложенную задачу.

Сделать:

- обновить Google Drive diagnostic;
- зафиксировать `403 appNotAuthorizedToFile`;
- подтвердить, что перенос не повторять;
- описать manual options;
- обновить pending approvals.

Без Google Drive write/move.

## 9. BATCH_081_SAFE_LOCAL_RELEASE_CANDIDATE_V2

Цель: подготовить Hermes-Clean Local Safe RC v2.

Сделать:

- release checklist v2;
- acceptance criteria;
- known limitations;
- disabled subsystem matrix;
- local command matrix;
- final test report.

## 10. BATCH_082_SAFE_LOCAL_NEXT_DIRECTION_DECISION_MENU

Цель: подготовить меню следующего большого решения.

Варианты:

1. Продолжить Malyarka.
2. Готовить Gemini secret setup checklist.
3. Готовить DeepSeek review checklist.
4. Углубить Telegram dry-run.
5. Вернуться к Google Drive только планом.
6. Готовить локальный UI без live-сервисов.
7. Подготовить real order approval protocol.

Результат:

- `03_TASKS\NEXT_TASK.md` содержит один выбранный или ожидающий выбора следующий блок;
- `05_REPORTS\NEXT_DIRECTION_MENU_REPORT.md` создан.
