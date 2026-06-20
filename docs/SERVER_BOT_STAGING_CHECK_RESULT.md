# Server Bot Staging Check Result

Дата: 2026-06-15

Серия:

```text
Серия 155-158 - Проверка staging перед локальным запуском collector
```

## Проверенная папка

```text
E:\Hermes-Hub\inputs\server_bot_read_only_copy
```

## Итог проверки

```text
staging checked
only expected copied whitelist files and local Hermes files found
forbidden files not found
collector not run
server not touched
```

## Найденные whitelist-файлы

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

## Отсутствующие whitelist-файлы

```text
malyarka_telegram/models.py
```

Причина из предыдущего SFTP-копирования:

```text
файл не найден на сервере во время SFTP get
```

## Локальные служебные файлы

```text
README.md
MANIFEST.md
```

## Запрещённые файлы не найдены

Проверка локальной staging-папки не нашла:

```text
.env
token
secrets
password
private_key
api_key
config.py
orders.db
database files
logs
.git
JSON с секретами
реальные заказы
реальные .cdr файлы
реальные .art файлы
реальные .xlsx файлы
```

## Папки целиком

```text
Папки целиком без фильтра не копировались.
В staging есть только подготовленные папки malyarka_telegram, malyarka_core, malyarka_core/services и явные файлы whitelist.
```

## Что не делалось

- collector не запускался;
- сервер не трогался;
- live-бот не трогался;
- polling/webhook не трогались;
- token не читался;
- `.env` не читался;
- переменные окружения не читались;
- новые серверные файлы не копировались;
- код бота не менялся.

## Следующий безопасный шаг

Отдельно решить, запускать ли collector локально по проверенной staging-папке:

```text
E:\Hermes-Hub\inputs\server_bot_read_only_copy
```
