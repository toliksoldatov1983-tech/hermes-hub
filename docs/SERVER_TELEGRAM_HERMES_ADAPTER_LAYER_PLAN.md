# План Hermes adapter layer для серверного Telegram-бота

Дата: 2026-06-15

Статус: план. Код не писался. Сервер, live-бот, polling, token, `.env`, `config.py`, Vision и API не трогались.

## Цель

Спроектировать безопасный способ подключить Hermes Hub к существующему серверному Telegram-боту через отдельный adapter layer.

Главный принцип:

```text
не превращать live app.py в экспериментальную площадку
```

Hermes должен подключаться как отдельный слой между Telegram-маршрутизацией и core-логикой, с feature flags, diagnostics, fallback и будущим rollback plan.

## Источники

Использованы только локальные документы:

* `E:\Hermes-Hub\handoff\HERMES_NAVIGATION_INDEX.md`;
* `E:\Hermes-Hub\docs\SERVER_TELEGRAM_BOT_ARCHITECTURE_MAP.md`;
* `E:\Hermes-Hub\docs\SERVER_TELEGRAM_BOT_ARCHITECTURE_MAP_SUMMARY.md`;
* `E:\Hermes-Hub\inputs\server_bot_read_only_copy\SERVER_BOT_READ_ONLY_REPORT.md`;
* `E:\Hermes-Hub\docs\SERVER_BOT_STAGING_CHECK_RESULT.md`.

Большой `CHATGPT_CONTEXT_BUNDLE.md` полностью не читался.

## Где должен стоять adapter

Целевая схема:

```text
Telegram
-> app.py
-> router.py / handlers.py
-> Hermes adapter
-> malyarka_core/services/orders.py
-> parsing / validation / calculations
-> exports / files
```

Adapter не должен быть первым изменением в live `app.py`. Безопаснее спроектировать его как отдельный слой, который можно подключить к уже существующим точкам:

* после определения режима в `router.py`;
* после безопасной текстовой обвязки в `handlers.py`;
* перед вызовом core-сервисов;
* перед export callbacks, но только как diagnostics/decision layer.

## Что adapter должен принимать

Будущий Hermes adapter должен принимать только безопасный контекст, без token и без прямого Telegram runtime:

* `text` — текст сообщения пользователя;
* `user_id` — идентификатор пользователя без раскрытия token;
* `current_mode` — текущий режим Telegram-бота;
* `route_result` — результат маршрутизации из `router.py`;
* `order_context` — безопасный контекст заказа, если он уже собран;
* `safe_feature_flags` — значения безопасных feature flags;
* owner/access status — только как boolean/решение, без секретных значений;
* export status — только доступность/блокировка, без создания файлов на этапе adapter diagnostics.

Adapter не должен зависеть от aiogram напрямую. Это позволит тестировать и диагностировать его отдельно от live Telegram.

## Что adapter должен возвращать

Будущий adapter должен возвращать структурированный безопасный результат:

* текст ответа;
* `action`;
* warnings;
* export availability;
* engineer task draft;
* diagnostics;
* безопасный fallback;
* сведения о том, был ли Hermes реально включён;
* reason, если действие заблокировано.

Пример логической формы результата:

```text
response_text
action
warnings
export_available
engineer_task_draft
diagnostics
fallback_used
block_reason
```

Это не требование к коду сейчас, а целевой контракт для будущего технического этапа.

## Что adapter НЕ должен делать

Hermes adapter не должен:

* читать token;
* читать `.env`;
* читать переменные окружения с token;
* запускать polling;
* запускать Telegram live;
* отправлять Telegram-сообщения сам;
* импортировать старый `bot.py`;
* менять серверные файлы;
* менять live `app.py` без отдельного плана;
* трогать базу без отдельного решения;
* создавать или отправлять файлы без отдельного разрешения;
* менять цены без подтверждения;
* менять материалы без подтверждения;
* менять правила спорных строк без подтверждения;
* менять production workflow без отдельной приёмки.

Adapter должен быть decision/diagnostics layer, а не скрытой автоматизацией live-бота.

## Feature flags

Нужны безопасные feature flags, чтобы новые возможности можно было включать постепенно и выключать без риска для live polling.

Предлагаемые flags:

* `HERMES_ADAPTER_ENABLED` — включает сам adapter layer;
* `HERMES_ASSISTANT_MODE_ENABLED` — включает будущий ассистентский режим;
* `HERMES_ENGINEER_MODE_ENABLED` — включает расширенный инженерный flow;
* `HERMES_ADMIN_CHANGES_ENABLED` — разрешает изменения через admin flow только после подтверждения владельца;
* `HERMES_EXPORT_CALLBACKS_ENABLED` — разрешает Hermes участвовать в export callbacks;
* `HERMES_SAFE_MODE` — принудительно включает максимально безопасный режим.

