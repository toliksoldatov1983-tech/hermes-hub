# BATCH 005 - One Command Codex Workflow

Updated: 2026-06-12

Purpose:

Simplify ChatGPT <-> Codex exchange to one short user command.

Status:

```text
prepared and applied
rules only
no Run-ActiveBatch.cmd
no app code
no tests
```

## Short Command

The user can write to Codex:

```text
Выполни ACTIVE_BATCH
```

Codex should then use the standing project rules in:

```text
E:\Hermes-Hub\AGENTS.md
```

## BATCH_PACKET

```text
BATCH_PACKET:

GOAL:
Create standing Codex rules so normal work can start from one short command:
"Выполни ACTIVE_BATCH."

CURRENT CONTEXT:
Project: Hermes Hub / Malyarka Clean.
Root folder: E:\Hermes-Hub
Simple handoff files:
E:\Hermes-Hub\handoff\ACTIVE_BATCH.md
E:\Hermes-Hub\handoff\REPORT_TO_CHATGPT.md
E:\Hermes-Hub\handoff\CHATGPT_CONTEXT_BUNDLE.md

TASKS:
1. Create or update E:\Hermes-Hub\AGENTS.md.
2. Tell Codex to read CHATGPT_CONTEXT_BUNDLE.md before work.
3. Tell Codex to take the active task from ACTIVE_BATCH.md.
4. Tell Codex to write the report to REPORT_TO_CHATGPT.md.
5. Tell Codex to refresh CHATGPT_CONTEXT_BUNDLE.md after meaningful packages.
6. Tell Codex not to touch forbidden files/services without separate permission.
7. Update BATCH_WORKFLOW.md.
8. Update HERMES_HUB_STATE.md.
9. Update tasks\NEXT_TASKS.md.
10. Update logs\WORKLOG.md.
11. Do not create Run-ActiveBatch.cmd yet.
12. Refresh CHATGPT_CONTEXT_BUNDLE.md.

WHAT CODEX MUST NOT TOUCH:
- .env
- orders.db
- .git
- tokens
- keys
- Telegram
- Vision
- API
- Docker
- old Malyarka as active system
- old bot.py
- commits
- push

EXPECTED RESULT:
The one-command workflow is documented and ready:
"Выполни ACTIVE_BATCH."

CHECKS:
- Confirm AGENTS.md exists.
- Confirm Run-ActiveBatch.cmd was not created.
- Confirm forbidden files/services were not touched.
- Confirm CHATGPT_CONTEXT_BUNDLE.md was refreshed.

FILES TO UPDATE:
E:\Hermes-Hub\AGENTS.md
E:\Hermes-Hub\handoff\BATCH_005_ONE_COMMAND_CODEX_WORKFLOW.md
E:\Hermes-Hub\docs\BATCH_WORKFLOW.md
E:\Hermes-Hub\HERMES_HUB_STATE.md
E:\Hermes-Hub\tasks\NEXT_TASKS.md
E:\Hermes-Hub\logs\WORKLOG.md
E:\Hermes-Hub\handoff\CHATGPT_CONTEXT_BUNDLE.md

REPORT BACK:
Return a short Russian report:
- what was created;
- what was changed;
- whether AGENTS.md was created;
- whether "Выполни ACTIVE_BATCH" is ready;
- what was not touched;
- whether bundle was refreshed;
- whether secret patterns were found.
```

