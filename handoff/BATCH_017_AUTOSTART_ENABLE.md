# BATCH_017 — Autostart Enable Plan

Дата: 2026-06-21
Статус: READY. Ждёт `APPROVE_ENABLE_AUTOSTART` + Codex.

---

## Цель

Включить автозапуск Telegram-бота: `systemctl enable malyarka-telegram-bot`.
После этого бот будет автоматически подниматься после перезагрузки сервера.

---

## Текущее состояние

| Параметр | Значение |
|----------|----------|
| Сервер | 178.104.95.187 |
| Сервис | malyarka-telegram-bot.service |
| Состояние | active/running |
| Autostart | **disabled** |

---

## Precheck (перед выполнением)

| # | Проверка | Команда | Ожидаемый результат |
|---|---------|---------|-------------------|
| 1 | SSH доступ | `ssh root@178.104.95.187` | Вход успешен |
| 2 | Сервис существует | `systemctl status malyarka-telegram-bot` | `Loaded: loaded` |
| 3 | Сервис работает | `systemctl is-active malyarka-telegram-bot` | `active` |
| 4 | Autostart выключен | `systemctl is-enabled malyarka-telegram-bot` | `disabled` |
| 5 | Feature flag OFF | `_HERMES_ADAPTER_ENABLED = False` | Подтверждено |
| 6 | Production OFF | Статус | OFF |

---

## Команда

```bash
systemctl enable malyarka-telegram-bot
```

**Одна команда.** Никаких restart, stop, или изменений кода.

---

## Postcheck

| # | Проверка | Ожидаемый результат |
|---|---------|-------------------|
| 1 | Autostart включён | `systemctl is-enabled malyarka-telegram-bot` → `enabled` |
| 2 | Сервис всё ещё работает | `systemctl is-active malyarka-telegram-bot` → `active` |
| 3 | Feature flag не изменился | OFF |

---

## Что разрешено

- `systemctl enable malyarka-telegram-bot`
- `systemctl status`, `is-enabled`, `is-active` (read-only)

## Что запрещено

- `systemctl restart` / `stop`
- Изменение feature flag
- Phase 2 / production
- Чтение .env, config.py, token, DB, logs, orders
- Git push

---

## Rollback

Если что-то пошло не так:
```bash
systemctl disable malyarka-telegram-bot
```

---

## Approval

**Точная фраза:** `APPROVE_ENABLE_AUTOSTART`

Только после этой фразы от пользователя — выполнение.

---

## Expected result

```
systemctl is-enabled malyarka-telegram-bot → enabled
systemctl is-active malyarka-telegram-bot  → active
```

Бот будет автоматически запускаться после перезагрузки сервера.
