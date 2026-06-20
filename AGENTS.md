# AGENTS

Updated: 2026-06-12

These are the standing Codex rules for this project.

## Project Root

```text
E:\Hermes-Hub
```

## Before Work

Before doing project work, read:

```text
E:\Hermes-Hub\handoff\CHATGPT_CONTEXT_BUNDLE.md
```

## Active Task

When the user says:

```text
Выполни ACTIVE_BATCH
```

Codex must read:

```text
E:\Hermes-Hub\handoff\ACTIVE_BATCH.md
```

Then Codex must find the current active package named inside that file and
execute only the safe allowed parts.

## Report

After executing a meaningful package, write the short user-facing report to:

```text
E:\Hermes-Hub\handoff\REPORT_TO_CHATGPT.md
```

## Context Bundle

After every meaningful package, refresh:

```text
E:\Hermes-Hub\handoff\CHATGPT_CONTEXT_BUNDLE.md
```

by running:

```text
E:\Hermes-Hub\tools\Update-ChatGPTContextBundle.cmd
```

## Do Not Touch Without Separate Explicit Permission

```text
.env
orders.db
.git
tokens
keys
Telegram
Vision
API
Docker
old Malyarka as active system
old bot.py
commits
push
```

## Conveyor Rule

When the user says:

```text
Выполни ACTIVE_BATCH
```

or

```text
запускай конвейер
```

Codex must also read the conveyor rule:

```text
E:\Hermes-Hub\rules\HERMES_RULE_CONVEYOR_001.md
```

The conveyor is a semi-automatic bundle processor. Process bundles in MANIFEST order. Stop on STOP_REVIEW or STOP_APPROVAL gates. Never skip gates. Never touch server/live/runtime/secrets without separate explicit permission.

## Default Behavior

- Work inside `E:\Hermes-Hub` unless the user explicitly says otherwise.
- Keep old Malyarka archive-only.
- Prefer file-based handoff over long chat messages.
- Do not write application code unless the active package explicitly allows it.
- Do not create tests unless the active package explicitly allows it.
- Update `REPORT_TO_CHATGPT.md` and `CHATGPT_CONTEXT_BUNDLE.md` after meaningful work.

