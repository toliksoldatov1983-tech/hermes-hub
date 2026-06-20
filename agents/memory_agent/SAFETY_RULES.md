# Memory Agent — SAFETY RULES

Date: 2026-06-17
Agent: Memory Agent (#5, `accepted`)

---

## Абсолютные запреты

| Запрет | Почему |
|--------|--------|
| **Сохранять спорное как подтверждённое** | Disputed ≠ confirmed |
| **Читать реальные заказы без разрешения** | Без live-разрешения — только test data |
| **Читать secrets** | Token, .env, config.py, os.environ |
| **Трогать сервер / live** | Агент работает локально |
| **Перезаписывать source of truth** | Без проверки источника |

---

## Source Priority

```text
1. STATE.md / INDEX.md / REPORTS   ← highest trust
2. Chat memory (сессия)            ← medium trust
3. Archive (старые записи)         ← lowest trust
```

При конфликте — приоритет выше.

---

## Формат записи

```yaml
memory_entry:
  source: "HERMES_HUB_STATE.md"
  confidence: "confirmed"
  timestamp: "2026-06-17T..."
  summary: "Агент #1 accepted, 48/48 tests"
  not_secret: true
```

## Статус

`proposed` — спецификация создана. Ждёт утверждения.
Не active. Secrets не читать. Спорное не сохранять.
