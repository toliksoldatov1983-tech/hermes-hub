# LEGACY PURGE MANIFEST

Дата: 2026-07-04

---

## ACTIVE_KEEP (не трогать)

- `C:\Users\user\.ssh\` — все ключи и config
- `C:\Users\user\Desktop\Hermes-Clean\` — весь проект
- `C:\Users\user\AppData\Local\hermes\` — активный Hermes
- `E:\РАБОТА\` — реальные заказы
- `C:\Users\user\AppData\Local\hermes\plugins\hermes_clean_gateway_plugin.py`

## PROTECTED_KEEP (не трогать никогда)

- `.env`, токены, ключи, пароли
- Базы данных
- Реальные заказы
- final backup перед purge
- private keys

## LEGACY_DELETE — СЕРВЕР

| Объект | Причина |
|--------|---------|
| `/opt/malyarka-telegram-bot/` | Старый проект бота, остановлен, disabled |
| `/etc/systemd/system/malyarka-telegram-bot.service` | Старый systemd unit, disabled |
| `cron: 0 21 * * * /opt/malyarka-telegram-bot/...` | Старый daily summary |

## LEGACY_DELETE — ЛОКАЛЬНО

| Объект | Причина |
|--------|---------|
| `02_PROJECTS/malyarka/telegram_bot.md` | Старый doc telegram бота |

## UNCERTAIN_KEEP (не удалять)

- Нет неопределённых объектов
