# CODEX_WORKFLOW_RU

Codex:

1. читает `AGENTS.md`;
2. работает крупными блоками;
3. обновляет state / done / report / next task;
4. не выполняет опасные действия без approval gate.

## Локальный статус задач

Проверить текущий task snapshot:

```cmd
scripts\hermes.cmd tasks
```

Команда читает только:

- `03_TASKS\ACTIVE_BATCH.md`
- `03_TASKS\NEXT_TASK.md`
- `03_TASKS\DONE.md`
- `03_TASKS\PENDING_APPROVALS.md`
