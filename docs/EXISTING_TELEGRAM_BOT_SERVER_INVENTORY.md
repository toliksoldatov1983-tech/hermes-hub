# Existing Telegram Bot Server Inventory

Дата: 2026-06-15

Серия:

```text
Серия 121–124 — Документирование серверной инвентаризации существующего Telegram-бота
BATCH_SERIES_121_124_EXISTING_TELEGRAM_BOT_SERVER_INVENTORY
```

## Назначение

Этот документ фиксирует результаты ручной read-only инвентаризации существующего Telegram-бота на сервере `hermes`.

Это только документация.

Codex к серверу не подключался, серверные файлы не читал и серверный код не менял.

## Сервер

```text
Сервер: hermes
IP: 178.104.95.187
Рабочая папка бота: /opt/malyarka-telegram-bot
```

Вывод:

```text
Существующий серверный Telegram-бот найден.
Новый бот с нуля сейчас не создаётся.
```

## Найденная структура проекта

Корень:

```text
malyarka_ai
malyarka_core
malyarka_telegram
malyarka_vision
.venv
MALYARKA_CURRENT_STATE.md
requirements.txt
```

Telegram-слой:

```text
/opt/malyarka-telegram-bot/malyarka_telegram

access.py
app.py
config.py
engineer_tasks.py
handlers.py
intent.py
keyboards.py
messages.py
models.py
obsidian_inbox.py
router.py
session.py
voice.py
```

Core-слой:

```text
/opt/malyarka-telegram-bot/malyarka_core

adapters
calculations.py
exports
models.py
parsing.py
security
services
storage
validation.py
```

Services:

```text
/opt/malyarka-telegram-bot/malyarka_core/services

archive.py
orders.py
```

## Найденный запуск

Работающий процесс:

```text
/opt/malyarka-telegram-bot/.venv/bin/python -m malyarka_telegram.app --run-polling
```

Зафиксировано:

- бот сейчас запущен;
- режим работы: polling;
- Python-окружение: `.venv`;
- запуск идёт через python module;
- команда запуска найдена;
- явный systemd service для `malyarka` / `telegram` / `bot` / `hermes` не найден;
- multi-user автозапуск с явным `malyarka` / `telegram` / `bot` / `hermes` не найден;
- `screen`: активных сессий нет;
- `tmux`: активной сессии нет;
- `cron root`: no crontab for root;
- способ автозапуска пока не определён;
- способ автозапуска требует отдельной будущей read-only проверки.

## Границы безопасности

Не делалось:

- сервер не изменялся;
- бот не останавливался;
- бот не перезапускался;
- Telegram live не трогался;
- polling не перезапускался;
- token не читался;
- `.env` не читался;
- переменные окружения с token не читались;
- старые JSON не использовались;
- код не менялся.

Важно:

- этот документ не разрешает подключение token или `.env`;
- этот документ не разрешает перезапуск Telegram;
- этот документ не разрешает изменение серверного кода;
- этот документ только фиксирует результаты ручной инвентаризации пользователя.

## Следующий безопасный шаг

Отдельно спланировать read-only карту серверного бота:

- какие файлы можно читать;
- какие файлы нельзя читать;
- как посмотреть `app.py`, `config.py`, `handlers.py` без token;
- как понять способ запуска без остановки бота;
- как позже связать серверный бот с Hermes Hub / Malyarka Clean adapter.