Базовое безопасное состояние:

```text
HERMES_ADAPTER_ENABLED=false
HERMES_ASSISTANT_MODE_ENABLED=false
HERMES_ENGINEER_MODE_ENABLED=false
HERMES_ADMIN_CHANGES_ENABLED=false
HERMES_EXPORT_CALLBACKS_ENABLED=false
HERMES_SAFE_MODE=true
```

Важно: этот документ не разрешает чтение `.env` или token. Реальный способ хранения flags должен быть спланирован отдельно.

## Fallback

Fallback — обязательное правило.

Если Hermes adapter:

* выключен;
* недоступен;
* вернул ошибку;
* вернул небезопасный action;
* не прошёл owner/access check;
* не прошёл diagnostics;

то старый Telegram-бот должен продолжать работать по текущей логике.

Цель fallback:

```text
новый Hermes layer не должен ломать существующий live polling
```

Fallback должен быть тихим и понятным:

* пользователь получает обычный ответ текущего бота;
* diagnostics фиксирует, что Hermes был пропущен;
* live app.py не падает;
* export callbacks не начинают вести себя иначе без flags.

## Защита режимов

Режимы Telegram-бота нельзя смешивать хаотично.

Правила:

* `/заказ` не ломать;
* `/чат` не должен случайно парсить заказ;
* `/инженер` только через owner/access checks;
* будущий `/ассистент` проектировать отдельно;
* будущий `/админ` только с подтверждением владельца;
* admin changes не должны включаться автоматически;
* neutral mode может уточнять намерение, но не должен выполнять опасные действия;
* export callbacks должны оставаться под явным контролем.

Hermes adapter должен уважать `current_mode` и `route_result`, а не пытаться самостоятельно переопределять весь Telegram UX.

## Будущая хотелка пользователя

Через Telegram в будущем можно будет добавлять и изменять:

* новые виды фрезеровки;
* цены;
* виды работ;
* типы расчётов;
* материалы;
* цвета и покрытия;
* правила спорных строк;
* шаблоны заказов.

Но это разрешено только через безопасный admin/engineer flow:

```text
черновик
-> проверка
-> подтверждение владельца
-> запись
-> история
-> откат
```

До появления такого flow запрещено напрямую менять цены, материалы, правила и производственные настройки через Telegram.

## Diagnostics

Перед любым live-подключением нужен diagnostics layer:

* показывает, включён ли adapter;
* показывает, какие flags активны;
* показывает, какой mode выбран;
* показывает, будет ли использован fallback;
* показывает, доступен ли export;
* не показывает token;
* не показывает owner_id;
* не читает `.env`;
* не запускает polling;
* не меняет файлы.

Diagnostics должен быть безопасным для запуска без token.

## Rollback plan

Перед любым техническим внедрением нужен rollback plan:

* как выключить adapter одним flag;
* как вернуть старую логику без правки live `app.py`;
* как отключить assistant/engineer/admin changes отдельно;
* как отключить Hermes-участие в export callbacks;
* как проверить, что polling продолжает работать;
* как не потерять owner/access ограничения.

Без rollback plan нельзя переходить к изменению live-бота.

## Риски

Основные риски:

* live polling;
* token / `.env` / `config.py`;
* owner/access checks;
* callback-отправка файлов;
* Excel/Corel flow;
* Malyarka file flow;
* archive/storage/db;
* Obsidian;
* missing `malyarka_telegram/models.py`;
* redaction-срабатывания collector;
* случайное изменение UX `/заказ`;
* случайный запуск действий из `/чат`;
* будущие цены/материалы/правила без подтверждения владельца.

Эти риски требуют отдельного плана перед любым кодом.

## Что сейчас не разрешается

Этот план не разрешает:

* подключаться к серверу;
* читать серверные файлы;
* читать `token`;
* читать `.env`;
* читать `config.py`;
* запускать Telegram;
* запускать polling;
* менять код существующего бота;
* менять export-логику;
* подключать Vision/API;
* трогать базу;
* менять реальные заказы.

## Следующий безопасный шаг

После этого плана безопасный следующий шаг:

```text
Серия 171-174 — План feature flags, diagnostics и rollback для Hermes adapter
```

Техническое имя:

```text
BATCH_SERIES_171_174_HERMES_ADAPTER_FLAGS_DIAGNOSTICS_ROLLBACK_PLAN
```

Цель следующего шага: подготовить feature flags / diagnostics / rollback plan без изменения live-бота.
