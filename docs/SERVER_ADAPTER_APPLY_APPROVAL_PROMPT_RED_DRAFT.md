# Server Adapter Apply Approval Prompt — RED Draft

Date: 2026-06-17 | DO NOT execute

```text
RED GATE APPROVAL:

Разрешаю SERVER_ADAPTER_GATE_6_BACKUP_AND_STAGING_APPLY.

ПРЕДУПРЕЖДЕНИЕ:
Будут server writes. Будут созданы backup-файлы.

РАЗРЕШЕНО:
- Создать backup adapters/telegram.py
- Создать новый файл adapters/hermes_adapter.py
- Добавить hook в adapters/telegram.py
- Флаг _HERMES_ADAPTER_ENABLED = False (off by default)

НЕЛЬЗЯ:
- Restart live bot
- Запускать systemctl
- Трогать token/.env/config.py
- Трогать handlers.py / router.py / orders.py
- Запускать polling/webhook
- Делать git/patch
- Включать feature flag в True

ОЖИДАНИЕ:
Файлы загружены на сервер, флаг off.
Ничего не изменилось в поведении бота.
```
