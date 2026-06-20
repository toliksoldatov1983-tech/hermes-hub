# План dry-run contract для Hermes adapter

Дата: 2026-06-15

Статус: план. Код не писался. Сервер, live-бот, polling, token, `.env`, `config.py`, Vision и API не трогались.

## Цель

Описать безопасный контракт будущего Hermes adapter без внедрения в live-бот и без изменения кода.

Контракт нужен, чтобы заранее определить:

* что adapter может получать;
* что adapter может возвращать;
* какие действия разрешены в dry-run;
* какие действия запрещены;
* как бот должен валидировать результат adapter;
* когда включается fallback.

## Источники

Использованы только локальные документы:

* `E:\Hermes-Hub\handoff\HERMES_NAVIGATION_INDEX.md`;
* `E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_LAYER_PLAN.md`;
* `E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_LAYER_PLAN_SUMMARY.md`;
* `E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_FLAGS_DIAGNOSTICS_ROLLBACK_PLAN.md`;
* `E:\Hermes-Hub\docs\SERVER_TELEGRAM_BOT_ARCHITECTURE_MAP.md`.

Большой `CHATGPT_CONTEXT_BUNDLE.md` полностью не читался.

## Dry-run принцип

Dry-run adapter:

* ничего не меняет;
* не отправляет Telegram-сообщения сам;
* не создаёт файлы;
* не редактирует файлы;
* не удаляет файлы;
* не запускает внешние действия;
* не читает token;
* не читает `.env`;
* не читает `config.py`;
* не трогает базу;
* не вызывает Vision/API;
* не запускает polling;
* не перезапускает бота.

Dry-run может только анализировать безопасный входной контекст и возвращать безопасное предложение, объяснение, диагностику или черновик.

## Adapter input

Будущий dry-run adapter должен принимать безопасную структуру input:

```text
text
user_id
current_mode
route_result
order_preview
owner_access_status
feature_flags
safe_context_summary
```

### Поля input

`text`

Текст пользователя. На будущих этапах может потребоваться redaction или сокращение, если текст содержит личные данные.

`user_id`

Идентификатор пользователя. В dry-run не должен раскрывать token, owner_id или личные данные.

`current_mode`

Текущий режим Telegram-бота: например, order, chat, engineer, admin, neutral.

`route_result`

Безопасный результат маршрутизации из `router.py`: action, mode decision, access decision, но без секретов.

`order_preview`

Безопасное представление результата заказа, если оно уже построено текущим flow. Не должно включать реальные файлы или приватные данные.

`owner_access_status`

Только безопасный статус: разрешён / запрещён / неизвестно. Не должен содержать owner_id.

`feature_flags`

Текущие значения безопасных flags:

* `HERMES_ADAPTER_ENABLED`;
* `HERMES_ASSISTANT_MODE_ENABLED`;
* `HERMES_ENGINEER_MODE_ENABLED`;
* `HERMES_ADMIN_CHANGES_ENABLED`;
* `HERMES_EXPORT_CALLBACKS_ENABLED`;
* `HERMES_SAFE_MODE`.

`safe_context_summary`

Короткий безопасный контекст проекта без секретов, token, `.env`, баз, логов и приватных данных.

## Adapter output

Будущий dry-run adapter должен возвращать безопасную структуру output:

```text
status
response_text
action
warnings
blocked_reason
suggested_next_step
export_allowed
engineer_task_draft
diagnostics
fallback_required
```

### Поля output

`status`

Один из безопасных статусов:

* `ok`;
* `blocked`;
* `dry_run_only`;
* `fallback_required`;
* `error`.

`response_text`

Текст, который можно показать пользователю только после safety validation.

`action`

Предлагаемое dry-run действие. Должно входить в whitelist разрешённых actions.

`warnings`

Список предупреждений без секретов и личных данных.

`blocked_reason`

Причина блокировки, если action запрещён или небезопасен.

`suggested_next_step`

Следующий безопасный шаг, например: уточнить режим, создать черновик задачи, открыть plan, попросить подтверждение владельца.

`export_allowed`

Только boolean/статус. В dry-run не создаёт файл и не отправляет документ.

`engineer_task_draft`

Черновик инженерной задачи. Не является разрешением на выполнение.

`diagnostics`

Безопасная диагностика: flags, mode, fallback status, adapter status. Без token, `.env`, owner_id, заказов целиком, баз и логов.

`fallback_required`

Boolean, который явно говорит старому flow игнорировать adapter output и идти по текущей логике.

