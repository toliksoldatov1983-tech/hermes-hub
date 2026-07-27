# TELEGRAM_GATEWAY_BINDING_REPORT

Дата: 2026-07-03
Исполнитель: Codex

## Финальный статус

`TELEGRAM_GATEWAY_BINDING_LOCAL_READY_PENDING_RESTART`

Binding реализован локально. Live gateway не остановлен и не перезапущен.

## Backup

Создан backup перед изменениями:

`C:\Users\user\Desktop\Hermes-Clean\backup_before_telegram_gateway_binding_20260703_234433`

В backup включены:

- Hermes Telegram adapter;
- Hermes gateway runner/config/base platform files;
- Hermes config.yaml;
- Malyarka router/handlers/safety;
- Hermes-Clean state/report files.

`config.yaml` был скопирован без печати содержимого.

## Найденный hook/plugin API

Hermes gateway уже поддерживает hook:

`pre_gateway_dispatch`

Файл вызова:

`C:\Users\user\AppData\Local\hermes\hermes-agent\gateway\run.py`

Hook вызывается в `GatewayRunner._handle_message` до generic agent dispatch/fallback.

Формат результатов:

- `{"action": "skip"}` -> остановить generic dispatch;
- `{"action": "rewrite", "text": "..."}` -> заменить текст и продолжить;
- `{"action": "allow"}` или `None` -> обычный generic dispatch.

## Выбранный binding

Создан standalone Hermes plugin:

`C:\Users\user\AppData\Local\hermes\hermes-agent\plugins\hermes-clean-gateway-binding`

Файлы plugin:

- `plugin.yaml`
- `__init__.py`

Plugin включен в:

`C:\Users\user\AppData\Local\hermes\config.yaml`

Добавлен allow-list:

```yaml
plugins:
  enabled:
    - hermes-clean-gateway-binding
```

Core gateway/adapter не менялись:

- `gateway\run.py` не изменен;
- `plugins\platforms\telegram\adapter.py` не изменен.

## Как работает route order

После будущего restart существующего `hermes gateway run` порядок будет:

1. Existing Telegram polling принимает update.
2. Telegram adapter передает `MessageEvent` в generic Hermes gateway.
3. `pre_gateway_dispatch` вызывает `hermes-clean-gateway-binding`.
4. Plugin fail-closed проверяет:
   - platform = `telegram`;
   - message не internal;
   - text не пустой;
   - `gateway._is_user_authorized(source)` возвращает `True`.
5. Plugin подключает `[удалённый архив]` в `sys.path`.
6. Plugin вызывает Malyarka/Hermes-Clean local router logic:
   - hard safety gate;
   - Hermes-Clean direct intents;
   - order-like preview.
7. Если фраза обработана, plugin отправляет ответ через уже живой `gateway.adapters[event.source.platform].send(...)` и возвращает `skip`.
8. Если фраза не обработана, plugin возвращает `allow`, и generic Hermes fallback остается последним.

Второй Telegram polling не запускается.

## Что обрабатывается до generic fallback

- `Покажи статус`
- `Статус`
- `Как дела по проекту`
- `Статус Hermes`
- `Статус Малярки`
- `Что дальше?`
- order-like текст с размером;
- correction intent;
- price draft;
- LKM draft;
- backup request;
- dangerous text через hard safety response.

Unknown phrase не потребляется plugin и остается для generic Hermes fallback.

## Измененные файлы

- `C:\Users\user\AppData\Local\hermes\hermes-agent\plugins\hermes-clean-gateway-binding\plugin.yaml`
- `C:\Users\user\AppData\Local\hermes\hermes-agent\plugins\hermes-clean-gateway-binding\__init__.py`
- `C:\Users\user\AppData\Local\hermes\config.yaml`
- `C:\Users\user\Desktop\Hermes-Clean\05_REPORTS\TELEGRAM_BINDING_IMPLEMENTATION_PLAN.md`
- `C:\Users\user\Desktop\Hermes-Clean\05_REPORTS\TELEGRAM_GATEWAY_BINDING_REPORT.md`

## Локальные тесты

Compile:

- `py_compile` plugin + Malyarka router/handlers/safety: passed.

Plugin discovery:

- `pre_gateway_dispatch_callbacks=1`
- `hermes_clean_binding_loaded=True`
- `plugin_enabled=True`
- `plugin_error=None`

Hook-level fake gateway test:

- `Покажи статус` -> `skip`, response sent through adapter;
- unknown phrase -> `allow`, no direct response sent.

Required routing tests:

- `Покажи статус` -> Hermes-Clean status: passed;
- `Что дальше?` -> Hermes-Clean next step: passed;
- `Есть заказ: Тест binding, МДФ 19 мм, RAL 9005, покраска, 720x400 2 шт` -> Malyarka preview: passed;
- `Поставь цену 25 000 как draft` -> price draft: passed;
- `PGP301 + тестовый профиль = 777 как draft` -> LKM draft: passed;
- `Удали файл` -> BLOCKED/safety response: passed;
- unknown phrase -> generic fallback allowed: passed.

Status aliases:

- `Покажи статус`: passed;
- `Статус`: passed;
- `Как дела по проекту`: passed;
- `Статус Hermes`: passed;
- `Статус Малярки`: passed.

Focused pytest:

- `tests\test_malyarka_telegram_router.py`
- `tests\test_malyarka_telegram_router_integration.py`
- `tests\test_malyarka_telegram_intent.py`
- Result: `145 passed`.

## Что не выполнялось

- Live gateway не останавливался.
- Live gateway не перезапускался.
- Новый polling не запускался.
- Live Telegram tests не выполнялись.
- `.env` и token values не читались и не показывались.
- Google Drive, Vision, production database, `E:\РАБОТА`, CorelDRAW, ArtCAM, CNC не трогались.
- `bot_archive_20260703.py` не трогался.
- `git push`, delete, reset, clear, prune не выполнялись.

## Rollback

До restart:

1. Убрать `hermes-clean-gateway-binding` из `plugins.enabled` в `C:\Users\user\AppData\Local\hermes\config.yaml`.
2. Оставить plugin files на месте или отключить их отдельным согласованным действием.
3. Live restart не нужен, если live gateway еще не перезапускался после binding.

После restart:

1. Восстановить `config.yaml` из:
   `C:\Users\user\Desktop\Hermes-Clean\backup_before_telegram_gateway_binding_20260703_234433`
2. Перезапустить только подтвержденный `hermes gateway run` после отдельного approval.

Core gateway/adapter rollback не нужен, потому что core files не менялись.

## Нужен ли live restart

Да. Binding уже включен в config, но текущий live gateway process был запущен до появления plugin.

Чтобы binding начал работать в Telegram, нужен отдельный approval на безопасный restart существующего `hermes gateway run`.

До этого live Telegram останется на старом process state.
