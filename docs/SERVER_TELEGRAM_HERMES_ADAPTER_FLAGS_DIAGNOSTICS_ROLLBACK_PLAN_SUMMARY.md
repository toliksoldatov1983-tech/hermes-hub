# Краткое резюме flags / diagnostics / rollback для Hermes adapter

Дата: 2026-06-15

## Feature flags

Нужны flags:

* `HERMES_ADAPTER_ENABLED`;
* `HERMES_ASSISTANT_MODE_ENABLED`;
* `HERMES_ENGINEER_MODE_ENABLED`;
* `HERMES_ADMIN_CHANGES_ENABLED`;
* `HERMES_EXPORT_CALLBACKS_ENABLED`;
* `HERMES_SAFE_MODE`.

Безопасные значения по умолчанию:

```text
всё новое выключено
HERMES_SAFE_MODE=true
старый Telegram-бот работает как раньше
```

## Diagnostics

Diagnostics должна показывать:

* включён ли adapter;
* включены ли assistant/engineer/admin/export modes;
* активен ли safe mode;
* активен ли fallback;
* token configured: да/нет, без значения token;
* owner_id configured: да/нет, без личных данных.

Diagnostics не должна показывать token, `.env`, секреты, переменные окружения, содержимое заказов, личные данные, базы и логи.

## Rollback

Главный rollback:

```text
HERMES_ADAPTER_ENABLED=false
HERMES_SAFE_MODE=true
```

Старый `router.py / handlers.py / core` flow должен продолжать работать.

Нельзя трогать `app.py`, polling, token, `.env` и базу ради rollback.

## Failure modes

Если adapter упал, вернул небезопасное действие, assistant/engineer/export callbacks ошиблись или diagnostics не проходят, включается fallback.

Правило:

```text
если Hermes adapter недоступен или небезопасен, бот обязан продолжить старый безопасный путь
```

## Что не включать первым

Первым этапом нельзя включать:

* admin changes;
* изменение цен;
* изменение правил;
* изменение базы;
* Vision/API;
* live-деплой;
* автоперезапуск polling.

## Следующий безопасный шаг

Серия 175-178 — План dry-run contract для Hermes adapter

Техническое имя:

`BATCH_SERIES_175_178_HERMES_ADAPTER_DRY_RUN_CONTRACT_PLAN`
