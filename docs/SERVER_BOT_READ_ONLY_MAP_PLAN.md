# Server Bot Read-Only Map Plan

Дата: 2026-06-15

Серия:

```text
Серия 125–128 — План read-only карты серверного Telegram-бота
BATCH_SERIES_125_128_SERVER_BOT_READ_ONLY_MAP_PLAN
```

## Назначение

Этот документ описывает безопасный план будущего read-only изучения существующего серверного Telegram-бота.

Цель будущей карты:

- безопасно изучить существующего серверного Telegram-бота;
- составить карту запуска, команд и обработчиков;
- понять, куда можно подключить Hermes Hub / Malyarka Clean adapter;
- не останавливать и не ломать работающий polling-бот.

Это только документация.

Codex к серверу не подключался, серверные файлы не читал, token и `.env` не читал.

## Файлы, которые можно будет читать позже

Только после отдельного прямого разрешения пользователя можно будет читать:

```text
/opt/malyarka-telegram-bot/malyarka_telegram/app.py
/opt/malyarka-telegram-bot/malyarka_telegram/config.py
/opt/malyarka-telegram-bot/malyarka_telegram/handlers.py
/opt/malyarka-telegram-bot/malyarka_telegram/router.py
/opt/malyarka-telegram-bot/malyarka_telegram/keyboards.py
/opt/malyarka-telegram-bot/malyarka_telegram/messages.py
/opt/malyarka-telegram-bot/malyarka_telegram/models.py
/opt/malyarka-telegram-bot/malyarka_core/parsing.py
/opt/malyarka-telegram-bot/malyarka_core/validation.py
/opt/malyarka-telegram-bot/malyarka_core/calculations.py
/opt/malyarka-telegram-bot/malyarka_core/services/orders.py
/opt/malyarka-telegram-bot/malyarka_core/services/archive.py
/opt/malyarka-telegram-bot/requirements.txt
/opt/malyarka-telegram-bot/MALYARKA_CURRENT_STATE.md
```

Эти файлы можно читать только в режиме просмотра. Изменения, запуск, копирование секретов и вывод секретов запрещены.

## Зоны, которые нельзя читать без отдельного специального разрешения

Нельзя читать без отдельного специального разрешения:

```text
.env
любые файлы с token
любые файлы секретов
переменные окружения
старые JSON с токенами
базы данных
приватные ключи
логи, если в них могут быть token или личные данные
```

Если во время будущей read-only проверки появится риск увидеть секрет, проверку нужно остановить и запросить отдельное решение пользователя.

## Будущий порядок read-only карты

1. Сначала прочитать только список файлов.
2. Потом прочитать `app.py`, чтобы понять точку входа.
3. Потом прочитать `config.py`, но без вывода token и без чтения `.env`.
4. Потом прочитать `handlers.py` и `router.py`, чтобы понять команды и сообщения.
5. Потом прочитать `keyboards.py` и `messages.py`, чтобы понять UX.
6. Потом прочитать core-файлы `parsing.py`, `validation.py`, `services/orders.py`, чтобы понять связь с заказами.
7. Потом выяснить автозапуск только read-only:
   - systemd service search;
   - process command;
   - возможный shell history не читать без отдельного разрешения;
   - не останавливать процесс.
8. После этого составить карту:
   - как бот запускается;
   - какие команды принимает;
   - где обработчики;
   - где можно подключить Hermes adapter;
   - какие зоны риска.

## Запреты будущей инвентаризации

Во время будущей инвентаризации нельзя:

- запускать новую копию бота;
- останавливать текущий процесс;
- перезапускать polling;
- читать token;
- читать `.env`;
- выводить секреты;
- менять файлы;
- ставить зависимости;
- делать `git pull`;
- делать `git commit` или `git push`;
- менять права файлов;
- создавать сервисы;
- менять systemd;
- менять cron;
- трогать базы;
- трогать реальные заказы.

## Что этот документ НЕ разрешает

Этот документ не разрешает:

- подключение к серверу;
- чтение серверных файлов;
- чтение `.env`;
- использование token;
- чтение переменных окружения с token;
- остановку бота;
- перезапуск бота;
- запуск Telegram;
- запуск polling;
- изменение кода существующего бота;
- импорт старого `bot.py`;
- отправку сообщений;
- создание Excel;
- подключение API;
- изменение парсера;
- изменение Excel/Corel export;
- любые действия с реальными заказами.

## Следующий безопасный шаг

Отдельным разрешением пользователя выполнить ручную read-only проверку содержимого:

```text
/opt/malyarka-telegram-bot/malyarka_telegram/app.py
/opt/malyarka-telegram-bot/malyarka_telegram/config.py
/opt/malyarka-telegram-bot/malyarka_telegram/handlers.py
/opt/malyarka-telegram-bot/malyarka_telegram/router.py
```

Условия будущей проверки:

```text
без token
без .env
без изменений
без остановки polling
без перезапуска Telegram-бота
```
