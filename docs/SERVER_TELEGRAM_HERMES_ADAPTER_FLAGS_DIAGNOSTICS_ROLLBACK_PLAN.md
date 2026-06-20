# План feature flags, diagnostics и rollback для Hermes adapter

Дата: 2026-06-15

Статус: план. Код не писался. Сервер, live-бот, polling, token, `.env`, `config.py`, Vision и API не трогались.

## Цель

Описать, как безопасно включать и выключать будущий Hermes adapter layer, диагностировать его состояние и откатываться к старой логике без поломки live polling.

Главное правило:

```text
новый Hermes adapter не должен становиться single point of failure для существующего Telegram-бота
```

## Источники

Использованы только локальные документы:

* `E:\Hermes-Hub\handoff\HERMES_NAVIGATION_INDEX.md`;
* `E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_LAYER_PLAN.md`;
* `E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_LAYER_PLAN_SUMMARY.md`;
* `E:\Hermes-Hub\docs\SERVER_TELEGRAM_BOT_ARCHITECTURE_MAP.md`;
* `E:\Hermes-Hub\docs\SERVER_TELEGRAM_BOT_ARCHITECTURE_MAP_SUMMARY.md`.

Большой `CHATGPT_CONTEXT_BUNDLE.md` полностью не читался.

## Feature flags

Для будущего adapter layer нужны отдельные flags:

* `HERMES_ADAPTER_ENABLED`;
* `HERMES_ASSISTANT_MODE_ENABLED`;
* `HERMES_ENGINEER_MODE_ENABLED`;
* `HERMES_ADMIN_CHANGES_ENABLED`;
* `HERMES_EXPORT_CALLBACKS_ENABLED`;
* `HERMES_SAFE_MODE`.

## Значения по умолчанию

Безопасные значения по умолчанию:

```text
HERMES_ADAPTER_ENABLED=false
HERMES_ASSISTANT_MODE_ENABLED=false
HERMES_ENGINEER_MODE_ENABLED=false
HERMES_ADMIN_CHANGES_ENABLED=false
HERMES_EXPORT_CALLBACKS_ENABLED=false
HERMES_SAFE_MODE=true
```

Смысл:

* всё новое выключено;
* safe mode включён;
* старый Telegram-бот работает как раньше;
* adapter не вмешивается в route/handlers/core flow;
* export callbacks не меняются;
* admin changes невозможны;
* assistant/engineer dry-run ещё не активны.

Этот документ не разрешает читать `.env`, token или `config.py`. Способ хранения flags должен быть выбран отдельным будущим решением.

## Diagnostics

Безопасная диагностика должна показывать только состояние, а не секреты.

Diagnostics должна показывать:

* adapter включён или выключен;
* assistant mode включён или выключен;
* engineer mode включён или выключен;
* admin changes включены или выключены;
* export callbacks включены или выключены;
* safe mode включён;
* fallback активен;
* token configured: да/нет, но без показа token;
* owner_id configured: да/нет, но без личных данных;
* текущий режим: order/chat/engineer/admin/neutral, если это безопасно;
* adapter status: ok/off/dry_run/error;
* последняя причина fallback, если она не содержит персональных данных.

Diagnostics должна быть безопасной для запуска без token и без live Telegram.

## Что diagnostics не должны показывать

Diagnostics не должны показывать:

* token;
* `.env`;
* секреты;
* переменные окружения;
* содержимое заказов;
* личные данные;
* базы;
* логи;
* приватные ключи;
* реальные пути к секретным файлам;
* значения owner_id;
* тексты сообщений клиентов.

Если diagnostics сомневается, строка должна быть скрыта или заменена безопасной формулировкой.

## Rollback

Rollback должен быть простым и быстрым.

Базовый rollback:

1. Выключить `HERMES_ADAPTER_ENABLED`.
2. Оставить старый `router.py / handlers.py / core` flow.
3. Не трогать `app.py` напрямую.
4. Не менять polling.
5. Не менять token / `.env`.
6. Не менять базу.
7. Не менять export callbacks.
8. Оставить `HERMES_SAFE_MODE=true`.

После rollback старый Telegram-бот должен продолжать работать по текущей логике.

## Rollback по отдельным зонам

Если проблема только в assistant mode:

```text
HERMES_ASSISTANT_MODE_ENABLED=false
```

