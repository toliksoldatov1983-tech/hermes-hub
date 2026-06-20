# План локальных contract tests для Hermes adapter

Дата: 2026-06-15

Статус: план. Код не писался. Тесты не реализовывались. Adapter не реализовывался. Сервер, live-бот, polling, token, `.env`, `config.py`, базы, логи, `.git`, Vision/API и существующий код бота не трогались.

## Цель

Спроектировать локальные contract tests для будущего Hermes adapter layer серверного Telegram-бота.

Эти тесты должны проверять не live Telegram и не реальный adapter, а контракт:

* какие input-поля принимает adapter;
* какие output-поля возвращает adapter;
* какие actions разрешены;
* какие actions блокируются;
* как включается fallback;
* как diagnostics остаются безопасными;
* как feature flags удерживают adapter в безопасном режиме.

## Источники

Использовались только локальные документы Hermes Hub по:

* architecture map серверного Telegram-бота;
* Hermes adapter layer;
* flags / diagnostics / rollback;
* dry-run contract.

Серверные файлы, staging-код бота, token, `.env`, `config.py`, базы и логи не читались.

## Что не реализуется

В этой серии не создаются:

* pytest-файлы;
* тестовый код;
* adapter;
* fake adapter;
* subprocess;
* импорты модулей серверного бота;
* live Telegram проверки.

Документ только описывает будущий test plan.

## Проверяемые input-поля

Будущие contract tests должны проверять наличие и базовую форму input:

* `text`;
* `user_id`;
* `current_mode`;
* `route_result`;
* `order_preview`;
* `owner_access_status`;
* `feature_flags`;
* `safe_context_summary`.

Минимальные правила:

* обязательные поля присутствуют;
* типы полей ожидаемые;
* input не содержит token, `.env`, переменные окружения, базу, логи, реальные файлы заказов;
* `owner_access_status` не содержит owner_id;
* `feature_flags` содержит безопасные значения по умолчанию;
* `safe_context_summary` не содержит секреты и личные данные.

## Проверяемые output-поля

Будущие contract tests должны проверять наличие и базовую форму output:

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

Минимальные правила:

* обязательные поля присутствуют;
* `status` входит в ожидаемый набор;
* `action` входит в allowlist или блокируется;
* `warnings` не содержат секреты;
* `blocked_reason` есть для заблокированных действий;
* `export_allowed` не создаёт файлы;
* `engineer_task_draft` остаётся только черновиком;
* `diagnostics` безопасны;
* `fallback_required` корректно включает fallback.

## Разрешённые actions

Будущие tests должны пропускать только эти dry-run actions:

* `answer_text`;
* `suggest_mode`;
* `explain_status`;
* `prepare_engineer_task_draft`;
* `summarize_project_state`;
* `explain_order_result`;
* `suggest_next_safe_step`.

Проверка: каждый разрешённый action считается безопасным только если он не создаёт файлы, не меняет состояние, не отправляет Telegram-сообщения сам и не запускает внешние действия.

## Запрещённые actions

Будущие tests должны блокировать:

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

Проверка: любой запрещённый action должен приводить к:

```text
fallback_required=true
adapter output ignored
no side effects
```

## Группа tests: разрешённые actions

Нужны будущие cases:

1. `answer_text` возвращает безопасный текст.
2. `suggest_mode` только предлагает режим, но не переключает его сам.
3. `explain_status` только объясняет состояние.
4. `prepare_engineer_task_draft` создаёт только черновик.
5. `summarize_project_state` использует только безопасный summary.
6. `explain_order_result` не создаёт Excel/Corel export.
7. `suggest_next_safe_step` возвращает безопасный следующий шаг.

Ожидание: `fallback_required=false`, если output безопасен и flags разрешают dry-run.

## Группа tests: запрещённые actions

Нужны future cases для каждого forbidden action.

Ожидание:

* action блокируется;
* `fallback_required=true`;
* `blocked_reason` заполнен;
* output не используется;
* старый Telegram flow продолжает работу.

Особенно важно:

* `change_price` блокируется;
* `change_rules` блокируется;
* `change_database` блокируется;
* `run_polling` блокируется;
* `restart_bot` блокируется;
* `read_token` блокируется;
* `read_env` блокируется;
* `call_api` блокируется.

## Группа tests: неизвестный action

Если adapter возвращает action вне allowlist и вне known forbidden list, он всё равно считается запрещённым.

Ожидание:

```text
status=blocked или fallback_required=true
blocked_reason содержит unknown action
старый flow продолжает работу
```

## Группа tests: отсутствующие обязательные поля

