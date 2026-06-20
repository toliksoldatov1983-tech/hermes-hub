# Codex Hermes Sync Protocol

Date: 2026-06-20

Status: `ACTIVE`

## Purpose

Create a shared markdown-based protocol for ChatGPT, Codex and Hermes.

The roles do not have automatic shared memory. The shared truth must be written into project markdown files.

## Sources Of Truth

Primary sync folder:

```text
E:\Hermes-Hub\sync
```

Project state/handoff:

```text
E:\Hermes-Hub\HERMES_HUB_STATE.md
E:\Hermes-Hub\tasks\NEXT_TASKS.md
E:\Hermes-Hub\handoff\START_NEW_CHAT_PROMPT.md
E:\Hermes-Hub\handoff\HERMES_NAVIGATION_INDEX.md
E:\Hermes-Hub\handoff\REPORT_TO_CHATGPT.md
E:\Hermes-Hub\handoff\CHATGPT_CONTEXT_BUNDLE.md
E:\Hermes-Hub\logs\WORKLOG.md
```

## Codex To Hermes

Codex writes results for Hermes into:

```text
E:\Hermes-Hub\sync\CODEX_TO_HERMES.md
E:\Hermes-Hub\sync\SHARED_CURRENT_STATUS.md
E:\Hermes-Hub\sync\DONE_LOG.md
```

## Hermes To Codex

Hermes writes micro reports using:

```text
E:\Hermes-Hub\sync\HERMES_TO_CODEX.md
```

If Hermes finds a blocker, it records it in:

```text
E:\Hermes-Hub\sync\BLOCKERS.md
```

## ChatGPT Decisions

ChatGPT/user decisions are recorded in:

```text
E:\Hermes-Hub\sync\CHATGPT_DECISIONS.md
E:\Hermes-Hub\sync\APPROVAL_GATES.md
```

## Large Context

Large context goes through:

```text
C:\Users\user\Desktop\HERMES_PACKET_INBOX
```

## Packet Launch Standard

Rule:

```text
NO_MANUAL_CMD_ONE_LINERS_FOR_PACKET_WORKFLOW
```

Do not make the user manually paste long CMD/PowerShell one-line commands for packet workflow.

Preferred user-facing flow:

1. Use a ready launcher `.cmd` / `.ps1`.
2. Launcher finds the ZIP.
3. Launcher extracts the ZIP.
4. Launcher finds `01_CODEX_TASK_*.md`.
5. Launcher creates `CODEX_PROMPT.txt`.
6. Launcher copies prompt to clipboard.
7. Launcher opens prompt in Notepad.
8. Launcher opens/selects the task file or folder if possible.

If a manual terminal command is still needed, ask first and keep it short.

## No-Touch Rule

Sync updates must not imply server, service, secrets, code, git, Phase 2 or production actions.

## 2026-06-20 — SIMPLE_CHATGPT_TO_CODEX_PROMPT_WORKFLOW_RESTORED

Active status:

```text
SIMPLE_CHATGPT_TO_CODEX_PROMPT_WORKFLOW_RESTORED
```

Active workflow:

1. Main task transfer to Codex is prompt text directly in ChatGPT.
2. ZIP / launcher / HERMES_PACKET_INBOX / LATEST_TASK_PATH are not used by default.
3. Launcher scripts are no longer the main workflow.
4. HERMES_PACKET_INBOX is no longer the main workflow.
5. Long user-facing CMD/PowerShell one-liners are not the main workflow.
6. If large context is needed, first agree on a simple file/ZIP separately, but still provide the prompt text in ChatGPT.
7. Always additionally provide the prompt text in ChatGPT.

Superseded / not active by default:

- NO_MANUAL_CMD_ONE_LINERS_FOR_PACKET_WORKFLOW
- SCRIPT_LAUNCHER_WORKFLOW_RULE_READY
- HERMES_PACKET_INBOX as default workflow

Still active:

- E:\Hermes-Hub\sync
- Codex/Hermes/ChatGPT sync through markdown files
- Micro tasks -> Hermes / cheap agent
- Big batch -> Codex
- Shared state -> markdown sync/state/handoff files

No-touch: server, SSH, service, Telegram runtime, feature flag, secrets, DB/logs/orders, `.py` code, git, Phase 2 and production were not touched.
