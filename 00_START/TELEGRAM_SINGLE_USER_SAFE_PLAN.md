# TELEGRAM SINGLE-USER SAFE PLAN

Дата: 2026-07-03 · Статус: **PLAN · LIVE НЕ ЗАПУЩЕН**

---

## 1. ДОСТУП

| Параметр | Значение |
|----------|----------|
| Кто | Только владелец |
| Клиенты | Нет |
| Сотрудники | Нет |
| Группы | Нет |
| Публичный | Нет |
| Метод | Single-user allowlist по chat_id |

---

## 2. ЧТО TELEGRAM МОЖЕТ ДЕЛАТЬ

| Действие | Условие |
|----------|---------|
| Принять текст заказа | ✅ Всегда |
| Показать preview | ✅ После разбора |
| Принять исправление | ✅ Correction mode |
| Менять цены | ✅ Только draft → preview → confirm |
| Менять ЛКМ | ✅ Draft first |
| Менять материалы | ✅ Draft first |
| Запустить backup | ✅ По просьбе владельца |
| Показать статус | ✅ Read-only |
| Показать следующий шаг | ✅ Read-only |
| Обновить статус заказа | ✅ Preview → confirm |

---

## 3. ЧТО TELEGRAM НЕ МОЖЕТ ДЕЛАТЬ

| Действие | Причина |
|----------|---------|
| Менять доступ / роли | 🚫 Owner only, Desktop |
| Менять настройки backup | 🚫 Owner only, Desktop |
| Удалять файлы | 🚫 Никогда |
| Перезаписывать заказы | 🚫 Только _vN |
| Запускать Vision API | 🚫 Отдельный план |
| Google Drive | 🚫 HOLD |
| Git push | 🚫 Без approval |
| CorelDRAW, ArtCAM, CNC | 🚫 Никогда |
| Менять правила без draft | 🚫 Draft first |
| Production database | 🚫 Без плана |

---

## 4. STOP CONDITIONS

Остановиться и не выполнять если:

- Неизвестный chat_id
- Попытка удаления / overwrite
- Disputed rows > 0
- Нет approval на draft
- Риск production-изменения без подтверждения
- Попытка доступа к запрещённым зонам
- Telegram token не валиден
- Backend недоступен

---

## 5. DRY-RUN ПРОВЕРКА

| Сценарий | Фраза | Ожидание |
|----------|-------|----------|
| Заказ | «Новый заказ: ...» | Preview, без export |
| Исправление | «Цвет другой» | Correction mode |
| Цена | «Поставь 25 000» | Draft, ждёт confirm |
| Backup | «Сделай backup» | Запускается |
| Статус | «Что по проекту?» | Read-only ответ |
| Запрет | «Удали этот заказ» | 🚫 Отказ |
| Запрет | «Добавь сотрудника» | 🚫 Отказ |
| Неизвестный | Сообщение от чужого chat_id | 🚫 Блок |

---

## 6. ROLLBACK

| Действие | Как откатить |
|----------|-------------|
| Остановить Telegram | Закрыть polling |
| Вернуть цену | Откат к archived значению |
| Вернуть норму ЛКМ | Откат к archived значению |
| Вернуть заказ | v2 не удаляется, v1 остаётся |
| Полный откат | Закрыть все gates, dry-run only |

---

## 7. НЕОБХОДИМО ДЛЯ LIVE

- [ ] Telegram bot token
- [ ] Single-user allowlist (chat_id)
- [ ] Approval phrase: «ОДОБРЯЮ TELEGRAM SINGLE-USER LIVE»
- [ ] Polling mode (не webhook)
- [ ] Все 10 dry-run сценариев PASS

---

## 8. СТАТУС

**TELEGRAM_SINGLE_USER_SAFE_PLAN_READY**

План готов. Live не запущен. Жду approval-фразу.
