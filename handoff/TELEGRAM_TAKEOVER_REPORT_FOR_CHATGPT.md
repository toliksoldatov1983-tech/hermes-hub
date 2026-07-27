# TELEGRAM BOT TAKEOVER — ПОЛНЫЙ ОТЧЁТ ДЛЯ CHATGPT

Дата: 2026-07-04 · Итог: **TAKEOVER SUCCESS**

---

## ИСХОДНАЯ СИТУАЦИЯ

- Старый Telegram-бот работал на сервере 49.13.76.163 через systemd (`malyarka-telegram-bot.service`)
- Бот использовал polling на токене, который конфликтовал с локальным Hermes gateway
- SSH-доступа к серверу не было — все 5 локальных ключей выдавали `Permission denied (publickey)`

---

## ХРОНОЛОГИЯ

### 1. Поиск доступа к серверу
- Проверены все SSH-ключи в `~/.ssh/` (5 штук): `hermes_clean_full_access_ed25519`, `hermes_phase2_temp`, `hermes_temp_server_readonly`, `hetzner_hermes`
- 12 комбинаций (ubuntu/root × ключи) — все отказали
- hcloud CLI не установлен, парольный вход отключён
- Hetzner API токен создан через консоль (Read-only → потом Read-Write)

### 2. Rescue mode
- Включён rescue через Hetzner Console
- Получен временный rescue-пароль и IP 178.104.95.187
- Подключение через `ssh -i hetzner_hermes root@178.104.95.187` — СРАБОТАЛО (ключ hetzner_hermes уже был в проекте Hetzner)
- Основной диск смонтирован: `/dev/sda1 → /mnt/server`
- Публичный ключ Hermes (`hermes_clean_full_access_ed25519.pub`) добавлен в `/mnt/server/root/.ssh/authorized_keys`
- Синхронизация выполнена, диск отмонтирован

### 3. Выход из rescue
- Несколько попыток перезагрузки через разные способы
- Rescue отключён — сервер загрузился нормально
- IP сервера в обычном режиме: 178.104.95.187 (основной IP 49.13.76.163 не отвечает)
- SSH-доступ настроен: `hermes-server → root@178.104.95.187`

### 4. Остановка старого бота
- Найден процесс: `python -m malyarka_telegram.app --run-polling`
- Systemd сервис: `malyarka-telegram-bot.service` (active, enabled)
- Cron: ежедневный отчёт в 21:00
- Выполнено:
  - `systemctl stop malyarka-telegram-bot` → inactive
  - `systemctl disable malyarka-telegram-bot` → disabled
  - Крон-строка удалена из crontab

### 5. Gateway takeover
- Локальный Hermes gateway неоднократно перезапускался
- Telegram polling conflict разрешился после истечения старой сессии (~2 минуты)
- Gateway подключился к Telegram в режиме polling

### 6. Исправление контекста
- Проблема: gateway отвечал старым контекстом из E:\«Гермес Клин»
- `AGENTS.md` в E:\«Гермес Клин» обновлён — убраны conveyor/batch-правила
- `ACTIVE_BATCH.md` обновлён — убран статус «Bot: active/running»
- `CHATGPT_CONTEXT_BUNDLE.md` обновлён с актуальным статусом Hermes-Clean

### 7. Legacy purge
- Сервер: `/opt/malyarka-telegram-bot/` → архивирован в `/root/final_backup_before_legacy_purge/`
- Сервер: `/etc/systemd/system/malyarka-telegram-bot.service` → удалён
- Сервер: крон старого бота → удалён
- Локально: `02_PROJECTS/malyarka/telegram_bot.md` → удалён

### 8. Финальная проверка
- Telegram: «статус» → отвечает правильно:
  - Gateway работает ✅
  - Иван фасады v2 ✅
  - Старый бот удалён ✅

---

## ТЕКУЩЕЕ СОСТОЯНИЕ

| Параметр | Значение |
|----------|----------|
| Сервер | hermes / 178.104.95.187 |
| SSH | `hermes-server` → root (беспарольный) |
| Старый бот | Удалён полностью |
| Gateway | RUNNING, Telegram polling active |
| Telegram | Production single-user |
| Rollback | Backup в `/root/final_backup_before_legacy_purge_20260704/` |

---

## ROLLBACK (если нужно)

```bash
# Восстановить старый бот
ssh hermes-server
cp -r /root/final_backup_before_legacy_purge_20260704/malyarka-telegram-bot /opt/
cp /root/final_backup_before_legacy_purge_20260704/malyarka-telegram-bot.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now malyarka-telegram-bot
```
