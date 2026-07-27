# TELEGRAM EXISTING BOT REPROFILE PLAN

Дата: 2026-07-03 · Статус: **PLAN · НЕ ВЫПОЛНЯТЬ**

---

## 1. ЧТО НАЙДЕНО

### Старый бот (архив)

| Поле | Значение |
|------|----------|
| Путь | `C:\Users\user\Documents\Codex\Malyarka_Desktop_Archive_2026-05-29\python_test\bot.py` |
| Копия | `python_test_рабочая_копия\bot.py` |
| Размер | 1348 строк |
| Функций/handlers | ~47 |
| Библиотека | python-telegram-bot |
| Статус | Архивный, не запущен |

### Hermes-Clean Telegram (dry-run)

| Поле | Значение |
|------|----------|
| Путь | `src/hermes_clean/telegram_flow.py` |
| Размер | 521 строка |
| Статус | Dry-run only, live не запущен |

---

## 2. BACKUP ПЕРЕД ИЗМЕНЕНИЯМИ

```
1. Полный backup архива:
   C:\Users\user\Documents\Codex\Malyarka_Desktop_Archive_2026-05-29\

2. Backup Hermes-Clean telegram:
   C:\Users\user\Desktop\Hermes-Clean\src\hermes_clean\telegram_flow.py

3. Создать backup_telegram_before_reprofile_YYYYMMDD\
```

---

## 3. ПЛАН ПЕРЕВОДА

### Фаза 1 — Инвентаризация старого бота

| Что проверить | Статус |
|---------------|--------|
| ⬜ Путь проекта | Найден |
| ⬜ Как запускается | `python bot.py` / systemd / cron |
| ⬜ Polling или webhook | read from old code |
| ⬜ Handlers | ~47 шт |
| ⬜ Config | .env / config.yaml |
| ⬜ Whitelist | chat_id allowlist |
| ⬜ Logs | файл или stdout |
| ⬜ Business logic | Malyarka + Telegram |

### Фаза 2 — Архивация старой логики

| Действие | Как |
|----------|-----|
| Не удалять bot.py | Переименовать: `bot_archive_20260703.py` |
| Не удалять handlers | Закомментировать, оставить в коде |
| Не удалять config | Сохранить как `config_archive.yaml` |
| Старый whitelist | Сохранить, не применять |

### Фаза 3 — Новый Hermes-Clean режим

| Компонент | Реализация |
|-----------|------------|
| Polling | python-telegram-bot Application |
| Single-user | Whitelist: только chat_id владельца |
| Приём сообщений | Обычный текст, без slash-команд |
| Заказы | Intake → preview → correction |
| Цены | Draft → preview → confirm |
| ЛКМ | Draft first |
| Backup | По просьбе владельца |
| Статус | Read-only |
| Audit log | Каждое изменение |

### Фаза 4 — Запреты

| Действие | Статус |
|----------|--------|
| Чужой chat_id | 🚫 Блок |
| Удаление | 🚫 Никогда |
| Overwrite | 🚫 Только _vN |
| Vision API | 🚫 Отдельный план |
| Google Drive | 🚫 HOLD |
| Git push | 🚫 Без approval |
| CorelDRAW, ArtCAM, CNC | 🚫 Никогда |

---

## 4. ROLLBACK

| Действие | Как |
|----------|-----|
| Остановить Hermes mode | Закрыть Application |
| Вернуть старую логику | Переименовать `bot_archive` → `bot.py` |
| Вернуть config | `config_archive` → `config.yaml` |
| Вернуть whitelist | Старый whitelist |
| Полный откат | `backup_telegram_before_reprofile` → восстановить |

---

## 5. НЕОБХОДИМО ДЛЯ ЗАПУСКА

- [ ] Telegram bot token (есть в старом .env)
- [ ] Подтверждён chat_id владельца
- [ ] Approval фраза: «ОДОБРЯЮ TELEGRAM EXISTING BOT REPROFILE»
- [ ] Dry-run всех 10 сценариев PASS
- [ ] Rollback протестирован

---

## 6. СТАТУС

**EXISTING_TELEGRAM_BOT_REPROFILE_PLAN_READY**

План готов. Бот не тронут. Live не запущен.
Жду «ОДОБРЯЮ TELEGRAM EXISTING BOT REPROFILE».
