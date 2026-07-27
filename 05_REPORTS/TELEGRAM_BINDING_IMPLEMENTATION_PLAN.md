# TELEGRAM_BINDING_IMPLEMENTATION_PLAN

Дата: 2026-07-03
Исполнитель: Codex

## Цель

Подключить Hermes-Clean / Malyarka direct intents к существующему live Telegram gateway без второго polling.

Текущий live runner:

- `hermes gateway run`
- CWD: `[удалённый архив]`
- Telegram adapter: `C:\Users\user\AppData\Local\hermes\hermes-agent\plugins\platforms\telegram\adapter.py`
- Gateway runner: `C:\Users\user\AppData\Local\hermes\hermes-agent\gateway\run.py`

Исправленный Malyarka router:

- `[удалённый архив]`

## Выбранный binding

Выбран Hermes plugin с hook:

`pre_gateway_dispatch`

Причина:

- hook уже вызывается в `GatewayRunner._handle_message`;
- hook вызывается до generic agent dispatch/fallback;
- hook получает `event`, `gateway`, `session_store`;
- hook может вернуть `{"action": "skip"}`, чтобы остановить generic fallback;
- ответ можно отправить через уже живой adapter из `gateway.adapters[event.source.platform]`;
- второй Telegram polling не нужен.

## Где будет hook

Новый plugin:

`C:\Users\user\AppData\Local\hermes\hermes-agent\plugins\hermes-clean-gateway-binding`

Файлы:

- `plugin.yaml`
- `__init__.py`

Core Hermes gateway файлы не меняются:

- `gateway\run.py` не меняется;
- `plugins\platforms\telegram\adapter.py` не меняется.

## Как gateway передаст text/chat_id

`pre_gateway_dispatch` получает Hermes `MessageEvent`.

Из него используются:

- `event.text`;
- `event.source.platform`;
- `event.source.chat_id`;
- `event.source.user_id`;

Plugin обрабатывает только:

- platform `telegram`;
- non-internal user-originated messages;
- текстовые сообщения с непустым `event.text`.

Owner check оставляется за текущим Hermes gateway authorization layer. Дополнительно plugin не расширяет доступ и не читает токены.

## Как подключается Malyarka router

Plugin добавляет в `sys.path` только project root:

`[удалённый архив]`

Затем импортирует:

- `malyarka_telegram.router.answer_free_text`

Импорт выполняется без чтения `.env` и без токенов.

## Как возвращается response

Если `answer_free_text(text)` возвращает прямой Hermes-Clean/Malyarka response, plugin:

1. получает live adapter из `gateway.adapters[event.source.platform]`;
2. планирует async отправку `adapter.send(event.source.chat_id, response)`;
3. возвращает `{"action": "skip", "reason": "hermes_clean_gateway_binding"}`;
4. generic Hermes fallback не запускается.

Если direct response нет, plugin возвращает `{"action": "allow"}` или `None`, и generic Hermes fallback остается последним.

## Route order

Фактический порядок после binding:

1. Telegram adapter принимает update в существующем polling.
2. Hermes gateway вызывает `pre_gateway_dispatch`.
3. Hermes-Clean binding проверяет Telegram text.
4. Hermes-Clean / Malyarka router обрабатывает:
   - status;
   - next step;
   - order intake;
   - correction;
   - price draft;
   - LKM draft;
   - backup request;
   - hard safety blocked phrases.
5. Если обработано, plugin отправляет ответ и возвращает `skip`.
6. Если не обработано, generic Hermes Agent fallback работает как раньше.

## Rollback

Rollback без удаления:

1. Восстановить plugin files из backup или отключить plugin отдельным согласованным действием.
2. Восстановить измененные файлы из:
   `C:\Users\user\Desktop\Hermes-Clean\backup_before_telegram_gateway_binding_20260703_234433`
3. Перезапустить gateway только после отдельного approval.

Так как core gateway и Telegram adapter не меняются, rollback минимальный: убрать/отключить plugin binding и перезапустить gateway.

## Локальные тесты

До live restart:

- `Покажи статус` -> Hermes-Clean status;
- `Что дальше?` -> Hermes-Clean next step;
- `Есть заказ: Тест binding, МДФ 19 мм, RAL 9005, покраска, 720x400 2 шт` -> Malyarka preview;
- `Поставь цену 25 000 как draft` -> price draft;
- `PGP301 + тестовый профиль = 777 как draft` -> LKM draft;
- `Удали файл` -> BLOCKED;
- unknown phrase -> generic fallback remains allowed.

## Live restart

На этом этапе live gateway не останавливается и не перезапускается.

После локальных тестов нужен отдельный approval на restart существующего `hermes gateway run`.
