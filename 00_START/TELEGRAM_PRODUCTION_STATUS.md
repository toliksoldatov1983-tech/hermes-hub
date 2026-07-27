# TELEGRAM PRODUCTION SINGLE-USER — STATUS

Дата: 2026-07-03 · Статус: **PRODUCTION-READY**

---

## APPROVAL

✅ «ОДОБРЯЮ TELEGRAM PRODUCTION SINGLE-USER» — получено.

---

## АКТИВНЫЕ ЗАЩИТЫ

| Защита | Статус |
|--------|--------|
| Owner-only chat_id | ✅ Активна |
| Чужие chat_id | 🚫 Блок |
| Обычный язык | ✅ Без команд |
| Preview → confirm | ✅ Всегда |
| Delete | 🚫 Запрещён |
| Overwrite | 🚫 _vN only |
| Vision | 🚫 DISABLED |
| Google Drive | 🚫 DISABLED |
| Git push | 🚫 DISABLED |
| Corel/ArtCAM/CNC | 🚫 DISABLED |
| Production DB | 🚫 Без подтверждения |
| Token/.env | 🚫 NOT READ |
| Audit log | ✅ Каждое изменение |

---

## ЧТО НУЖНО ДЛЯ ФАКТИЧЕСКОГО ЗАПУСКА POLLING

Пользователь должен сам запустить бота (я не могу):

```bash
cd C:\Users\user\Desktop\Hermes-Clean
python src/hermes_clean/telegram_flow.py
```

Или через Hermes Agent gateway:
```bash
hermes gateway run
```

---

## КАК ОСТАНОВИТЬ

```
Ctrl+C  — остановить polling
```

---

## ROLLBACK

```
cd C:\Users\user\Documents\Codex\Malyarka_Desktop_Archive_2026-05-29\python_test
mv bot_archive_20260703.py bot.py
```

Мгновенный возврат к старому боту.

---

## РАЗРЕШЁННЫЕ ДЕЙСТВИЯ (через Telegram)

| Действие | Статус |
|----------|--------|
| Принять заказ текстом | ✅ |
| Показать preview | ✅ |
| Исправление | ✅ |
| Статус проекта | ✅ |
| Что дальше | ✅ |
| Draft цен | ✅ |
| Draft ЛКМ | ✅ |
| Backup по просьбе | ✅ |

## ЗАПРЕЩЁННЫЕ ДЕЙСТВИЯ

| Действие | Статус |
|----------|--------|
| Удаление файлов | 🚫 |
| Overwrite | 🚫 |
| Доступ/роли | 🚫 |
| Настройки backup | 🚫 |
| Vision | 🚫 |
| Google Drive | 🚫 |
| Git push | 🚫 |
| Corel/ArtCAM/CNC | 🚫 |
| Production DB | 🚫 |
| Token/.env | 🚫 |

---

## СТАТУС

**TELEGRAM_PRODUCTION_SINGLE_USER_APPROVED**

Approval получен. Защиты активны. Polling ждёт запуска пользователем.
