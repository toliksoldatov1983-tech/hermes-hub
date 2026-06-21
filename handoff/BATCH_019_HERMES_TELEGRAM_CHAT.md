# BATCH_019 — Telegram Hermes Chat Mode

Дата: 2026-06-21
Статус: READY. Ждёт Codex.

---

## Цель

Добавить Hermes-режим в Telegram-бота. Пользователь пишет `/hermes <вопрос>`, бот отправляет вопрос в DeepSeek API с Hermes-промтом, возвращает ответ.

---

## Что уже есть

| Компонент | Где |
|-----------|-----|
| Бот рабочий | `/opt/malyarka-telegram-bot` |
| DeepSeek API | `deepseek-v4-pro` |
| Hermes-адаптер | Включён, проверен |
| System prompt | `E:\Hermes-General\agents\hermes-general\SYSTEM_PROMPT.md` |
| Правила безопасности | `docs/TELEGRAM_SAFE_COMMANDS.md` |

---

## Как должно работать

```
Пользователь: /hermes какие задачи сегодня?
       ↓
      Бот принимает /hermes
       ↓
      Отправляет запрос в DeepSeek API
      (model: deepseek-v4-pro, system: Hermes prompt)
       ↓
      DeepSeek отвечает как Hermes
       ↓
      Бот возвращает ответ пользователю
```

---

## Что нужно сделать (Codex)

### 1. Добавить обработчик `/hermes`

В `malyarka_telegram/handlers.py` (или `router.py`):

```python
@router.message(Command("hermes"))
async def hermes_chat(message: Message):
    text = message.text.replace("/hermes", "").strip()
    if not text:
        await message.answer("Напиши вопрос после /hermes")
        return
    
    # Отправить в DeepSeek
    response = await deepseek_ask(text)
    await message.answer(response)
```

### 2. Функция deepseek_ask()

Новый файл: `malyarka_core/hermes_chat.py`

```python
import aiohttp
import os

HERMES_SYSTEM_PROMPT = """..."""  # из SYSTEM_PROMPT.md

async def deepseek_ask(user_text: str) -> str:
    api_key = os.environ.get("DEEPSEEK_API_KEY")  # уже в .env
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": "deepseek-v4-pro",
                "messages": [
                    {"role": "system", "content": HERMES_SYSTEM_PROMPT},
                    {"role": "user", "content": user_text}
                ]
            }
        ) as resp:
            data = await resp.json()
            return data["choices"][0]["message"]["content"]
```

### 3. System prompt

Взять из `E:\Hermes-General\agents\hermes-general\SYSTEM_PROMPT.md`.
Добавить в начало: «Ты Hermes. Отвечай на русском, коротко, по делу.»

---

## Разрешено

- Добавить `/hermes` в handlers.py
- Создать `malyarka_core/hermes_chat.py`
- Использовать существующий DEEPSEEK_API_KEY
- Перезапустить бота после изменений
- Телеграм-тест: `/hermes привет`

## Запрещено

- Менять order flow
- Трогать adapter/hermes_adapter.py
- Включать production
- Читать .env содержимое (брать ключ из os.environ)
- Менять feature flag
- Git push

---

## Безопасность

| Проверка | Как |
|----------|-----|
| Hermes не видит заказы | `/hermes` — отдельная команда, order flow — отдельно |
| Hermes не меняет сервер | Только read-only ответы |
| DeepSeek ключ не раскрыт | Берётся из os.environ, не в коде |
| Бот не ломается | Новый handler, старые не трогаем |

---

## Проверка после установки

| # | Тест | Ожидаемый результат |
|---|------|-------------------|
| 1 | `/start` | Приветствие |
| 2 | `700 x 500` | Парсинг заказа |
| 3 | `/hermes привет` | Ответ от Hermes |
| 4 | `/hermes какие задачи?` | Список актуального |
| 5 | Excel для Corel | Работает |
| 6 | Файл Малярки | Работает |

---

## Approval

`APPROVE_HERMES_TELEGRAM_CHAT_MODE`

---

## Expected result

Пользователь пишет `/hermes вопрос` в Telegram с телефона → получает ответ от Hermes.
