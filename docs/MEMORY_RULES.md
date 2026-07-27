# MEMORY_RULES

Current project memory lives only in Hermes-Clean.

Old Obsidian, Open WebUI and Google Drive are archive sources, not truth.

Memory stores:

- user decisions;
- prohibitions;
- current tasks;
- completed stages;
- risks;
- pending approvals.

## Local memory store

Hermes-Clean reads local memory with:

```cmd
scripts\hermes.cmd memory
```

Allowed local memory files:

- `00_START/CURRENT_STATE.md`
- `00_START/PROJECT_DECISIONS.md`
- `00_START/PROJECT_PROHIBITIONS.md`
- `03_TASKS/NEXT_TASK.md`
- `03_TASKS/DONE.md`
- `03_TASKS/PENDING_APPROVALS.md`

Forbidden sources remain:

- Obsidian memory;
- Open WebUI memory;
- Google Drive documents;
- old archives;
- real orders;
- secrets.
