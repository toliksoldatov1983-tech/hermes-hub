# Server Bot Running State Decision Required

Date: 2026-06-20

Status: `DECISION_REQUIRED`

## Current State

The server Telegram bot is currently running after controlled start.

```text
ActiveState=active
SubState=running
MainPID=28149
Autostart=disabled
Feature flag=OFF
Production=not enabled
Phase 2=not continued
```

## Decision A — Leave Service Running

Meaning:

- keep the bot running;
- do not enable autostart;
- do not enable Hermes adapter flag;
- do not continue Phase 2;
- monitor only with read-only checks if needed.

## Decision B — Perform Controlled Stop

Meaning:

- stop service once using a future explicit approval;
- confirm inactive state;
- do not restart;
- do not enable/disable autostart;
- do not read secrets/logs/DB/orders.

Required future approval phrase:

```text
APPROVE_SERVER_BOT_CONTROLLED_STOP_ONCE
```

## Decision C — Prepare Phase 2 Dry-Run Plan Only

Meaning:

- create a plan for a later Hermes adapter dry-run;
- do not enable feature flag yet;
- do not run Phase 2 yet;
- no production.

Required future approval phrase for actual Phase 2 dry-run:

```text
APPROVE_HERMES_ADAPTER_PHASE2_DRY_RUN_ONCE
```

## Decision D — Discuss Autostart Enable Later

Meaning:

- create separate plan before any `systemctl enable`;
- include rollback and operational owner decision;
- not part of current running-state decision.

## Decision E — Discuss Production Later

Meaning:

- production is out of scope now;
- requires many gates after Phase 2;
- no real orders until separately approved.

## Default Safe Position

If no decision is made:

```text
Do not perform additional lifecycle actions.
Service remains running as currently observed.
Autostart remains disabled.
```

