# Server Bot Controlled Start Telegram Test Plan

Date: 2026-06-20

Mode: markdown-only test plan.

Status: `PLAN_ONLY_TELEGRAM_NOT_TOUCHED`

## Purpose

Define safe phone-side checks for a future approved controlled start of the server Telegram bot.

This document does not authorize sending messages now.

## Safe Test Messages

After future approved start, the user may send only safe, non-production messages.

Suggested safe messages:

```text
/start
```

```text
тест
```

```text
700 x 500
```

The last message is a dummy size check only. It is not a real order.

## Expected Results

Expected behavior:

- bot responds without crashing;
- no production enable;
- no real order is created;
- no Vision/API path is triggered;
- no real files are processed;
- no secrets are exposed;
- adapter feature flag remains OFF.

## What Not To Send

Do not send:

- real client orders;
- photos;
- drawings;
- `.cdr`, `.art`, `.xlsx` files;
- price requests;
- production commands;
- admin/write requests;
- token/config/env text;
- personal data;
- large archives.

## What Not To Test

Do not test:

- Vision;
- API;
- production export;
- DB writes;
- log-reading flows;
- real order workflow;
- Phase 2 adapter enable.

## Stop Conditions

Stop testing and perform the planned stop if:

- bot behaves unexpectedly;
- user sees production-like behavior;
- bot asks for secrets;
- bot tries to process real order data;
- multiple or repeated unexpected messages appear;
- service status becomes unstable.

## Report Required

After future phone test, record:

- exact safe messages sent;
- expected/actual response summary;
- whether bot stayed stable;
- whether stop was needed;
- final service state;
- no-touch confirmations.

