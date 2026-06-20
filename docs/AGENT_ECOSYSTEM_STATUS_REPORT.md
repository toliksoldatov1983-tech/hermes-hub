# Agent Ecosystem Status Report

Date: 2026-06-17
Autopilot: HERMES_AUTOPILOT_001

## Агенты

| # | Агент | Статус | Тесты | Спецификация |
|---|-------|--------|-------|-------------|
| 1 | Sales + Client Intake | `accepted` (not active) | 48/48 ✅ | ✅ hardened |
| 2 | Malyarka Agent | `proposed` | — | AGENT_SPEC + SAFETY_RULES |
| 3 | Corel Export Agent | `proposed` | — | AGENT_SPEC |
| 4 | Telegram Safe Adapter | `planned` | — | — |
| 5 | Memory Agent | `planned` | — | — |
| 6 | Diagnostics Agent | `proposed` | — | AGENT_SPEC |

## Цепочка

```text
Клиент → #1 Sales Intake → #2 Malyarka → #3 Corel Export
              ✅                ⏳             ⏳
         (accepted)        (proposed)      (proposed)
```

## Что принято

- ✅ Agent Factory rules
- ✅ Sales + Client Intake Agent (accepted, hardened, 48/48 tests)
- ✅ HERMES_AUTOPILOT_001 (10 green tasks/pass)

## Что proposed (ждёт утверждения)

- ⏳ Malyarka Agent (#2)
- ⏳ Corel Export Agent (#3)
- ⏳ Diagnostics Agent (#6)

## Что planned

- 📋 Telegram Safe Adapter Agent (#4)
- 📋 Memory Agent (#5)

## Что запрещено (все агенты)

- 🔴 Сервер / SSH / live Telegram
- 🔴 Secrets / token / .env / config.py
- 🔴 Реальные заказы без разрешения
- 🔴 Production/staging code
- 🔴 Commit/push
- 🔴 Live ответы клиентам
