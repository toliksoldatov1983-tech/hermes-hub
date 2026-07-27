# MALYARKA_LOCAL_ONLY_SUMMARY

## Status

Malyarka is currently a local synthetic module inside Hermes-Clean.

## Ready Local Commands

- `scripts\hermes.cmd malyarka-preview`
- `scripts\hermes.cmd malyarka-fixtures`
- `scripts\hermes.cmd malyarka-resolve "paint 2 bucket" --replacement "paint | 2 | bucket"`
- `scripts\hermes.cmd malyarka-workflow`
- `scripts\hermes.cmd malyarka-status`
- `scripts\hermes.cmd malyarka-schema`
- `scripts\hermes.cmd malyarka-pricing`
- `scripts\hermes.cmd malyarka-demo`

## Ready Contracts

- order rows;
- parser;
- preview;
- dispute detection;
- dispute resolution;
- workflow summary;
- schema;
- export preview;
- synthetic pricing;
- module status.

## Synthetic-Only Rules

- Prices are fake.
- Customers are fake.
- Orders are fake.
- No Excel files are written.
- No real client documents are read.

## Gated

- Real orders require `APPROVE_REAL_ORDER_ACCESS`.
- Old Malyarka archives require `APPROVE_MALYARKA_ARCHIVE_IMPORT` or `APPROVE_ARCHIVE_UNPACK`.
- Real Excel export requires a separate future approval after schema confirmation.
- Client documents require separate approval.

## Checks

- `scripts\hermes.cmd smoke` — OK.
- `scripts\run_tests.cmd` — OK.
