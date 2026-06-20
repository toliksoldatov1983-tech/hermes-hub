# Server Bot Read-Only Copy Manifest

Дата создания заготовки: 2026-06-15

Последнее обновление: 2026-06-15

Статус:

```text
whitelist files copied by SFTP
server files copied only from whitelist
collector run locally
```

## Назначение

Эта папка содержит локальную read-only staging-копию whitelist-файлов существующего серверного Telegram-бота.

Источник копии:

```text
Сервер: hermes
IP: 178.104.95.187
Путь на сервере: /opt/malyarka-telegram-bot
Способ копирования: SFTP
```

Локальная staging-папка:

```text
E:\Hermes-Hub\inputs\server_bot_read_only_copy
```

## Скопированные whitelist-файлы

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
malyarka_core/services/orders.py
malyarka_core/services/archive.py
malyarka_core/parsing.py
malyarka_core/validation.py
malyarka_core/calculations.py
requirements.txt
MALYARKA_CURRENT_STATE.md
```

## Пропущенные whitelist-файлы

```text
malyarka_telegram/models.py - не найден на сервере во время SFTP get
```

## Локальные служебные файлы Hermes Hub

```text
README.md
MANIFEST.md
```

## Что НЕ копировалось

```text
.env
token
secret files
environment dumps
config.py
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

## Проверка staging по именам

```text
Запрещённые имена/расширения в staging не найдены.
config.py не скопирован.
.env не скопирован.
db/logs/.git/JSON/cdr/art/xlsx не скопированы.
Проверка перед запуском collector зафиксирована в E:\Hermes-Hub\docs\SERVER_BOT_STAGING_CHECK_RESULT.md.
```

## Collector

```text
collector not run on server
collector run locally on staging copy
report created: E:\Hermes-Hub\inputs\server_bot_read_only_copy\SERVER_BOT_READ_ONLY_REPORT.md
read_only: true
whitelist_only: true
bot_code_executed: false
environment_read: false
token_read: false
redaction hits: 22
```

Collector был запущен только локально по staging-копии.

## История

```text
2026-06-15: создана пустая локальная папка-заготовка. Серверные файлы не копировались.
2026-06-15: добавлена инструкция безопасного будущего копирования whitelist-файлов. Серверные файлы не копировались, collector не запускался.
2026-06-15: создан ручной пакет копирования и checklist. Staging был пустой, серверные файлы не копировались, collector не запускался.
2026-06-15: созданы пустые staging-папки malyarka_telegram, malyarka_core, malyarka_core/services. Серверные файлы не копировались, collector не запускался.
2026-06-15: выполнено SFTP-копирование whitelist-файлов с сервера hermes. Скопированы только whitelist-файлы. models.py не найден на сервере. Collector не запускался.
2026-06-15: выполнена локальная проверка staging перед collector. Запрещённые файлы не найдены, models.py отсутствует, collector не запускался.
2026-06-15: collector запущен локально по staging-копии. Создан SERVER_BOT_READ_ONLY_REPORT.md. Сервер не трогался, token/.env/config.py не читались, live-бот/polling не трогались.
2026-06-15: повторно подтверждён локальный запуск collector по staging-копии. SERVER_BOT_READ_ONLY_REPORT.md обновлён. Safety status остался read_only/whitelist_only, models.py missing, redaction hits: 22.
```
