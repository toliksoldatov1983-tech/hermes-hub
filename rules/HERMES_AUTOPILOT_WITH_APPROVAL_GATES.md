# HERMES AUTOPILOT WITH APPROVAL GATES

Date: 2026-06-17
Rule ID: HERMES_AUTOPILOT_001
Mode: GREEN_SERIES_AUTOPILOT_200

## Лимиты

| Режим | Pass | Задач/pass | Макс. pass | Макс. задач |
|-------|------|-----------|-----------|------------|
| Автономный | 10 | 10 | 1 | 10 |
| Серийный | 200 | 10 | 20 | 200 |

## Зоны

🟢 **GREEN** — автономно до лимита
🟡 **YELLOW** — остановка + APPROVAL_REQUEST
🔴 **RED** — HARD STOP

## Серийный режим

Hermes выполняет до 20 pass подряд без запроса пользователя.
После каждого pass — краткий отчёт в WORKLOG.
Финальный отчёт — после серии или gate.

## Приоритет задач

1. Завершить текущий sprint
2. Tracking/recovery cleanup
3. Launch readiness / blockers / gate docs
4. Diagnostics/Memory workflow
5. Regression checklists
6. Sandbox/preplan docs
7. Operator runbooks
8. Registry/state/navigation updates
9. Stop before code/live/server/real orders
