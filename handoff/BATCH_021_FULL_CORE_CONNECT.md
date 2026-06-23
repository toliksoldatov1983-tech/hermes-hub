# BATCH_021 — Connect Full Malyarka Core to Telegram Bot

Дата: 2026-06-24
Для: Codex

## Цель

Подключить ВЕСЬ чистый конвейер Malyarka Core в обработчик заказов Telegram-бота.

## Сейчас

Бот использует только `parse_size_line` — старый упрощённый вызов.
Новый код уже на сервере, но не подключён:
- `parse_sizes_text()` — разбор всего текста, confirmed + disputed
- `calculate_total_area_m2()` — расчёт площади
- `calculate_total_quantity()` — общее количество
- `OrderDraft` — черновик с confirmed/disputed
- `validation.py` — проверки

## Что сделать

1. Прочитать текущий обработчик заказа в handlers.py на сервере
2. Заменить старый вызов `parse_size_line` на полный конвейер:
   - `parse_sizes_text(text)` → OrderDraft
   - `calculate_total_area_m2(draft.items)` → площадь
   - `calculate_total_quantity(draft.items)` → количество
   - Показать disputed_items пользователю
3. Обновить формат ответа — показать confirmed, disputed, total area, total qty
4. Сделать бэкап handlers.py перед правкой
5. py_compile проверка
6. systemctl restart malyarka-telegram-bot

## Разрешено

- Править /opt/malyarka-telegram-bot/malyarka_telegram/handlers.py
- Читать /opt/malyarka-telegram-bot/malyarka_core/*.py
- Перезапустить бота для теста

## Запрещено

- Не трогать .env, токены, ключи
- Не трогать router.py, session.py, app.py
- Не трогать production-данные
- Не делать git push
