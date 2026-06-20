# BATCH 001 - Hermes Context Handoff

Updated: 2026-06-12

Purpose:

Store the large `BATCH_PACKET` for Hermes context handoff so the user does not
need to paste long text into ChatGPT.

Execution status:

```text
executed by Codex on 2026-06-12
```

## Short Command For ChatGPT

Paste only this short command into ChatGPT:

```text
Прочитай файл BATCH_001_HERMES_CONTEXT_HANDOFF.md как большой BATCH_PACKET по теме Hermes context handoff. Если ты не видишь файл, попроси меня загрузить или вставить его. После чтения дай короткую карточку прогресса и подготовь следующий BATCH_PACKET для Codex только если нужна работа с файлами.
```

## BATCH_PACKET

```text
BATCH_PACKET:

GOAL:
Prepare a clean context handoff path between ChatGPT, Codex and future Hermes / Nous Portal.

CURRENT CONTEXT:
Project: Hermes Hub / Malyarka Clean.
Root folder: E:\Hermes-Hub
Main source of truth: E:\Hermes-Hub\HERMES_HUB_STATE.md
Portable ChatGPT context bundle: E:\Hermes-Hub\handoff\CHATGPT_CONTEXT_BUNDLE.md

ChatGPT cannot see local files by itself. It should use uploaded/pasted context bundles or batch files.
Codex can read and update local project files.
Hermes / Nous Portal is future visual workspace and should later read the same source-of-truth files.

ACCEPTED DECISIONS:
- Old Malyarka is archive-only, not active system.
- Work happens in E:\Hermes-Hub.
- Use batch workflow for larger blocks of work.
- Store large BATCH_PACKET texts in separate .md files under E:\Hermes-Hub\handoff.
- In chat, paste only a short command with a file reference.
- After meaningful Codex work, refresh CHATGPT_CONTEXT_BUNDLE.md.

TASKS:
1. Keep ChatGPT synchronized through CHATGPT_CONTEXT_BUNDLE.md.
2. Keep large handoff packets as separate .md files in E:\Hermes-Hub\handoff.
3. Use short chat commands that reference the packet file.
4. Ask Codex to verify real disk state when ChatGPT is uncertain.
5. Keep future Hermes / Nous Portal aligned with the same state files.

WHAT CODEX MAY DO WITHOUT ASKING:
- Read and update documentation inside E:\Hermes-Hub.
- Create handoff .md files inside E:\Hermes-Hub\handoff.
- Update progress, task, decision and worklog files.
- Refresh CHATGPT_CONTEXT_BUNDLE.md using the existing generator.

WHAT CODEX MUST NOT TOUCH:
- .env
- orders.db
- .git
- tokens
- keys
- passwords
- Telegram launch
- Vision
- external APIs
- old bot.py
- old Malyarka as an active system

WHAT NEEDS USER CONFIRMATION:
- Any real Telegram/API/Vision/database connection.
- Any work inside old Malyarka folders.
- Any background Windows automation.
- Any deletion or mass file move.

EXPECTED RESULT:
ChatGPT, Codex and future Hermes can pass large context safely using files instead of long chat messages.

CHECKS:
- Confirm the batch file exists.
- Confirm documentation says large BATCH_PACKET files belong in E:\Hermes-Hub\handoff.
- Confirm CHATGPT_CONTEXT_BUNDLE.md was refreshed.
- Confirm no forbidden files or services were touched.

FILES TO UPDATE:
E:\Hermes-Hub\handoff\BATCH_001_HERMES_CONTEXT_HANDOFF.md
E:\Hermes-Hub\docs\BATCH_WORKFLOW.md
E:\Hermes-Hub\logs\WORKLOG.md
E:\Hermes-Hub\handoff\CHATGPT_CONTEXT_BUNDLE.md

REPORT BACK TO CHATGPT:
Large batch packets are now stored as handoff .md files. ChatGPT should ask the user to upload/paste the file if it cannot see it. ChatGPT should not require the user to paste long packet text into chat.
```

## Codex Execution Result

Done:

- confirmed this batch file exists;
- confirmed large batch files are documented in `E:\Hermes-Hub\docs\BATCH_WORKFLOW.md`;
- confirmed `CHATGPT_CONTEXT_BUNDLE.md` should be refreshed after meaningful Codex work;
- confirmed forbidden zones remain forbidden.

No application code was written.
No old Malyarka files were touched.
No secrets were read.
No APIs, bots or services were launched.
