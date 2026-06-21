# BATCH_020 — Vision: Gemini photo recognition for orders

Дата: 2026-06-21
Статус: IN PROGRESS

---

## Цель

Пользователь отправляет фото/скриншот заказа в Telegram → бот через Gemini извлекает размеры → парсинг как обычный заказ.

---

## Что уже есть

- `malyarka_vision/gemini.py` — заглушка, не вызывает API
- `malyarka_vision/config.py` — `real_recognition_enabled = False`
- Google API ключ на сервере
- Обработчик фото: `handle_photo_message()` в handlers.py (тоже заглушка)

---

## Что сделать

1. Включить `real_recognition_enabled = True` в config.py
2. Реализовать вызов Gemini API в gemini.py (отправить фото → получить текст)
3. Обновить `handle_photo_message()` — вызвать Gemini, получить размеры, отдать парсеру
4. Результат: фото → размеры → парсинг → Excel/Corel

---

## Разрешено

- Править `malyarka_vision/gemini.py`, `config.py`
- Править `malyarka_telegram/handlers.py` (handle_photo_message)
- Использовать Google API ключ из env
- Перезапустить бота для теста

## Запрещено

- Менять order flow
- Трогать adapter
- Production
- Читать .env содержимое
