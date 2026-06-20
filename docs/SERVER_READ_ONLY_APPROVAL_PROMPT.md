# Server Read-Only Approval Prompt

Date: 2026-06-17 | Gate: RED

## RED APPROVAL PROMPT

```text
RED GATE APPROVAL:

Разрешаю SERVER_READ_ONLY_GATE_1_VERIFY_ARCHITECTURE_ONLY.

Цель:
Только read-only verification архитектуры сервера.
Без изменений. Без patch. Без записи.

РАЗРЕШЕНО:
- pwd, ls -la, find (maxdepth 2), tree -L 2
- head -5 для whitelist файлов
- Проверить наличие: handlers.py, router.py, app.py

НЕЛЬЗЯ:
- Читать token/.env/config.py contents
- Читать os.environ
- Читать database/log/order contents
- Запускать polling/webhook
- Делать git add/commit/push
- Применять patch
- Менять любые файлы
- Запускать systemctl

ОСТАНОВИТЬСЯ ЕСЛИ:
- Встречен config.py → STOP
- Нужен SSH без approval → STOP
- Сомнение в безопасности файла → STOP

ОЖИДАЕМЫЙ РЕЗУЛЬТАТ:
Read-only report с подтверждённой структурой сервера.
```

## Status

This prompt is READY but NOT submitted. Requires explicit user RED approval.
