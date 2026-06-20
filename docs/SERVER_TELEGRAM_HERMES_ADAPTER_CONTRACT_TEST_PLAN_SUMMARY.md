# Краткое резюме contract test plan для Hermes adapter

Дата: 2026-06-15

## Суть

План описывает будущие локальные contract tests для Hermes adapter. Код и pytest-файлы сейчас не создаются.

## Что должны проверять tests

* input-поля: `text`, `user_id`, `current_mode`, `route_result`, `order_preview`, `owner_access_status`, `feature_flags`, `safe_context_summary`;
* output-поля: `status`, `response_text`, `action`, `warnings`, `blocked_reason`, `suggested_next_step`, `export_allowed`, `engineer_task_draft`, `diagnostics`, `fallback_required`;
* разрешённые actions;
* запрещённые actions;
* unknown action;
* отсутствующие поля;
* неправильные типы;
* пустой output;
* опасные лишние поля;
* fallback;
* diagnostics без секретов;
* adapter off by default;
* feature flags.

## Разрешённые actions

* `answer_text`;
* `suggest_mode`;
* `explain_status`;
* `prepare_engineer_task_draft`;
* `summarize_project_state`;
* `explain_order_result`;
* `suggest_next_safe_step`.

## Запрещённые actions

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

## Главное правило

Если output небезопасен, неизвестен или нарушает контракт, он игнорируется, а старый Telegram flow продолжает работать через fallback.

## Следующий безопасный шаг

Серия 183-186 — План fake adapter / локального test double для Hermes adapter

Техническое имя:

`BATCH_SERIES_183_186_HERMES_ADAPTER_FAKE_ADAPTER_TEST_DOUBLE_PLAN`
