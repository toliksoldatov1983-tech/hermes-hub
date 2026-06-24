# BATCH_024 — Подключить фото к Vision

Дата: 2026-06-24
Для: Codex

## Проблема

Модуль Vision (`malyarka_vision/openai_vision.py`) работает, но бот не использует его для фото. Фото падает в `handle_photo_message()` → «Фото пока без Vision».

## Что сделать

В `app.py` заменить обработку фото:

### Найти (строка ~675)
```python
else:
    await message.answer(handle_photo_message(), reply_markup=remove_reply_markup)
```

### Заменить на
```python
elif getattr(message, "photo", None) is not None:
    photos = getattr(message, "photo", [])
    if not photos:
        await message.answer("Фото не получено.", reply_markup=remove_reply_markup)
        return
    largest = max(photos, key=lambda p: getattr(p, "width", 0) or 0)
    file_id = getattr(largest, "file_id", None)
    if not file_id:
        await message.answer("Не удалось загрузить фото.", reply_markup=remove_reply_markup)
        return
    await message.answer("Распознаю фото...", reply_markup=remove_reply_markup)
    with tempfile.TemporaryDirectory(prefix="malyarka_photo_") as temp_dir:
        photo_path = Path(temp_dir) / "telegram_photo.jpg"
        telegram_file = await bot.get_file(file_id)
        await bot.download_file(telegram_file.file_path, photo_path)
        photo_bytes = photo_path.read_bytes()
        from malyarka_vision.openai_vision import recognize_order_photo
        recognized_text = recognize_order_photo(photo_bytes)
    if not recognized_text or recognized_text.startswith("Vision"):
        await message.answer(f"Не удалось распознать: {recognized_text}", reply_markup=remove_reply_markup)
        return
    response = build_live_text_response(
        text=recognized_text, user_id=resolve_message_user_id(message),
        session_store=session_store, config=config, write_obsidian_inbox=True,
    )
    reply_markup = _build_inline_copy_markup(response.copy_keyboard)
    await message.answer(
        f"Распознано:\n{recognized_text}\n\n{response.text}",
        reply_markup=reply_markup or remove_reply_markup,
    )
else:
    await message.answer(handle_photo_message(), reply_markup=remove_reply_markup)
```

## Сервер

root@178.104.95.187, ключ hetzner_hermes
Путь: /opt/malyarka-telegram-bot/
Бэкап: скопировать app.py перед правкой

## Проверка

- py_compile
- systemctl restart
- Отправить фото в бот → должно распознать
