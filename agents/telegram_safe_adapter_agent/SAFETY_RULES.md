# Telegram Safe Adapter Agent — SAFETY RULES

Date: 2026-06-17
Agent: Telegram Safe Adapter Agent (#4, `accepted`)

---

## Hard Stop (красная зона)

| Запрет | Почему |
|--------|--------|
| **Server / SSH** | Агент — интерфейс, не серверный код |
| **Live Telegram bot** | Существующий бот не трогать |
| **Telegram API calls** | Без live-разрешения — hard stop |
| **Polling / webhook** | Не запускать, не менять |
| **Token / .env** | Secrets — никогда не читать |
| **config.py / os.environ** | Secrets — никогда не читать |
| **Real order data** | Без разрешения — hard stop |

---

## Допустимо (только planning)

- Описание adapter contract
- Проектирование message format
- Планирование safety checks
- Future adapter layer design

---

## Режимы

| Режим | Статус |
|-------|--------|
| `offline` | Только markdown planning |
| `live` | Только после явного разрешения пользователя |

Переход в `live` — только после:
1. Утверждения спецификации (accepted)
2. Реализации Python-модуля
3. Прохождения safety checks
4. Явного live-разрешения
