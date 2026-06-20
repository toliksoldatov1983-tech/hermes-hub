# ChatGPT Chat Roles

Updated: 2026-06-12

This file explains how to use the ChatGPT project `HERMES HUB`.

## Main Rule

The user should not keep the workflow in memory.

ChatGPT, Codex and future Hermes / Nous Portal must use the same project files:

```text
E:\Hermes-Hub\HERMES_HUB_STATE.md
E:\Hermes-Hub\progress\PROGRESS_CARD.md
E:\Hermes-Hub\tasks\NEXT_TASKS.md
E:\Hermes-Hub\logs\WORKLOG.md
```

## ChatGPT Project

Project name in ChatGPT:

```text
HERMES HUB
```

## Chats

| Chat | Purpose |
|---|---|
| Главный чат для работы | Main control chat. Decisions, progress cards, next steps, task packets for Codex. |
| Инженер проекта Hermes Hub | Review chat. Architecture criticism, risks, checks, alternative plans. |
| Рабочий чат 0.0.1 | Drafts and temporary experiments. Nothing becomes official until moved to the state files. |
| Архив-перенос чат | Old-context transfer and archive review. Old Malyarka stays archive-only. |

## How To Work In The Main Chat

Use `Главный чат для работы` for normal project work.

ChatGPT should regularly show:

```text
Откуда пришли:
Где сейчас:
Куда идем:
Сколько примерно времени:
Что нужно решить:
```

If ChatGPT wants Codex to do work, it must prepare:

```text
TASK:
CONTEXT:
WHAT TO DO:
WHAT NOT TO TOUCH:
EXPECTED RESULT:
CHECKS:
FILES TO UPDATE:
```

## What Counts As Official

A decision is official only when it is written to one of these files:

```text
E:\Hermes-Hub\HERMES_HUB_STATE.md
E:\Hermes-Hub\decisions\DECISIONS.md
E:\Hermes-Hub\tasks\NEXT_TASKS.md
```

Chat messages alone are not enough.

## Safety

Do not touch without separate explicit permission:

```text
C:\Users\user\Desktop\malyarka_codex_work
C:\Users\user\Desktop\malyarka_memory_cleanup
.env
orders.db
.git
tokens
keys
passwords
Telegram launch
Vision
external APIs
old bot.py
```

