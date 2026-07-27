# MAX_SAFE_PACKAGES_FOR_HERMES

## Готовая серия задач

Дать Hermes-Clean/Codex следующую серию:

1. `BATCH_063_SAFE_LOCAL_MALYARKA_FULL_HARDENING_PACK`
2. `BATCH_064_SAFE_LOCAL_FINAL_REFRESH_AFTER_MALYARKA_FULL_HARDENING`
3. `BATCH_065_SAFE_LOCAL_RUNTIME_SAFETY_GATE_AND_AUDIT_LOG`
4. `BATCH_066_SAFE_LOCAL_TELEGRAM_DRY_RUN_DEEPENING_PACK`
5. `BATCH_067_SAFE_LOCAL_AI_PROVIDER_MOCK_AND_SECRET_GATE_HARDENING`
6. `BATCH_068_SAFE_LOCAL_PROJECT_AUDIT_AND_COMMAND_COVERAGE_MAX`
7. `BATCH_069_SAFE_LOCAL_DASHBOARD_AND_DAILY_REPORT_MAX`
8. `BATCH_070_SAFE_LOCAL_DOCS_POLISH_AND_USER_RUNBOOK`
9. `BATCH_071_SAFE_LOCAL_RELEASE_CANDIDATE_PREP`
10. `BATCH_072_SAFE_LOCAL_FINAL_MASTER_REFRESH_AND_NEXT_DECISION`

## Как выполнять

Выполнять подряд крупными пакетами.

Останавливаться только если требуется:

- удаление;
- Google Drive write/move;
- чтение `.env`, токенов, ключей;
- запуск live Telegram;
- запуск внешних AI API;
- реальные заказы;
- архивы или `[удалён]`.

## Что важно

Эта серия специально составлена так, чтобы дать максимум полезной локальной работы без опасных действий.

Все пакеты должны завершаться:

- обновлением task-state;
- отчётом в `05_REPORTS`;
- записью следующего пакета в `NEXT_TASK.md`;
- локальными проверками.
