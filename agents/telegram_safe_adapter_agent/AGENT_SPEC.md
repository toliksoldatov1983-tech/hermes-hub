# Telegram Safe Adapter Agent — AGENT_SPEC

Date: 2026-06-17
Status: `accepted` (not active)
Registry: `agents/AGENT_REGISTRY.md` (#4)
Telegram API: NOT connected | Polling/webhook: NOT started | Token/.env/config.py: FORBIDDEN | Live bot: NOT touched

---

## Роль

**Telegram Safe Adapter Agent** — безопасный слой между Hermes agents и Telegram.

## Цель

```text
Agent output → Safe Adapter → Telegram (только после live-разрешения)
```

## Что делает (будущее)

1. Принимает структурированные сообщения от агентов
2. Проверяет safety rules перед отправкой
3. Форматирует сообщение для Telegram
4. Отправляет ТОЛЬКО после live-разрешения

## Что запрещено (hard stop)

- ❌ Подключать Telegram API
- ❌ Запускать polling / webhook
- ❌ Читать token / .env / config.py / os.environ
- ❌ Трогать live Telegram бот
- ❌ Отправлять сообщения без live-разрешения
- ❌ Читать secrets
- ❌ Работать с сервером

## Режимы

| Режим | Разрешено | Запрещено |
|-------|-----------|-----------|
| `offline` | Только planning | Telegram, API, live |
| `live` (после разрешения) | Отправка сообщений | Server, secrets |

## Статус

`accepted` (not active) — спецификация принята пользователем.
Не active. Telegram не подключать.
