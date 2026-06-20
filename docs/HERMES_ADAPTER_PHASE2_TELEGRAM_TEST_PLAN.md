# HERMES_ADAPTER_PHASE2_TELEGRAM_TEST_PLAN

Дата: 2026-06-20

## Purpose

Define a safe Telegram test for a future Hermes adapter Phase 2 dry-run.

Phase 2 is not started by this document.

## Safe test messages

Allowed test messages:

```text
/start
тест
700 x 500
```

## Expected safety boundaries

The test must use dummy data only.

No real customers, real orders, files, photos, personal data, production commands, Vision/API, or administrative changes are allowed.

## Forbidden during the test

- real orders;
- photos;
- files;
- personal data;
- production commands;
- Vision/API;
- price/material/rule changes;
- DB writes outside the existing bot flow;
- reading secrets.

## Report fields

Record only:

- whether bot responded;
- whether Hermes dry-run behavior appeared;
- whether fallback worked;
- whether rollback returned flag OFF;
- whether production stayed OFF.

