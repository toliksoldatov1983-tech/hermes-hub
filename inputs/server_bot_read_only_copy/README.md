# Server Bot Read-Only Copy

Эта папка предназначена для будущей локальной read-only копии разрешённых файлов существующего серверного Telegram-бота.

Collector НЕ должен запускаться на live-сервере.

Папка:

```text
E:\Hermes-Hub\inputs\server_bot_read_only_copy
```

## Что сюда можно будет положить позже

Только после отдельного разрешения пользователя:

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

## Что сюда нельзя класть

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
```

## Будущий запуск collector

```powershell
python E:\Hermes-Hub\tools\server_bot\collect_server_bot_read_only.py --source E:\Hermes-Hub\inputs\server_bot_read_only_copy --output E:\Hermes-Hub\inputs\server_bot_read_only_copy\SERVER_BOT_READ_ONLY_REPORT.md
```