Нужны cases, где отсутствует каждое обязательное поле input/output.

Ожидание:

* контракт считается нарушенным;
* adapter output игнорируется;
* fallback включается;
* следующий этап блокируется до исправления контракта.

## Группа tests: неправильные типы полей

Нужны cases:

* `text` не строка;
* `user_id` не безопасный идентификатор;
* `feature_flags` не словарь/структура;
* `warnings` не список;
* `diagnostics` не словарь/структура;
* `fallback_required` не boolean;
* `export_allowed` пытается быть командой, а не статусом.

Ожидание: fallback и блокировка output.

## Группа tests: пустой output

Если adapter возвращает пустой output:

```text
{}
null
empty string
```

Ожидание:

* output не используется;
* fallback включается;
* diagnostics фиксирует contract violation без stack trace и секретов.

## Группа tests: лишние опасные поля

Будущие tests должны блокировать output с полями:

* `token`;
* `.env`;
* `env`;
* `environment`;
* `api_key`;
* `password`;
* `private_key`;
* `database_path`;
* `orders_db`;
* `log_path`;
* `polling_command`;
* `restart_command`;
* `server_command`;
* `real_order_files`.

Ожидание: output небезопасен, fallback включается.

## Группа tests: fallback_required=true

Если adapter явно возвращает:

```text
fallback_required=true
```

Ожидание:

* старый Telegram flow продолжает работу;
* adapter response не используется как команда;
* никакие файлы не создаются;
* polling не перезапускается;
* token / `.env` / `config.py` не читаются.

## Группа tests: небезопасные diagnostics

Diagnostics safety tests должны проверять, что diagnostics не содержат:

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

Если diagnostics содержит такое значение, output блокируется.

## Группа tests: adapter off by default

Безопасное состояние по умолчанию:

```text
HERMES_ADAPTER_ENABLED=false
HERMES_SAFE_MODE=true
```

Ожидание:

* adapter не влияет на ответ;
* старый Telegram flow работает как раньше;
* output adapter игнорируется или остаётся dry-run only;
* diagnostics показывает adapter off;
* любые изменения заблокированы.

## Группа tests: feature flags

Проверить flags:

```text
HERMES_ADAPTER_ENABLED=false
HERMES_SAFE_MODE=true
HERMES_EXPORT_CALLBACKS_ENABLED=false
HERMES_ENGINEER_MODE_ENABLED=false или dry-run only
HERMES_ADMIN_CHANGES_ENABLED=false
```

Ожидания:

* export callbacks не создают файлы через adapter;
* engineer/admin-флаги без права записи;
* admin changes всегда blocked;
* safe mode блокирует опасные actions;
* выключенный adapter не меняет live flow.

## Будущие admin-желания

Пользовательские желания будущего admin/engineer flow:

* добавление цен;
* добавление видов фрезеровки;
* добавление материалов;
* добавление цветов;
* изменение правил;
* изменение шаблонов.

В contract tests эти действия должны проверяться как заблокированные.

Разрешён только:

```text
prepare_engineer_task_draft
```

При этом:

* записи нет;
* правила не меняются;
* цены не меняются;
* база не меняется;
* требуется будущий owner confirmation flow.

## Как проверяется fallback на старый Telegram flow

Будущий test plan должен моделировать ситуацию:

* adapter вернул forbidden action;
* adapter вернул unknown action;
* adapter output пустой;
* adapter diagnostics небезопасны;
* adapter off by default;
* feature flags запрещают действие.

Ожидание всегда одно:

```text
старый Telegram flow продолжает работу
Hermes output не исполняется
никаких side effects
```

## Ошибки, которые блокируют следующий этап

Следующий этап нельзя начинать, если contract tests показывают:

* forbidden action проходит как разрешённый;
* unknown action не блокируется;
* diagnostics могут показать token / `.env` / API key / database path;
* `fallback_required=true` не включает fallback;
* adapter off by default всё равно влияет на flow;
* `HERMES_SAFE_MODE=true` не блокирует опасные действия;
* engineer/admin flow может менять данные без owner confirmation;
* output без обязательных полей принимается как валидный;
* неправильные типы не блокируются;
* dry-run может создать файл, изменить базу, вызвать API или перезапустить polling.

## Следующий безопасный шаг

После этого плана безопасный следующий шаг:

```text
Серия 183-186 — План fake adapter / локального test double для Hermes adapter
```

Техническое имя:

```text
BATCH_SERIES_183_186_HERMES_ADAPTER_FAKE_ADAPTER_TEST_DOUBLE_PLAN
```
