# Hermes Approval Gate Template

Date: 2026-06-17
Rule: `rules/HERMES_AUTOPILOT_WITH_APPROVAL_GATES.md`

## Когда использовать

При встрече 🟡 жёлтой зоны во время автопрохода.

## Шаблон

```text
HERMES APPROVAL REQUEST

task: <описание задачи>
zone: YELLOW
reason: <почему задача требует approval>

current_progress:
  green_completed: <N из 10>
  tasks_done:
    - <task_1>
    - <task_2>

risk:
  server: <true|false>
  secrets: <true|false>
  code_change: <true|false>
  integration: <true|false>

proposed_action: <что именно предлагается сделать>

user_decision_needed:
  - ACCEPT — выполнить задачу
  - REJECT — пропустить задачу
  - REVISE — изменить задачу и вернуть

no_touch:
  server: false
  secrets: false
  commit: false
```

## Лимиты

- Зелёная зона: до **10 задач** за проход
- Жёлтая зона: остановка после **каждой** задачи
- Красная зона: **немедленный** hard stop
