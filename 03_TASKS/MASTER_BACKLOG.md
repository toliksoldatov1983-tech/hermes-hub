# MASTER_BACKLOG

## Core

- Довести Hermes router до CLI-приложения.
- Добавить persistable task state.
- Добавить memory registry read/write внутри Hermes-Clean.
- Усилить runtime safety gate.
- Добавить локальный audit log без секретов и внешних сервисов.

## AI

- Подключить Gemini только после `APPROVE_SECRET_SETUP`.
- Подключить DeepSeek / DeepSig review только после `APPROVE_SECRET_SETUP`.
- До approval использовать только mock/disabled providers.
- Не читать `.env`, токены и ключи.
- Не запускать внешние API без отдельного gate.

## Telegram

- Расширить dry-run команды.
- Подготовить live approval gate.
- Не запускать polling/webhook.
- Не читать Telegram token.

## Malyarka

- Разработать parser contract.
- Добавить order preview.
- Добавить dispute workflow.
- Добавить validation layer.
- Расширить synthetic fixtures.
- Усилить export gate.
- Не читать реальные заказы.
- Не экспортировать реальные Excel-файлы.

## Google Drive

- Решить `403 appNotAuthorizedToFile`.
- Ручной или повторно авторизованный перенос LOW-документов только после отдельного решения.
- Не выполнять Google Drive write/move внутри safe local пакетов.

## Max Safe Local Package Queue

- BATCH_063_SAFE_LOCAL_MALYARKA_FULL_HARDENING_PACK
- BATCH_064_SAFE_LOCAL_FINAL_REFRESH_AFTER_MALYARKA_FULL_HARDENING
- BATCH_065_SAFE_LOCAL_RUNTIME_SAFETY_GATE_AND_AUDIT_LOG
- BATCH_066_SAFE_LOCAL_TELEGRAM_DRY_RUN_DEEPENING_PACK
- BATCH_067_SAFE_LOCAL_AI_PROVIDER_MOCK_AND_SECRET_GATE_HARDENING
- BATCH_068_SAFE_LOCAL_PROJECT_AUDIT_AND_COMMAND_COVERAGE_MAX
- BATCH_069_SAFE_LOCAL_DASHBOARD_AND_DAILY_REPORT_MAX
- BATCH_070_SAFE_LOCAL_DOCS_POLISH_AND_USER_RUNBOOK
- BATCH_071_SAFE_LOCAL_RELEASE_CANDIDATE_PREP
- BATCH_072_SAFE_LOCAL_FINAL_MASTER_REFRESH_AND_NEXT_DECISION

## Next 10 After BATCH_063C

- BATCH_073_SAFE_LOCAL_MALYARKA_VALIDATION_REFRESH
- BATCH_074_SAFE_LOCAL_MALYARKA_ORDER_STATE_MACHINE
- BATCH_075_SAFE_LOCAL_MALYARKA_PREVIEW_REPORT_MAX
- BATCH_076_SAFE_LOCAL_TELEGRAM_MALYARKA_DIALOG_FLOW
- BATCH_077_SAFE_LOCAL_TASK_QUEUE_AND_AUTO_NEXT_HARDENING
- BATCH_078_SAFE_LOCAL_MEMORY_DECISIONS_AND_PROHIBITIONS_SYNC
- BATCH_079_SAFE_LOCAL_SECRET_AND_ENV_GUARD_MAX
- BATCH_080_SAFE_LOCAL_GOOGLE_DRIVE_BLOCKED_STATUS_FREEZE
- BATCH_081_SAFE_LOCAL_RELEASE_CANDIDATE_V2
- BATCH_082_SAFE_LOCAL_NEXT_DIRECTION_DECISION_MENU
