# Malyarka Runtime Clean

Создано: 2026-06-23

Это clean-кандидат для будущего runtime-кода Telegram-бота Malyarka.

## Источники

База:

```text
C:\Users\user\Desktop\malyarka_codex_work
```

Точечно перенесено с серверного снимка `/opt/malyarka-telegram-bot`:

```text
malyarka_core/exports/malyarka_file.py
requirements.txt: openpyxl
```

## Что сознательно не перенесено

```text
.env
orders.db
.venv
.git
__pycache__
.pytest_cache
bot.py
bot_backup_before_vision.py
test.py
серверные backup-файлы
```

## Почему

Задача этой папки — стать чистой runtime-базой без секретов, базы, старых монолитов и случайных backup-файлов.

## Важно

Эта папка пока не деплоится на сервер. Сначала нужны тесты, ручное ревью отличий и исправление Telegram token/env на боевом сервере.
