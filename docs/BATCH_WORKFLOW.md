# Batch Workflow

Updated: 2026-06-12

This file defines how ChatGPT, Codex and future Hermes should work without
micro-copying every small step.

## Main Idea

Work in batches.

One batch should contain enough context for Codex to work for a while without
asking the user to paste every small answer back and forth.

## Roles

| Role | Does |
|---|---|
| ChatGPT | Discusses with user, groups decisions, prepares `BATCH_PACKET`. |
| Codex | Executes safe parts of the batch, verifies, updates project files, reports one summary. |
| Hermes / Nous Portal | Later becomes the visual workspace that reads the same state files. |
| User | Confirms risky steps and final decisions. |

## Batch Size

A normal batch should include:

- 1 clear goal;
- 3-7 related tasks;
- safety limits;
- expected outputs;
- checks;
- files to update;
- user decisions that are still open.

Avoid batches that mix unrelated work, for example:

- architecture + Telegram launch + Vision + database migration;
- old Malyarka audit + production bot launch;
- UI design + real API calls.

## Batch Packet Format

```text
BATCH_PACKET:

GOAL:

CURRENT CONTEXT:

ACCEPTED DECISIONS:

TASKS:
1.
2.
3.

WHAT CODEX MAY DO WITHOUT ASKING:

WHAT CODEX MUST NOT TOUCH:

WHAT NEEDS USER CONFIRMATION:

EXPECTED RESULT:

CHECKS:

FILES TO UPDATE:

REPORT BACK TO CHATGPT:
```

## Large Batch Files

Large `BATCH_PACKET` texts should be stored as separate `.md` files in:

```text
E:\Hermes-Hub\handoff
```

Do not paste huge packet text into ChatGPT when a file can hold it.

In chat, paste only a short command with a file reference, for example:

```text
Прочитай файл E:\Hermes-Hub\handoff\BATCH_001_HERMES_CONTEXT_HANDOFF.md как BATCH_PACKET. Если ты не видишь файл, попроси меня загрузить или вставить его.
```

Recommended naming:

```text
BATCH_001_TOPIC_NAME.md
BATCH_002_TOPIC_NAME.md
BATCH_003_TOPIC_NAME.md
```

## Simple Handoff Files

For everyday work, use fixed handoff files:

```text
E:\Hermes-Hub\handoff\ACTIVE_BATCH.md
E:\Hermes-Hub\handoff\REPORT_TO_CHATGPT.md
E:\Hermes-Hub\handoff\CHATGPT_CONTEXT_BUNDLE.md
```

Meaning:

- `ACTIVE_BATCH.md` stores the current active package for Codex.
- `REPORT_TO_CHATGPT.md` stores the short Codex report that the user can paste back into ChatGPT.
- `CHATGPT_CONTEXT_BUNDLE.md` stores the portable context snapshot for ChatGPT.

Rule:

ChatGPT should not give long commands in chat. It should point to the active
package file.

Codex should write its short report into `REPORT_TO_CHATGPT.md` after executing
a meaningful package.

Short execution command:

```text
Выполни ACTIVE_BATCH
```

Standing Codex rules live here:

```text
E:\Hermes-Hub\AGENTS.md
```

Codex should use `AGENTS.md` as the durable project instruction file for the
one-command workflow.

When this command is used, Codex should:

1. read `E:\Hermes-Hub\handoff\ACTIVE_BATCH.md`;
2. find the current active package;
3. execute only the safe allowed parts;
4. write the user-facing report to `E:\Hermes-Hub\handoff\REPORT_TO_CHATGPT.md`;
5. refresh `E:\Hermes-Hub\handoff\CHATGPT_CONTEXT_BUNDLE.md`.

## Codex Execution Rule

Codex may complete all safe tasks in the batch without stopping after each
micro-step.

Codex must stop and ask only if:

- the batch asks to read or modify secrets;
- the batch asks to touch old Malyarka as an active system;
- there is a real risk of deleting or overwriting data;
- a required user decision is missing;
- a command would launch Telegram, Vision, external APIs or production services.

## End Of Batch Report

Codex should return one compact report:

```text
DONE:
CHANGED FILES:
CHECKS:
NOT DONE:
NEXT BATCH:
COPY TO CHATGPT:
```

## Context Bundle Update Rule

After each meaningful batch, Codex should update the portable ChatGPT bundle:

```text
E:\Hermes-Hub\tools\Update-ChatGPTContextBundle.ps1
```

Output file:

```text
E:\Hermes-Hub\handoff\CHATGPT_CONTEXT_BUNDLE.md
```

This keeps ChatGPT synchronized even though ChatGPT cannot read local files by
itself.

## State Patch Rule

After each meaningful batch, Codex should prepare/update:

```text
E:\Hermes-Hub\patches\LATEST_STATE_PATCH.md
```

Patch log:

```text
E:\Hermes-Hub\patches\PATCH_LOG.md
```

The patch is a short acceptance/review summary for ChatGPT.

It must include:

- what was accepted;
- what changed;
- what was not accepted;
- what is forbidden;
- touched files;
- untouched areas;
- next step.

The patch does not replace:

```text
E:\Hermes-Hub\HERMES_HUB_STATE.md
E:\Hermes-Hub\handoff\CHATGPT_CONTEXT_BUNDLE.md
E:\Hermes-Hub\handoff\REPORT_TO_CHATGPT.md
```

## Rule For ChatGPT

ChatGPT should not send Codex one tiny task at a time.

If the next work is not risky, ChatGPT should prepare a batch with several
safe related tasks.
