# START_NEW_CODEX_CHAT_PROMPT

Copy this into a new Codex chat.

```text
Continue «Гермес Клин» from:
C:\Users\user\Documents\«Гермес Клин»

Use minimal context only. Do not scan everything.

First read:
1. AGENTS.md
2. START_HERE.md
3. 00_MEMORY\PROJECT_MEMORY_INDEX.md
4. 00_MEMORY\USER_PROFILE.md
5. 00_START\CURRENT_STATE.md
6. 03_TASKS\NEXT_TASK.md
7. 05_REPORTS\REPORT_TO_USER.md
8. 00_MEMORY\ACTIVE_CONTEXT.md
9. 00_MEMORY\COMPACT_STATE_FOR_AGENTS.md
10. 00_MEMORY\CONTEXT_LOAD_POLICY.md

Do not load `E:\[архив] [удалённый архив]` or `E:\«Гермес Клин»`; they are obsolete.

Work in large batches, not microsteps.
Wait for the user's or ChatGPT's concrete batch task.
Do not invent new major tasks outside NEXT_TASK.md.

Forbidden without explicit approval:
- .env, tokens, keys;
- live Telegram, polling, webhook;
- external APIs;
- Google Drive writes/moves;
- real orders;
- old archives;
- old projects;
- delete operations.

When a batch is complete, update:
- 00_START\CURRENT_STATE.md
- 03_TASKS\DONE.md
- 03_TASKS\NEXT_TASK.md
- 05_REPORTS\REPORT_TO_USER.md
- 00_MEMORY\ACTIVE_CONTEXT.md
- 00_MEMORY\COMPACT_STATE_FOR_AGENTS.md
```

