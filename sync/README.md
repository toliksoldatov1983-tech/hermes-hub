# Hermes Hub Sync Layer

Date: 2026-06-20

Status: `CODEX_HERMES_SYNC_LAYER_READY`

## Purpose

This folder is the shared markdown sync layer between ChatGPT, Codex and Hermes.

There is no automatic shared memory between roles. Current state, decisions, handoffs, blockers and next work must be written here or into the project state/handoff files.

## Files

```text
SHARED_CURRENT_STATUS.md
CODEX_TO_HERMES.md
HERMES_TO_CODEX.md
CHATGPT_DECISIONS.md
NEXT_BATCH_QUEUE.md
MICRO_TASK_QUEUE.md
DONE_LOG.md
BLOCKERS.md
APPROVAL_GATES.md
```

## Routing

- ChatGPT: decisions, acceptance, large task framing.
- Codex: batch packets, implementation, docs, complex checks, state/handoff updates.
- Hermes/cheap agent: safe micro-checks, short runtime checks, summaries, drafts.
- User: approval gates and live-action decisions.

Large context uses `HERMES_PACKET_INBOX`.

