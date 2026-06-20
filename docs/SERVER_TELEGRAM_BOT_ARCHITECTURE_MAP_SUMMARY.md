# Краткое резюме architecture map серверного Telegram-бота

Дата: 2026-06-15

Источник:

`E:\Hermes-Hub\inputs\server_bot_read_only_copy\SERVER_BOT_READ_ONLY_REPORT.md`

## Что уже понятно

Существующий серверный Telegram-бот устроен как цепочка:

```text
Telegram
-> malyarka_telegram/app.py
-> aiogram Dispatcher
-> router.py
-> handlers.py
-> malyarka_core/services/orders.py
-> parsing / validation / calculations
-> exports / files
```

Точка входа — `malyarka_telegram/app.py`.

Режим запуска — polling через `--run-polling`.

В боте есть режимы order, chat, engineer, ideas, admin, summary, rules и neutral. Текст пользователя сначала маршрутизируется по режиму, затем заказная ветка уходит в core-слой.

Есть callback flows для:

* Excel/Corel;
* файла малярки;
* инженерных task-card actions;
* уточнения намерения пользователя.

Access checks завязаны на owner-механику и owner-only modes. Значения owner/token не раскрывались.

## Куда потенциально подключать Hermes

Самые безопасные точки будущего подключения:

* adapter layer между `router.py` / `handlers.py` и core-сервисами;
* обвязка вокруг `build_order_preview_from_text`;
* read-only diagnostics рядом с `services/orders.py`;
* feature flags перед export callbacks;
* отдельный Hermes adapter без прямой правки live `app.py`.

## Что нельзя менять напрямую

Нельзя напрямую менять:

* live `app.py`;
* polling-запуск;
* token / `.env` / `config.py`;
* owner/access checks;
* callback-отправку файлов;
* Excel/Corel export server flow;
* Malyarka file export;
* archive/storage/db-зону;
* Vision/API;
* любые live-действия на сервере.

## Особые отметки

* `malyarka_telegram/models.py` отсутствует в staging и отмечен как missing.
* Redaction сработал 22 раза.
* Obsidian hints есть только на уровне прежней инвентаризации: `obsidian_inbox.py` не входил в whitelist и не анализировался.
* Сервер, live-бот, token, `.env`, `config.py`, Vision и API не трогались.

## Следующий безопасный шаг

Серия 167-170 — План Hermes adapter layer для серверного Telegram-бота

Техническое имя:

`BATCH_SERIES_167_170_HERMES_ADAPTER_LAYER_PLAN`
