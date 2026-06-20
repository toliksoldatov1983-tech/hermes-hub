# BATCH 004 - Simple Handoff Workflow

Updated: 2026-06-12

Purpose:

Create a simpler ChatGPT <-> Codex exchange mode using fixed handoff files.

Status:

```text
prepared only
workflow package
no app code
no core implementation
no tests
```

Execution status:

```text
executed by Codex on 2026-06-12
```

## Short Command For ChatGPT

Paste only this short command into ChatGPT:

```text
Работаем через простой handoff-режим. Текущий пакет для Codex лежит в ACTIVE_BATCH.md, отчет Codex возвращает в REPORT_TO_CHATGPT.md, общий контекст лежит в CHATGPT_CONTEXT_BUNDLE.md. Если ты не видишь файлы, попроси меня загрузить нужный .md файл.
```

## BATCH_PACKET

```text
BATCH_PACKET:

GOAL:
Simplify ChatGPT <-> Codex exchange through fixed files:
E:\Hermes-Hub\handoff\ACTIVE_BATCH.md
E:\Hermes-Hub\handoff\REPORT_TO_CHATGPT.md
E:\Hermes-Hub\handoff\CHATGPT_CONTEXT_BUNDLE.md

CURRENT CONTEXT:
Project: Hermes Hub / Malyarka Clean.
Large batch packets already live in:
E:\Hermes-Hub\handoff

ChatGPT cannot see local files unless the user uploads/pastes them.
Codex can read and update local files.

TASKS:
1. Document ACTIVE_BATCH.md as the current active package for Codex.
2. Document REPORT_TO_CHATGPT.md as the short Codex report for pasting back into ChatGPT.
3. Document CHATGPT_CONTEXT_BUNDLE.md as the portable shared context.
4. Update BATCH_WORKFLOW.md.
5. Update HERMES_HUB_STATE.md.
6. Update tasks\NEXT_TASKS.md.
7. Update logs\WORKLOG.md.
8. Refresh CHATGPT_CONTEXT_BUNDLE.md through:
   E:\Hermes-Hub\tools\Update-ChatGPTContextBundle.cmd

RULES:
- ChatGPT should not give long commands in chat.
- ChatGPT should point to the active package file.
- Codex should read ACTIVE_BATCH.md when asked to execute the active batch.
- Codex should write a short result to REPORT_TO_CHATGPT.md after execution.
- After every meaningful batch, Codex should refresh CHATGPT_CONTEXT_BUNDLE.md.

WHAT CODEX MAY DO WITHOUT ASKING:
- Create or update handoff workflow documentation inside E:\Hermes-Hub.
- Create placeholder handoff files if the executing packet allows it.
- Update state, tasks and worklog.
- Refresh CHATGPT_CONTEXT_BUNDLE.md.

WHAT CODEX MUST NOT TOUCH:
- .env
- orders.db
- .git
- tokens
- keys
- Telegram
- Vision
- API
- old Malyarka as active system
- old bot.py
- commits
- push

WHAT MUST NOT BE DONE IN THIS PACKAGE:
- Do not implement the Malyarka Clean technical core.
- Do not write application code.
- Do not create tests.
- Do not connect Telegram, Vision, API, database or Docker.
- Do not use old Malyarka as an active system.

EXPECTED RESULT:
The project has a simple handoff workflow:

1. ChatGPT/user prepares or selects an active packet.
2. Active packet lives in ACTIVE_BATCH.md.
3. Codex executes the active packet only when explicitly asked.
4. Codex writes the short report to REPORT_TO_CHATGPT.md.
5. Codex refreshes CHATGPT_CONTEXT_BUNDLE.md.

CHECKS:
- Confirm BATCH_004 exists.
- Confirm workflow docs mention ACTIVE_BATCH.md, REPORT_TO_CHATGPT.md and CHATGPT_CONTEXT_BUNDLE.md.
- Confirm no application code, core implementation or tests were created.
- Confirm forbidden files and services were not touched.

FILES TO UPDATE:
E:\Hermes-Hub\handoff\BATCH_004_SIMPLE_HANDOFF_WORKFLOW.md
E:\Hermes-Hub\docs\BATCH_WORKFLOW.md
E:\Hermes-Hub\HERMES_HUB_STATE.md
E:\Hermes-Hub\tasks\NEXT_TASKS.md
E:\Hermes-Hub\logs\WORKLOG.md
E:\Hermes-Hub\handoff\CHATGPT_CONTEXT_BUNDLE.md

REPORT BACK:
Return a short Russian report:
- what was created;
- what was changed;
- what was not touched;
- whether CHATGPT_CONTEXT_BUNDLE.md was refreshed.
```

## Codex Execution Result

Created:

```text
E:\Hermes-Hub\handoff\ACTIVE_BATCH.md
E:\Hermes-Hub\handoff\REPORT_TO_CHATGPT.md
```

Simple command is now enabled:

```text
Выполни ACTIVE_BATCH
```

No application code was written.
No core implementation was created.
No tests were created.
No forbidden files or services were touched.

