# START HERE FOR CODEX

You are working in the clean Hermes Hub workspace.

Always start by reading:

```text
E:\Hermes-Hub\HERMES_HUB_STATE.md
E:\Hermes-Hub\SAFETY_RULES.md
E:\Hermes-Hub\PROJECT_HINTS.md
E:\Hermes-Hub\tasks\NEXT_TASKS.md
E:\Hermes-Hub\logs\WORKLOG.md
```

If the task involves old Malyarka, also read:

```text
E:\Hermes-General\logs\CODEX_AUDIT_2026-06-12.md
E:\Hermes-General\logs\MALYARKA_GIT_DIFF_REVIEW_2026-06-12.md
```

## Codex Role

Codex implements, verifies and writes files.

Codex should:

- keep work inside `E:\Hermes-Hub` unless explicitly told otherwise;
- keep old Malyarka frozen;
- update state, worklog and next tasks after every meaningful stage;
- avoid secrets and external API calls;
- give the user full Win+R paths.

## Forbidden Without Separate Permission

```text
C:\Users\user\Desktop\malyarka_codex_work
C:\Users\user\Desktop\malyarka_memory_cleanup
.env
orders.db
.git
tokens
keys
Telegram launch
Vision
external APIs
old bot.py
```

## Output Style

Explain simply in Russian.

For folders, always give a full Win+R path.

