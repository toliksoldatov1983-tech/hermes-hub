# MALYARKA_LOCAL_CONTRACTS_REPORT

## Block

BATCH_013_CONTINUE_MALYARKA_MODULE_LOCAL_CONTRACTS

## Done

Expanded Malyarka local contracts:

- `MalyarkaOrderRow`
- `RowStatus`
- local `ParserContract`
- preview with confirmed/disputed rows
- dispute summary
- export blocking contract

## Dry-run format

```text
item name | quantity | unit
```

## Checks

- `scripts\hermes.cmd malyarka-preview "краска | 2 | л"` — confirmed row, export still requires approval.
- `scripts\hermes.cmd malyarka-preview "краска 2 л"` — disputed row, export blocked.
- `python -m unittest discover -s tests` — OK, 24 tests.

## Safety

No real orders were read.

No old Malyarka archive was imported.

No Google Drive documents, Excel files, client sheets, secrets or external APIs were touched.
