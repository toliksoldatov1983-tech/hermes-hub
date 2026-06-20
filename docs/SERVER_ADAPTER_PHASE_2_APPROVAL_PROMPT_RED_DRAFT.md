# Phase 2 — RED Approval Prompt Draft

Date: 2026-06-18 | DO NOT execute

```text
RED GATE APPROVAL:

Разрешаю SERVER_ADAPTER_PHASE_2_CONTROLLED_ENABLE.

ПРЕДУПРЕЖДЕНИЕ:
Потребуется server access. Feature flag будет временно ON.
Бот будет restarted controlled.

РАЗРЕШЕНО:
- Reconnect via Rescue (hetzner-hermes)
- Создать backup
- Установить _HERMES_ADAPTER_ENABLED = True
- Controlled restart bot
- Тестовые сообщения 2-4 часа
- Вернуть flag OFF
- Restart bot
- Удалить temp key

ЗАПРЕЩЕНО:
- .env/token/config.py
- DB/log/orders
- Production enable
- Оставить flag ON после теста

ОЖИДАНИЕ:
После теста flag OFF, бот работает, temp key удалён.
```
