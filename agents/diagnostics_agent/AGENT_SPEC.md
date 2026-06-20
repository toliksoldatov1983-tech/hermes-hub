# Diagnostics Agent — AGENT_SPEC

Date: 2026-06-17
Status: `accepted` (not active)
Registry: `agents/AGENT_REGISTRY.md` (#6)
Safe reports only | Secrets/server/live: FORBIDDEN

---

## Роль

**Diagnostics Agent** — сервисный агент для безопасной диагностики состояния Hermes Hub.

## Цель

```text
Запрос диагностики → Safe Report (без secrets/server/live)
```

## Что проверяет (safe-only)

- Статусы агентов в registry
- Наличие/отсутствие файлов (markdown presence)
- Последние результаты тестов (из known records)
- Состояние веток (server patch paused, agent factory active)
- Открытые блокеры

## Что НЕ проверяет

- ❌ Сервер (SSH, процессы, порты)
- ❌ Secrets (token, .env, config.py)
- ❌ Live Telegram (статус бота, polling)
- ❌ Базы данных / логи / реальные заказы
- ❌ Сетевые соединения

## Выходные данные

```yaml
diagnostics_report:
  timestamp: str
  agents:
    - name, status, tests_passed
  branches:
    - server_patch: paused
    - agent_factory: active
  blockers: list
  warnings: list
  safe_only: true
```

## Статус

`accepted` (not active) — спецификация принята пользователем.
Код не писать. Диагностику не запускать без разрешения. Secrets/server/live не трогать.
