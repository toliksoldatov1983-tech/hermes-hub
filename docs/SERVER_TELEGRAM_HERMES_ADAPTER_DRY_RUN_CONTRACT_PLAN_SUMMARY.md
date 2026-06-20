# Краткое резюме dry-run contract для Hermes adapter

Дата: 2026-06-15

## Принцип

Dry-run adapter ничего не меняет, не отправляет сообщения, не создаёт файлы и не запускает внешние действия.

Он только анализирует безопасный input и возвращает безопасное предложение, объяснение, диагностику или черновик.

## Input contract

Adapter input:

* `text`;
* `user_id`;
* `current_mode`;
* `route_result`;
* `order_preview`;
* `owner_access_status`;
* `feature_flags`;
* `safe_context_summary`.

## Output contract

Adapter output:

* `status`;
* `response_text`;
* `action`;
* `warnings`;
* `blocked_reason`;
* `suggested_next_step`;
* `export_allowed`;
* `engineer_task_draft`;
* `diagnostics`;
* `fallback_required`.

## Разрешённые actions

Разрешены только:

* `answer_text`;
* `suggest_mode`;
* `explain_status`;
* `prepare_engineer_task_draft`;
* `summarize_project_state`;
* `explain_order_result`;
* `suggest_next_safe_step`.

## Запрещённые actions

Запрещены:

* `send_telegram_message`;
* `create_file`;
* `edit_file`;
* `delete_file`;
* `change_price`;
* `change_rules`;
* `change_database`;
* `run_polling`;
* `restart_bot`;
* `read_token`;
* `read_env`;
* `call_api`;
* `process_real_order_files`.

## Safety validation и fallback

Если adapter возвращает запрещённое действие, неизвестный status, небезопасные diagnostics или подозрительные данные, бот должен игнорировать adapter output и использовать fallback.

Fallback означает: старый Telegram flow продолжает работать как раньше.

## Следующий безопасный шаг

Серия 179-182 — План локального contract test для Hermes adapter

Техническое имя:

`BATCH_SERIES_179_182_HERMES_ADAPTER_CONTRACT_TEST_PLAN`
