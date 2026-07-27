# CONTEXT_REFRESH_RULES

Update this memory layer after every large batch.

## Files To Refresh

Always update:

- `00_MEMORY\ACTIVE_CONTEXT.md`
- `00_MEMORY\COMPACT_STATE_FOR_AGENTS.md`
- `00_START\CURRENT_STATE.md`
- `03_TASKS\DONE.md`
- `03_TASKS\NEXT_TASK.md`
- `05_REPORTS\REPORT_TO_USER.md`

Update when relevant:

- `00_MEMORY\PROJECT_MEMORY_INDEX.md`
- `00_MEMORY\CONTEXT_LOAD_POLICY.md`
- `00_MEMORY\START_NEW_HERMES_CHAT_PROMPT.md`
- `00_MEMORY\START_NEW_CODEX_CHAT_PROMPT.md`
- `00_MEMORY\DO_NOT_AUTOLOAD.md`
- `START_HERE.md`
- `docs\USER_RUNBOOK_RU.md`

## What To Record

Record only:

- completed batch name;
- changed high-level area;
- latest verified checks;
- next large task;
- enabled/disabled subsystem changes;
- new safety risks or gates;
- new files that are important for future context.

Do not paste full reports into memory.
Do not paste source code into memory.
Do not paste test logs unless they are short and directly relevant.

## Length Limits

- `ACTIVE_CONTEXT.md`: keep under 150-250 lines.
- `COMPACT_STATE_FOR_AGENTS.md`: keep one-screen if possible.
- Start prompts: keep clean and copy-ready.

## If Context Usage Is Too High

If a new chat opens above 70% context usage:

1. Stop.
2. Identify what was autoloaded.
3. Use only the minimal startup files.
4. Ask user/ChatGPT for one narrow missing file if needed.

If a new chat opens at 100% context usage:

1. Do not execute the batch.
2. Do not read more project files.
3. Reduce context and restart from `00_MEMORY\START_NEW_HERMES_CHAT_PROMPT.md` or `00_MEMORY\START_NEW_CODEX_CHAT_PROMPT.md`.

