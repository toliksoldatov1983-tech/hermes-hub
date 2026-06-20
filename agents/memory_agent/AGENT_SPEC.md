# Memory Agent — AGENT_SPEC

Date: 2026-06-17
Status: `accepted` (not active)
Registry: `agents/AGENT_REGISTRY.md` (#5)
Source priority: state/index/reports > chat > archive

---

## Роль

**Memory Agent** — сервисный агент для хранения project memory и state summaries.

## Цель

```text
Agent events → Memory Agent → State summaries (без secrets)
```

## Что делает (будущее)

1. Принимает state updates от других агентов
2. Сохраняет структурированные summaries
3. Отвечает на запросы: «какой статус у X?»
4. Приоритет источников:
   - state/index/reports > чатовая память > архив

## Что запрещено

- ❌ Читать secrets (token, .env, config.py)
- ❌ Читать реальные заказы без разрешения
- ❌ Сохранять спорные данные как подтверждённые факты
- ❌ Трогать сервер / live
- ❌ Записывать в базу данных
- ❌ Перезаписывать source of truth без проверки

## Правила записи

- `source` — откуда данные
- `confidence` — confirmed / preliminary / disputed
- `timestamp` — когда записано
- Спорное (`disputed`) не сохранять как `confirmed`

## Статус

`accepted` (not active) — спецификация принята пользователем.
Не active. Secrets не читать.
