# Server Read-Only Gate 1 Retry Prompt

Date: 2026-06-17 | After SSH access restored

```text
RED GATE APPROVAL (retry):

SSH доступ восстановлен.
Разрешаю SERVER_READ_ONLY_GATE_1_VERIFY_ARCHITECTURE_ONLY (повторно).

Цель: read-only проверка архитектуры /opt/malyarka-telegram-bot.
Без изменений. Без patch. Без записи. Без чтения secrets.

Allowed: pwd, ls, find, tree, head (whitelist only).
Forbidden: token, .env, config.py, DB, logs, orders, systemctl, git, patch.
```