## Разрешённые dry-run actions

В dry-run разрешены только безопасные действия:

* `answer_text`;
* `suggest_mode`;
* `explain_status`;
* `prepare_engineer_task_draft`;
* `summarize_project_state`;
* `explain_order_result`;
* `suggest_next_safe_step`.

Эти actions не должны менять файлы, запускать процессы, отправлять сообщения напрямую или создавать export.

## Запрещённые actions

Dry-run adapter не имеет права возвращать к исполнению:

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

Если adapter вернул любое из этих действий, результат считается небезопасным.

## Safety validation

Перед использованием output старый Telegram flow должен выполнить safety validation.

Проверки:

1. `action` входит в whitelist разрешённых dry-run actions.
2. `fallback_required` не конфликтует с `status`.
3. `response_text` не содержит token, `.env`, секреты, stack trace, личные данные.
4. `diagnostics` не содержит token, owner_id, `.env`, переменные окружения, базы, логи.
5. `export_allowed` не приводит к созданию файла.
6. `engineer_task_draft` остаётся черновиком и не выполняется.
7. `status=blocked` не должен выполнять action.
8. Любое неизвестное action считается запрещённым.

Если adapter возвращает запрещённое действие, бот должен:

```text
игнорировать adapter output
использовать fallback
не выполнять action
не менять файлы
не запускать внешние действия
```

## Fallback

Fallback включается, если:

* adapter недоступен;
* adapter упал;
* adapter вернул `status=error`;
* adapter вернул неизвестный status;
* adapter вернул запрещённый action;
* diagnostics небезопасны;
* output содержит подозрительные данные;
* feature flags запрещают действие;
* owner/access status не разрешает engineer/admin flow.

Fallback означает:

```text
старый Telegram flow продолжает работать как раньше
Hermes output игнорируется
live polling не перезапускается
token/.env/config.py не читаются
файлы не создаются
база не меняется
```

## Contract examples

### Обычный вопрос пользователя

Input:

```text
text: "Что умеет бот?"
current_mode: chat
feature_flags: safe mode on, adapter dry-run
```

Output:

```text
status: ok
action: answer_text
response_text: короткое безопасное объяснение
fallback_required: false
```

### Запрос "что дальше по проекту"

Output:

```text
status: ok
action: suggest_next_safe_step
suggested_next_step: показать следующий безопасный план
fallback_required: false
```

### Запрос "сделай задачу Codex"

Output:

```text
status: dry_run_only
action: prepare_engineer_task_draft
engineer_task_draft: черновик задачи для проверки владельцем
fallback_required: false
```

Важно: задача не отправляется в Codex автоматически и не выполняется без подтверждения.

### Запрос на изменение цены

Output:

```text
status: blocked
action: prepare_engineer_task_draft
blocked_reason: изменение цены требует admin/engineer flow, подтверждения владельца, истории и отката
fallback_required: false
```

Цена не меняется. Можно подготовить только черновик.

### Запрос на Excel

Output:

```text
status: dry_run_only
action: explain_order_result
export_allowed: true/false/unknown
suggested_next_step: использовать существующий safe export flow
fallback_required: false
```

Adapter не создаёт Excel напрямую. Excel допускается только через существующий безопасный flow и отдельные flags.

## Будущие этапы

Порядок после этого документа:

1. Contract document.
2. Локальный contract test.
3. Fake adapter.
4. Dry-run adapter off by default.
5. Live integration plan.

До live integration должны быть готовы:

* tests для allowed/forbidden actions;
* tests для fallback;
* diagnostics без секретов;
* redaction;
* feature flags;
* rollback checklist;
* отдельное разрешение пользователя.

## Что сейчас не разрешается

Этот план не разрешает:

* писать код adapter;
* подключаться к серверу;
* читать серверные файлы;
* менять код бота;
* запускать collector;
* читать token;
* читать `.env`;
* читать `config.py`;
* запускать polling;
* останавливать или перезапускать бота;
* трогать Vision/API;
* создавать файлы;
* менять цены, правила, базу или реальные заказы.

## Следующий безопасный шаг

После этого плана безопасный следующий шаг:

```text
Серия 179-182 — План локального contract test для Hermes adapter
```

Техническое имя:

```text
BATCH_SERIES_179_182_HERMES_ADAPTER_CONTRACT_TEST_PLAN
```

Цель следующего шага: спланировать локальные проверки dry-run contract без live-бота и без изменения серверного кода.
