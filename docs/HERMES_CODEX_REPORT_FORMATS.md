# Hermes Codex Report Formats

Date: 2026-06-20

Status: `ACTIVE`

## Hermes Micro Report

```text
Micro task:
Checked:
Result:
Blocker:
No-touch:
Recommendation:
```

## Codex Batch Report

```text
Batch:
Created:
Updated:
Checks run:
Result:
No-touch:
Next step:
```

## ChatGPT Acceptance Summary

```text
Accepted:
Rejected:
Open questions:
Next direction:
Approval needed:
```

## Blocker Report

```text
Blocker:
Where found:
Why it blocks:
What was not touched:
Safe next step:
```

## No-Touch Confirmation

Use explicit confirmations:

```text
No server lifecycle action.
No secrets read.
No DB/log/order contents read.
No .py code changed.
No git/commit/push.
No production.
No Phase 2.
```

## Workflow Rule Confirmation

When relevant, reports should mention:

```text
NO_MANUAL_CMD_ONE_LINERS_FOR_PACKET_WORKFLOW
```

Meaning:

- user-facing packet launch should use launcher scripts;
- long CMD/PowerShell one-liners are not the default workflow;
- big context still goes through ZIP packages;
- shared state is recorded in markdown sync/state/handoff files.

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
