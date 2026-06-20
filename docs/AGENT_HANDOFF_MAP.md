# Agent Handoff Map

Date: 2026-06-17
Autopilot: GREEN_AUTOPILOT_PASS_10_AGENT_SPEC_REVIEW_AND_HANDOFF

## Цепочка агентов

```text
Client Message
    │
    ▼
┌─────────────────────────────┐
│ Sales + Client Intake (#1)  │  accepted, not active, 48/48
│                             │
│ Хаотичное сообщение         │
│ → структурированная         │
│   Intake Card               │
└─────────────┬───────────────┘
              │ HANDOFF_CONTRACT_TO_MALYARKA.md
              │ Условия: ready=true, no blocking flags
              ▼
┌─────────────────────────────┐
│ Malyarka Agent (#2)         │  accepted_as_spec, not active
│                             │
│ Intake Card                 │
│ → парсинг + площадь         │
│ → Preliminary Order Result  │
└─────────────┬───────────────┘
              │ OUTPUT_CONTRACT.md
              │ Статус: preliminary_result
              ▼
┌─────────────────────────────┐
│ Human Review                │  обязательный этап
│                             │
│ Проверка preliminary result │
│ → confirmed / revise        │
└─────────────┬───────────────┘
              │ (будущее)
              ▼
┌─────────────────────────────┐
│ Corel Export Agent (#3)     │  accepted_as_spec, not active
│                             │
│ Order Result                │
│ → Export Contract           │
│ → .cdr preparation data     │
└─────────────────────────────┘
```

## Статусы агентов в цепочке

| # | Агент | Статус | Активен? |
|---|-------|--------|----------|
| 1 | Sales + Client Intake | `accepted` | ❌ not active |
| 2 | Malyarka | `accepted_as_spec` | ❌ not active |
| 3 | Corel Export | `accepted_as_spec` | ❌ not active |
| — | Human Review | обязателен | всегда |

## Handoff contracts

| Контракт | Файл |
|----------|------|
| Sales → Malyarka | `agents/sales_client_intake_agent/HANDOFF_CONTRACT_TO_MALYARKA.md` |
| Malyarka Input | `agents/malyarka_agent/INTAKE_CONTRACT.md` |
| Malyarka Output | `agents/malyarka_agent/OUTPUT_CONTRACT.md` |

## Что пока не активно

- Corel Export: `accepted_as_spec`, код не писать, Corel не запускать
- Все агенты: `not active`, Telegram/live не подключены
- Handoff: только markdown contract, не активирован
