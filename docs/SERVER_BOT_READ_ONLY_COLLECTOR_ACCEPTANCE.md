# Server Bot Read-Only Collector Acceptance

Дата: 2026-06-15

Серия:

```text
Серия 131–134 — Safe read-only collector серверного Telegram-бота
```

## Принято

Создан локальный безопасный collector:

```text
E:\Hermes-Hub\tools\server_bot\collect_server_bot_read_only.py
```

Созданы focused tests:

```text
E:\Hermes-Hub\tests\test_server_bot_read_only_collector.py
```

Создана документация:

```text
E:\Hermes-Hub\docs\SERVER_BOT_READ_ONLY_COLLECTOR.md
E:\Hermes-Hub\docs\SERVER_BOT_READ_ONLY_COLLECTOR_ACCEPTANCE.md
```

## Проверки

Focused tests:

```text
python -m pytest E:\Hermes-Hub\tests\test_server_bot_read_only_collector.py -q
5 passed
```

Локальный dry-run на временной тестовой папке:

```text
SERVER_BOT_READ_ONLY_REPORT.md created
read_only: true
redaction applied
```

## Подтверждённые границы

- сервер не трогался;
- live-бот не трогался;
- polling не останавливался и не перезапускался;
- webhook не трогался;
- token не читался;
- `.env` не читался;
- переменные окружения не читались collector-ом;
- серверные файлы не читались;
- код существующего бота не менялся.

## Следующий безопасный шаг

Отдельно спланировать безопасный запуск collector на read-only копии или получить отдельное разрешение пользователя на будущий read-only сбор карты серверного бота.
