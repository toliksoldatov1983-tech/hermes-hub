# Server Bot Whitelist Copy Instructions

Дата: 2026-06-15

Серия:

```text
Серия 139-142 - Инструкция безопасного копирования whitelist-файлов в read-only staging
```

## Цель

Безопасно получить локальную read-only копию только разрешённых файлов существующего серверного Telegram-бота.

Это подготовительная инструкция. Она не разрешает подключение к серверу, копирование файлов, запуск collector, чтение token или чтение `.env`.

## Источник

```text
Сервер: hermes
Путь на сервере: /opt/malyarka-telegram-bot
```

## Локальная staging-папка

```text
E:\Hermes-Hub\inputs\server_bot_read_only_copy
```

В эту папку позже можно положить только whitelist-файлы и только после отдельного разрешения пользователя.

## Whitelist файлов

Копировать позже можно только эти файлы:

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

Нельзя копировать папки целиком. Каждый файл должен попадать в staging только по этому списку.

## Что запрещено копировать

```text
.env
token
secret files
environment dumps
orders.db
database files
logs
.git
JSON с секретами
приватные ключи
реальные заказы
реальные .cdr файлы
реальные .art файлы
реальные .xlsx файлы
любые папки целиком без фильтра
```

Если есть сомнение, файл не копировать.

## Проверочный список после будущего копирования

Перед запуском collector нужно проверить:

- в staging есть только whitelist-файлы;
- в staging нет `.env`;
- в staging нет token/secret/db/log/.git;
- в staging нет JSON с секретами;
- в staging нет приватных ключей;
- в staging нет реальных заказов;
- в staging нет реальных `.cdr`, `.art`, `.xlsx`;
- структура staging соответствует whitelist;
- `MANIFEST.md` обновлён после копирования;
- collector ещё не запускался до проверки списка.

## Следующий шаг после будущего копирования

После отдельного разрешения пользователя, ручного копирования только whitelist-файлов и проверки staging можно запускать collector локально:

```powershell
python E:\Hermes-Hub\tools\server_bot\collect_server_bot_read_only.py --source E:\Hermes-Hub\inputs\server_bot_read_only_copy --output E:\Hermes-Hub\inputs\server_bot_read_only_copy\SERVER_BOT_READ_ONLY_REPORT.md
```

Ожидаемый результат:

```text
E:\Hermes-Hub\inputs\server_bot_read_only_copy\SERVER_BOT_READ_ONLY_REPORT.md
```

После отчёта нужен отдельный анализ архитектуры серверного Telegram-бота.

## Что эта инструкция НЕ разрешает

- подключаться к серверу сейчас;
- копировать серверные файлы сейчас;
- запускать collector сейчас;
- запускать collector на сервере;
- читать token;
- читать `.env`;
- читать переменные окружения;
- менять код существующего бота;
- останавливать или перезапускать polling;
- трогать live-бот;
- трогать базы, логи, реальные заказы, Corel, ArtCAM, CNC.
