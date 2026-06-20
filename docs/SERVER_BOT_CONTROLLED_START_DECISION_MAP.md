# Server Bot Controlled Start Decision Map

Date: 2026-06-20

Mode: markdown-only decision map.

## Current Known State

```text
malyarka-telegram-bot.service exists
ActiveState=inactive
SubState=dead
is-enabled=disabled
adapter installed
feature flag should be OFF
production enable not performed
live dry-run not currently confirmed
```

## Option A — Keep Bot Stopped

Gate: green.

Meaning:

- do nothing on server;
- keep service inactive/dead;
- keep autostart disabled;
- do not proceed to Phase 2.

Use when:

- user wants zero live risk;
- startup is not needed today.

## Option B — One-Time Controlled Start

Gate: red approval.

Requires exact phrase:

```text
APPROVE_SERVER_BOT_CONTROLLED_START_ONCE
```

Meaning:

- precheck;
- confirm feature flag OFF;
- start service once;
- check service state;
- perform safe phone test;
- document result.

Does not include enable/autostart or production.

## Option C — Controlled Start + Stop

Gate: red approval.

Meaning:

- same as Option B;
- stop service after test;
- leave service inactive again.

Use when:

- user wants to verify startup only;
- user does not want the bot to remain running.

## Option D — Discuss Enable / Autostart Later

Gate: separate red approval.

Meaning:

- not part of controlled start;
- requires separate plan;
- must include rollback and monitoring.

## Option E — Discuss Phase 2 Dry-Run Later

Gate: separate red approval.

Meaning:

- not part of controlled start;
- requires confirmed running bot first;
- requires feature flag and diagnostics plan;
- production remains forbidden until separately approved.

## Recommended Next Step

Choose Option A, B, or C.

Default safe state is Option A:

```text
Keep bot stopped.
```

