# Краткое резюме плана Hermes adapter layer

Дата: 2026-06-15

## Главная идея

Hermes Hub нельзя сразу внедрять прямой правкой live `app.py`.

Нужен отдельный adapter layer:

```text
Telegram -> app.py -> router.py / handlers.py -> Hermes adapter -> core/services/orders.py
```

Adapter должен быть безопасным промежуточным слоем, который можно включать, выключать и диагностировать без риска для live polling.

## Что adapter принимает

Adapter должен принимать:

* text;
* user_id;
* current_mode;
* route_result;
* order context;
* safe feature flags.

Он не должен принимать token и не должен зависеть от live Telegram runtime.

## Что adapter возвращает

Adapter должен возвращать:

* текст ответа;
* action;
* warnings;
* export availability;
* engineer task draft;
* diagnostics;
* безопасный fallback.

## Feature flags

Предложены flags:

* `HERMES_ADAPTER_ENABLED`;
* `HERMES_ASSISTANT_MODE_ENABLED`;
* `HERMES_ENGINEER_MODE_ENABLED`;
* `HERMES_ADMIN_CHANGES_ENABLED`;
* `HERMES_EXPORT_CALLBACKS_ENABLED`;
* `HERMES_SAFE_MODE`.

Базовая безопасная идея: всё новое выключено, `HERMES_SAFE_MODE=true`.

## Fallback

Если Hermes adapter выключен или упал, старый Telegram-бот должен продолжать работать по текущей логике.

Fallback обязателен, чтобы новый слой не ломал live polling.

## Что нельзя делать adapter-слою

Adapter не должен:

* читать token;
* читать `.env`;
* запускать polling;
* отправлять Telegram-сообщения сам;
* менять серверные файлы;
* трогать базу без отдельного решения;
* менять цены, материалы или правила без подтверждения.

## Следующий безопасный шаг

Серия 171-174 — План feature flags, diagnostics и rollback для Hermes adapter

Техническое имя:

`BATCH_SERIES_171_174_HERMES_ADAPTER_FLAGS_DIAGNOSTICS_ROLLBACK_PLAN`
