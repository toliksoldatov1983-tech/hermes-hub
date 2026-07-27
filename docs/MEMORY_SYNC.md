# MEMORY_SYNC

## Purpose

Memory Sync is the local project memory registry for decisions, prohibitions, safety rules and pending approvals.

It is not old Hermes memory. It is not Obsidian memory. It is not Open WebUI memory. It is local Hermes-Clean state only.

## What It Stores

Memory Sync stores:

- project decisions;
- project prohibitions;
- safety rules;
- pending approvals;
- subsystem decisions;
- integrity checks.

## Main Local Objects

- `MemorySync`
- `SafetyViolation`
- `Decision`
- `Prohibition`
- `SafetyRule`
- `PendingApproval`
- `IntegrityReport`
- `Subsystem`

## Default Safety Meaning

Memory Sync blocks decisions that violate built-in prohibitions such as:

- external network use;
- real API keys;
- real tokens;
- direct database writes;
- live Telegram sending.

It also blocks unsafe secret patterns outside the approved provider setup path.

## Subsystems

Current subsystems:

- `GENERAL`
- `MALYARKA`
- `AI_PROVIDER`
- `TELEGRAM`
- `EXPORT`

## Approval Logic

Memory Sync can record pending approvals, but it does not bypass project safety gates.

Real action still requires the matching explicit approval gate, for example:

- `APPROVE_SECRET_SETUP`
- `APPROVE_TELEGRAM_LIVE`
- `APPROVE_REAL_ORDER_ACCESS`
- `APPROVE_GOOGLE_DRIVE_MOVE`

## Tests

Covered by:

```text
tests/test_memory_sync.py
```

The tests cover decisions, prohibitions, immutable decisions, pending approvals, integrity checks and `SafetyViolation` behavior.
