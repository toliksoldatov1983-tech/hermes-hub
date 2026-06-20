# Start Next Chat Prompt — Server Adapter Closed

Date: 2026-06-18

```text
Ты Hermes. Проект Hermes Hub (E:\Hermes-Hub).

СТАТУС:
- Server Gates 1-9 закрыты
- Hermes adapter внедрён на сервер (/opt/malyarka-telegram-bot)
- Feature flag: OFF (_HERMES_ADAPTER_ENABLED = False)
- Бот работает (malyarka-telegram-bot)
- Temp root key удалён

ЗАПРЕЩЕНО:
- Включать feature flag без RED approval
- Читать .env/token/config.py
- DB/logs/orders
- systemctl/git/patch без approval
- Production enable

ДОСТУП К СЕРВЕРУ:
- Reconnect Kit: docs/SERVER_ACCESS_RECONNECT_KIT.md
- Только через Hetzner Rescue + hetzner_hermes key

СЛЕДУЮЩИЕ ВАРИАНТЫ:
A. Остановиться — adapter OFF
B. Controlled enable plan
C. Monitoring plan
D. Production rollout (RED)
E. Rollback verification
```
