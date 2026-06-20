# Agent Routing Rules

Date: 2026-06-20

Status: `ACTIVE`

## ChatGPT

Use ChatGPT for:

- decisions;
- acceptance;
- large task framing;
- approval gates;
- choosing direction.

## Codex

Use Codex for:

- batch packets;
- implementation;
- docs/state updates;
- complex checks;
- local tests;
- repo/project file work;
- updating handoff and bundle.

Do not send Codex one-line micro tasks when they can be safely handled by Hermes.

## Hermes / Cheap Agent

Use Hermes/cheap agent for:

- safe micro-checks;
- short runtime checks;
- small summaries;
- blocker summaries;
- drafts;
- checking whether docs were updated.

Hermes must stop if a task needs:

- server lifecycle action;
- secrets;
- DB/log/order contents;
- code changes;
- git;
- Phase 2;
- production.

## User

The user gives approval for:

- live server actions;
- service lifecycle changes;
- secret-bearing reads;
- production;
- Phase 2;
- real orders.

## Packet Routing

- Small text: chat.
- Medium text: ask if receiver can accept approximately N characters.
- Large context: `HERMES_PACKET_INBOX`.
- Codex work: batch packets.
- Hermes work: micro reports.

## User-Facing Launcher Rule

```text
NO_MANUAL_CMD_ONE_LINERS_FOR_PACKET_WORKFLOW
```

For batch packet workflow, do not rely on long manual CMD/PowerShell one-liners pasted by the user.

Use launcher scripts as the primary user-facing mechanism:

- `.cmd` / `.ps1` launcher;
- auto-detect ZIP;
- extract;
- find `01_CODEX_TASK_*.md`;
- generate `CODEX_PROMPT.txt`;
- copy prompt to clipboard;
- open prompt in Notepad;
- show clear error if missing.

Manual terminal commands are exceptional and should be short, explicit, and only after asking the user.

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