Если проблема только в engineer mode:

```text
HERMES_ENGINEER_MODE_ENABLED=false
```

Если проблема только в export callbacks:

```text
HERMES_EXPORT_CALLBACKS_ENABLED=false
```

Если проблема в admin changes:

```text
HERMES_ADMIN_CHANGES_ENABLED=false
```

Если проблема непонятна:

```text
HERMES_ADAPTER_ENABLED=false
HERMES_SAFE_MODE=true
```

## Failure modes

### Adapter упал

Действие:

* включить fallback;
* не падать в live polling;
* вернуть текущий ответ старого бота;
* diagnostics показать `adapter_status=error`;
* не отправлять stack trace пользователю.

### Adapter вернул небезопасное действие

Действие:

* заблокировать action;
* включить fallback;
* diagnostics показать `unsafe_action_blocked=true`;
* не менять файлы;
* не запускать export;
* не менять базу.

### Assistant mode не отвечает

Действие:

* вернуть fallback-ответ;
* оставить `/чат` в старой логике;
* не пытаться парсить заказ случайно;
* diagnostics показать assistant timeout/error без личных данных.

### Engineer mode ошибся

Действие:

* не выполнять изменения;
* оставить только draft;
* требовать owner confirmation;
* при сомнении включить fallback;
* `HERMES_ENGINEER_MODE_ENABLED=false`, если ошибка повторяется.

### Export callbacks дают ошибку

Действие:

* не отправлять файл;
* не создавать новый live export без подтверждения;
* включить fallback старого export flow, если он безопасен;
* иначе показать безопасную блокировку;
* `HERMES_EXPORT_CALLBACKS_ENABLED=false` до анализа.

### Diagnostics не проходят

Действие:

* не включать adapter;
* оставить `HERMES_ADAPTER_ENABLED=false`;
* оставить `HERMES_SAFE_MODE=true`;
* не переходить к dry-run;
* сначала исправить diagnostics plan.

## Правило fallback

Обязательное правило:

```text
если Hermes adapter недоступен или небезопасен, бот обязан продолжить старый безопасный путь
```

Fallback не должен:

* запускать Telegram заново;
* перезапускать polling;
* читать token;
* читать `.env`;
* менять файлы;
* создавать export;
* менять базу;
* скрыто менять цены, материалы или правила.

## Что нельзя включать первым этапом

Первым этапом нельзя включать:

* admin changes;
* изменение цен;
* изменение правил;
* изменение базы;
* Vision/API;
* live-деплой;
* автоперезапуск polling;
* отправку файлов через новый adapter;
* запись в production-хранилище;
* изменение owner/access checks.

Эти зоны допускаются только после отдельных планов, diagnostics, dry-run, подтверждения владельца и rollback.

## Первый безопасный порядок внедрения позже

Рекомендуемый порядок будущего внедрения:

1. Diagnostics only.
2. Adapter off.
3. Adapter dry-run.
4. Assistant mode dry-run.
5. Engineer mode dry-run.
6. Export callbacks отдельно.
7. Admin changes только последним этапом.

Каждый этап должен иметь:

* отдельный план;
* отдельное разрешение пользователя;
* проверку fallback;
* проверку diagnostics;
* отчёт;
* решение: принять или откатить.

## Минимальные критерии готовности перед live

Перед любым live-включением должны быть готовы:

* dry-run contract;
* diagnostics report;
* fallback tests;
* rollback checklist;
* owner/access safety check;
* запрет на вывод token;
* запрет на чтение `.env` без отдельного разрешения;
* понятная инструкция отключения adapter.

## Что сейчас не разрешается

Этот план не разрешает:

* подключаться к серверу;
* читать серверные файлы;
* читать token;
* читать `.env`;
* читать `config.py`;
* читать переменные окружения;
* запускать Telegram;
* запускать polling;
* менять код бота;
* трогать Vision/API;
* менять базу;
* менять реальные заказы;
* делать deploy.

## Следующий безопасный шаг

После этого плана безопасный следующий шаг:

```text
Серия 175-178 — План dry-run contract для Hermes adapter
```

Техническое имя:

```text
BATCH_SERIES_175_178_HERMES_ADAPTER_DRY_RUN_CONTRACT_PLAN
```

Цель следующего шага: описать контракт dry-run режима Hermes adapter без изменения live-бота.
