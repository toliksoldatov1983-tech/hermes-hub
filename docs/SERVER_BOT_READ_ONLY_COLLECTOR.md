# Server Bot Read-Only Collector

Дата: 2026-06-15

Серия:

```text
Серия 131–134 — Safe read-only collector серверного Telegram-бота
```

## Назначение

Локальный collector создан для будущего безопасного read-only сбора карты существующего серверного Telegram-бота.

Файл collector:

```text
E:\Hermes-Hub\tools\server_bot\collect_server_bot_read_only.py
```

Collector готовит отчёт:

```text
SERVER_BOT_READ_ONLY_REPORT.md
```

## Что делает collector

- читает только whitelist файлов;
- работает только как read-only;
- не импортирует `malyarka_telegram`;
- не импортирует `malyarka_core`;
- не импортирует `aiogram`;
- не выполняет код бота;
- не запускает процессы;
- не читает переменные окружения;
- не читает `.env`, token, secrets, db, logs;
- не меняет файлы бота;
- маскирует подозрительные строки;
- строит карту entrypoints, modes, handlers, callbacks, keyboards, Telegram → core, exports, owner/access checks.

## Whitelist

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

## Redaction

Collector маскирует строки, где встречаются:

```text
TOKEN
SECRET
API_KEY
PASSWORD
PRIVATE_KEY
bot_token
.env
```

Маска:

```text
[REDACTED: suspicious secret-like line]
```

## Как запускать позже

Только после отдельного разрешения пользователя и только на подготовленной read-only копии или безопасно примонтированной папке:

```powershell
python E:\Hermes-Hub\tools\server_bot\collect_server_bot_read_only.py --source <BOT_ROOT> --output SERVER_BOT_READ_ONLY_REPORT.md
```

## Что этот collector НЕ разрешает

- подключаться к серверу без отдельного разрешения;
- запускать collector на сервере без отдельного разрешения;
- читать `.env`;
- читать token;
- читать переменные окружения;
- останавливать или перезапускать Telegram-бота;
- менять код существующего бота;
- делать live-внедрение.
