# План fake adapter / локального test double для Hermes adapter

Дата: 2026-06-15

Статус: план. Код fake adapter не писался. Pytest-файлы не создавались. Live Telegram-бот, сервер, token, `.env`, `config.py`, Vision/API, staging-код и реальные заказы не трогались.

## Цель

Спроектировать fake adapter / локальный test double для будущего Hermes adapter layer серверного Telegram-бота.

Fake adapter нужен, чтобы позже безопасно проверять contract tests локально:

* без live-бота;
* без сервера;
* без token;
* без `.env`;
* без `config.py`;
* без импорта модулей бота;
* без изменения существующего кода.

## Что такое fake adapter

Fake adapter — это будущий локальный test double, который имитирует ответы Hermes adapter по заранее заданным сценариям.

Он нужен только для проверки контракта:

* какие input-поля ожидаются;
* какие output-поля возвращаются;
* какие actions разрешены;
* какие actions блокируются;
* как включается fallback;
* как diagnostics остаются безопасными;
* как feature flags блокируют опасные ветки.

Fake adapter не является live Hermes adapter.

## Что fake adapter НЕ делает

Fake adapter не должен:

* подключаться к Telegram;
* читать token;
* читать `.env`;
* читать `config.py`;
* читать переменные окружения;
* импортировать live bot modules;
* импортировать `malyarka_telegram`;
* импортировать `malyarka_core`;
* запускать polling;
* запускать webhook;
* запускать subprocess;
* вызывать API;
* менять существующий серверный бот;
* читать серверные файлы;
* читать staging-код без отдельного разрешения;
* создавать файлы export;
* менять цены;
* менять правила;
* менять базу;
* трогать реальные заказы.

## Где fake adapter должен жить в будущей архитектуре

На этапе планирования fake adapter существует только как идея для локальных tests.

Будущая логическая схема:

```text
contract test
-> fake adapter
-> fake output
-> contract validator
-> fallback / accepted dry-run result
```

Это не live path:

```text
Telegram -> app.py -> router.py / handlers.py -> Hermes adapter
```

Fake adapter не должен подменять live-бот и не должен попадать в polling.

## Fake scenarios

### Safe allowed action

Fake adapter возвращает разрешённый action, например:

```text
answer_text
suggest_mode
explain_status
prepare_engineer_task_draft
summarize_project_state
explain_order_result
suggest_next_safe_step
```

Ожидание:

* output проходит contract validation;
* side effects отсутствуют;
* fallback не нужен, если остальные поля безопасны.

### Forbidden action

Fake adapter возвращает запрещённый action:

```text
send_telegram_message
create_file
edit_file
delete_file
change_price
change_rules
change_database
run_polling
restart_bot
read_token
read_env
call_api
process_real_order_files
```

Ожидание:

* output блокируется;
* `fallback_required=true`;
* старый Telegram flow должен продолжать работу;
* side effects запрещены.

### Unknown action

Fake adapter возвращает action вне allowlist и вне known forbidden list.

Ожидание:

* action считается запрещённым;
* output игнорируется;
* fallback включается.

### Empty output

Fake adapter возвращает:

```text
{}
null
empty string
```

Ожидание:

* contract violation;
* fallback;
* без stack trace и без секретов в diagnostics.

### Missing required fields

Fake adapter возвращает output без одного или нескольких обязательных полей:

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

Ожидание:

* output не принимается;
* fallback включается;
* следующий этап блокируется до исправления контракта.

### Wrong field types

Fake adapter возвращает неверные типы:

* `warnings` как строку вместо списка;
* `diagnostics` как строку вместо структуры;
* `fallback_required` как строку вместо boolean;
* `export_allowed` как команду вместо статуса;
* `engineer_task_draft` как исполняемое действие вместо черновика.

Ожидание:

* output блокируется;
* side effects нет.

### Unsafe diagnostics

Fake adapter возвращает diagnostics с опасными данными:

* token;
* `.env`;
* переменные окружения;
* API keys;
* database paths;
* реальные заказы;
* реальные `.cdr/.art/.xlsx`;
* команды polling/restart;
* server commands;
* логи;
* личные данные.

Ожидание:

* diagnostics блокируются;
* output не используется;
* fallback включается.

### fallback_required=true

Fake adapter явно возвращает:

```text
fallback_required=true
```

Ожидание:

* contract validator уважает fallback;
* adapter response не исполняется как команда;
* старый Telegram flow продолжает работу.

