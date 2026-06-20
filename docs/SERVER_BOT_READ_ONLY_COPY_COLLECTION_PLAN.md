# Server Bot Read-Only Copy Collection Plan

Дата: 2026-06-15

Серия:

```text
Серия 135–138 — План безопасного запуска collector на read-only копии
```

## Цель

Подготовить надёжный путь запуска server bot collector не на live-сервере, а на локальной read-only копии разрешённых файлов.

Collector не запускается на сервере.

Сначала должна быть создана копия только whitelist-файлов.

## Локальная зона копии

Подготовлена пустая локальная папка-заготовка:

```text
E:\Hermes-Hub\inputs\server_bot_read_only_copy
```

## Что можно копировать позже

Только после отдельного разрешения пользователя можно положить в локальную папку копии только whitelist-файлы:

```text
malyarka_telegram/app.py
malyarka_telegram/router.py
malyarka_telegram/handlers.py
malyarka_telegram/keyboards.py
malyarka_telegram/messages.py
malyarka_telegram/access.py
malyarka_telegram/modes.py
malyarka_telegram/session.py
malyarka_telegram/intent.py
malyarka_telegram/models.py
malyarka_core/services/orders.py
malyarka_core/services/archive.py
malyarka_core/parsing.py
malyarka_core/validation.py
malyarka_core/calculations.py
requirements.txt
MALYARKA_CURRENT_STATE.md
```

## Что запрещено копировать

Запрещено копировать:

```text
.env
token
secrets
db
logs
.git
реальные заказы
приватные ключи
переменные окружения
архивы с секретами
```

Если есть сомнение, файл не копировать.

## Как должен запускаться collector

Collector запускается только по локальной копии:

```powershell
python E:\Hermes-Hub\tools\server_bot\collect_server_bot_read_only.py --source E:\Hermes-Hub\inputs\server_bot_read_only_copy --output E:\Hermes-Hub\inputs\server_bot_read_only_copy\SERVER_BOT_READ_ONLY_REPORT.md
```

Результат:

```text
E:\Hermes-Hub\inputs\server_bot_read_only_copy\SERVER_BOT_READ_ONLY_REPORT.md
```

## Что будет после отчёта

После создания `SERVER_BOT_READ_ONLY_REPORT.md` нужен отдельный анализ архитектуры:

- entrypoints;
- modes;
- handlers;
- callbacks;
- keyboards;
- Telegram → core;
- exports/files;
- owner/access checks;
- точки для будущего Hermes adapter layer.

## Что этот план НЕ разрешает

Этот план не разрешает:

- подключаться к серверу;
- копировать серверные файлы сейчас;
- запускать collector на сервере;
- читать token;
- читать `.env`;
- читать переменные окружения;
- менять код существующего бота;
- останавливать или перезапускать polling;
- трогать live-бот;
- трогать реальные заказы.

## Следующий безопасный шаг

Отдельно получить разрешение пользователя на создание read-only копии whitelist-файлов в:

```text
E:\Hermes-Hub\inputs\server_bot_read_only_copy
```

После этого запустить collector только локально по этой копии.
