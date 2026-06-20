# Server Bot Manual Whitelist Copy Package

Дата: 2026-06-15

Серия:

```text
Серия 143-146 - Ручной пакет копирования whitelist-файлов серверного бота
```

## Цель

Дать пользователю простой ручной порядок, как позже безопасно скопировать только whitelist-файлы существующего серверного Telegram-бота в локальный staging.

Сейчас этот документ не разрешает подключаться к серверу, копировать файлы, запускать collector, читать token или `.env`.

## Источник

```text
Сервер: hermes
Путь на сервере: /opt/malyarka-telegram-bot
```

## Куда копировать локально

Локальный staging:

```text
E:\Hermes-Hub\inputs\server_bot_read_only_copy
```

## Какую структуру папок создать

Внутри staging должна получиться только такая структура:

```text
E:\Hermes-Hub\inputs\server_bot_read_only_copy
├─ malyarka_telegram
│  ├─ app.py
│  ├─ router.py
│  ├─ handlers.py
│  ├─ keyboards.py
│  ├─ messages.py
│  ├─ access.py
│  ├─ modes.py
│  ├─ session.py
│  ├─ intent.py
│  └─ models.py
├─ malyarka_core
│  ├─ services
│  │  ├─ orders.py
│  │  └─ archive.py
│  ├─ parsing.py
│  ├─ validation.py
│  └─ calculations.py
├─ requirements.txt
├─ MALYARKA_CURRENT_STATE.md
├─ README.md
└─ MANIFEST.md
```

`README.md` и `MANIFEST.md` - локальные файлы Hermes Hub. Их не нужно брать с сервера.

## Какие файлы скопировать с сервера

Копировать только эти файлы:

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

Нельзя копировать папки целиком. Нужно выбирать только конкретные файлы из whitelist.

## Что запрещено копировать

```text
.env
token
secret files
env dumps
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
папки целиком без фильтра
```

Если файл не входит в whitelist, его не копировать.

## Пошаговый ручной порядок

1. Получить отдельное разрешение пользователя на ручное копирование whitelist-файлов.
2. Открыть локальную папку:

```text
E:\Hermes-Hub\inputs\server_bot_read_only_copy
```

3. Вручную создать в ней подпапки:

```text
malyarka_telegram
malyarka_core
malyarka_core\services
```

4. С сервера `hermes` из `/opt/malyarka-telegram-bot` скопировать только файлы из whitelist.
5. Не копировать `.env`, token, secrets, db, logs, `.git`, JSON с секретами, реальные заказы, реальные `.cdr/.art/.xlsx`.
6. После копирования открыть checklist:

```text
E:\Hermes-Hub\docs\SERVER_BOT_STAGING_CHECKLIST.md
```

7. Проверить staging по checklist.
8. Обновить `MANIFEST.md`, если копирование реально выполнялось.
9. Только после успешной проверки запускать collector локально.

## Как проверить, что лишнее не попало

После будущего копирования нужно убедиться:

- в staging есть только whitelist-файлы;
- нет `.env`;
- нет token или secret files;
- нет env dumps;
- нет `orders.db` и database files;
- нет logs;
- нет `.git`;
- нет JSON с секретами;
- нет приватных ключей;
- нет реальных заказов;
- нет реальных `.cdr`, `.art`, `.xlsx`;
- нет папок, скопированных целиком без фильтра.

## Что делать после копирования

После отдельного разрешения пользователя, ручного копирования whitelist и проверки checklist можно запускать collector только локально:

```powershell
python E:\Hermes-Hub\tools\server_bot\collect_server_bot_read_only.py --source E:\Hermes-Hub\inputs\server_bot_read_only_copy --output E:\Hermes-Hub\inputs\server_bot_read_only_copy\SERVER_BOT_READ_ONLY_REPORT.md
```

Ожидаемый результат:

```text
E:\Hermes-Hub\inputs\server_bot_read_only_copy\SERVER_BOT_READ_ONLY_REPORT.md
```

После этого нужен отдельный анализ архитектуры отчёта.

## Что этот пакет НЕ разрешает

- подключаться к серверу сейчас;
- копировать серверные файлы сейчас;
- запускать collector сейчас;
- читать token;
- читать `.env`;
- читать переменные окружения;
- менять код существующего бота;
- останавливать или перезапускать polling;
- трогать live-бот;
- трогать базы, логи, реальные заказы, Corel, ArtCAM, CNC.