### Adapter off by default

Feature flags:

```text
HERMES_ADAPTER_ENABLED=false
HERMES_SAFE_MODE=true
```

Ожидание:

* fake adapter не влияет на flow;
* output игнорируется или остаётся dry-run only;
* diagnostics показывает adapter off.

### Feature flags blocking export/admin/write actions

Feature flags:

```text
HERMES_EXPORT_CALLBACKS_ENABLED=false
HERMES_ADMIN_CHANGES_ENABLED=false
HERMES_ENGINEER_MODE_ENABLED=false или dry-run only
HERMES_SAFE_MODE=true
```

Ожидание:

* export actions не создают файлы;
* admin changes blocked;
* write actions blocked;
* engineer flow только draft;
* цены, материалы, правила и база не меняются.

## Fake outputs

### Valid output

Пример логической формы:

```text
status: ok
action: answer_text
response_text: safe text
warnings: []
blocked_reason: null
suggested_next_step: safe next step
export_allowed: false
engineer_task_draft: null
diagnostics: safe diagnostics
fallback_required: false
```

### Blocked output

```text
status: blocked
action: change_price
blocked_reason: action is forbidden in dry-run
fallback_required: true
```

### Unsafe output

Output содержит опасные поля или diagnostics с секретами.

Ожидание:

```text
output ignored
fallback_required=true
unsafe diagnostics blocked
```

### Malformed output

Output пустой, неполный или с неправильными типами.

Ожидание:

```text
contract violation
fallback_required=true
```

### Fallback output

```text
status: fallback_required
action: suggest_next_safe_step
fallback_required: true
diagnostics: adapter unavailable / off / unsafe
```

## Как fake adapter помогает contract tests

Fake adapter позволяет проверить contract validator без live-бота:

* разрешённые actions проходят;
* запрещённые actions блокируются;
* unknown action блокируется;
* diagnostics очищаются от секретов;
* feature flags работают;
* fallback включается;
* adapter off by default не влияет на flow;
* admin/write/export ветки не выполняются.

Это безопасный промежуточный слой перед любым реальным adapter.

## Запрещённые side effects

В fake adapter и будущих contract tests должны быть запрещены:

* отправка Telegram-сообщений;
* создание файлов;
* редактирование файлов;
* удаление файлов;
* изменение цен;
* изменение правил;
* изменение базы;
* запуск polling;
* restart bot;
* чтение token;
* чтение `.env`;
* чтение `config.py`;
* вызов API;
* обработка реальных файлов заказа;
* commit/push.

## Детерминированные поля

Fake adapter должен возвращать детерминированные значения, чтобы tests были повторяемыми.

Детерминированными должны быть:

* `status`;
* `action`;
* `warnings`;
* `blocked_reason`;
* `suggested_next_step`;
* `export_allowed`;
* `engineer_task_draft`;
* `diagnostics`;
* `fallback_required`.

`response_text` тоже должен быть стабильным для каждого fake scenario.

Нельзя использовать:

* реальные token;
* текущие переменные окружения;
* реальные server paths;
* случайные внешние ответы;
* live API;
* данные реальных заказов.

## Как отличить dry-run результат от реального действия

Dry-run result должен явно содержать признаки:

```text
status: dry_run_only / ok / blocked / fallback_required
diagnostics.dry_run: true
diagnostics.side_effects: false
diagnostics.live_telegram: false
diagnostics.files_changed: false
diagnostics.external_actions_started: false
```

Если result предлагает реальное действие, оно не должно исполняться. Оно может быть только:

* объяснением;
* черновиком;
* следующим безопасным шагом;
* blocked reason.

## Почему следующий этап требует отдельного разрешения

Следующий этап — реализация локального fake adapter и focused contract tests.

Он требует отдельного разрешения, потому что там уже появятся:

* код fake adapter;
* pytest-файлы;
* contract validator или test helpers;
* локальный запуск tests.

Даже если это безопасный локальный слой, его нужно вводить отдельным техническим пакетом.

## Следующий безопасный шаг

После этого плана безопасный следующий шаг:

```text
Серия 187-190 — Реализация локального fake adapter и focused contract tests
```

Техническое имя:

```text
BATCH_SERIES_187_190_HERMES_ADAPTER_FAKE_ADAPTER_TEST_DOUBLE_IMPLEMENTATION
```

Только после отдельного разрешения пользователя.
