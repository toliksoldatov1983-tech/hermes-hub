# Batch Vs Micro Task Rules

Date: 2026-06-20

Status: `ACTIVE`

## Codex Batch Rule

Codex should receive coherent batch packets, not many one-line micro tasks.

Good Codex batch size:

```text
5-10 connected tasks
```

Codex is best for:

- multi-file updates;
- implementation;
- project state synchronization;
- tests;
- complex verification;
- preparing reports.

## Hermes Micro Rule

Hermes/cheap agent can handle micro tasks if safe:

- service status read-only;
- feature flag read-only;
- summarize a blocker;
- check if markdown exists;
- prepare a short status.

## Text Size Rule

- Short task: normal chat text.
- Medium task: ask if N characters can fit.
- Large task: ZIP through `HERMES_PACKET_INBOX`.

## Packet Workflow Launcher Rule

Rule:

```text
NO_MANUAL_CMD_ONE_LINERS_FOR_PACKET_WORKFLOW
```

Long manual CMD/PowerShell one-liners are no longer the primary way to unpack ZIP packages, select `LATEST_TASK_PATH.txt`, or launch batch packets.

New standard:

- user-facing batch launch should use ready `.cmd` / `.ps1` launcher scripts;
- the launcher should find the ZIP, extract it, find `01_CODEX_TASK_*.md`, create `CODEX_PROMPT.txt`, copy the prompt to clipboard, open it in Notepad, and preferably open/select the file in Explorer;
- if ZIP or task file is missing, the launcher must stop with a clear error;
- `HERMES_PACKET_INBOX` remains available as a legacy/additional mechanism;
- if a terminal command is still needed, ask the user first and provide the shortest safe command.

Routing summary:

- Micro tasks -> Hermes/cheap agent.
- Big batch -> Codex.
- Big context -> ZIP package.
- User-facing batch launch -> launcher script, not manual CMD.
- Shared state -> markdown sync/state/handoff files.

## Stop Conditions

Escalate to Codex batch or user approval if the task involves:

- server lifecycle;
- secrets;
- DB/log/order contents;
- `.py` changes;
- git;
- production;
- Phase 2;
- real orders.

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
