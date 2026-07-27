# Malyarka Dispute Classification Report

## Scope

This report uses only synthetic fixtures inside Hermes-Clean.
No real orders, client documents, old archives, Google Drive files, secrets, tokens or `.env` files were read.

## Summary

- total_disputes: 8
- blocks_final: True

## Categories

- FORMAT_ERROR: 3
- INVALID_QUANTITY: 3
- MISSING_ITEM: 1
- MISSING_UNIT: 1

## Severities

- HIGH: 7
- MEDIUM: 1

## Disputed Rows

- category=FORMAT_ERROR; severity=HIGH; raw=paint 2 bucket; action=Ask user to rewrite the row as item | quantity | unit.
- category=INVALID_QUANTITY; severity=HIGH; raw=paint | many | bucket; action=Ask user to replace quantity with a number.
- category=INVALID_QUANTITY; severity=HIGH; raw=paint | -1 | bucket; action=Ask user to provide a positive quantity.
- category=MISSING_ITEM; severity=HIGH; raw=| 1 | bucket; action=Ask user to provide the missing item name.
- category=MISSING_UNIT; severity=MEDIUM; raw=paint | 1 |; action=Ask user to provide the unit.
- category=FORMAT_ERROR; severity=HIGH; raw=broken row; action=Ask user to rewrite the row as item | quantity | unit.
- category=INVALID_QUANTITY; severity=HIGH; raw=paint | 0 | bucket; action=Ask user to provide a positive quantity.
- category=FORMAT_ERROR; severity=HIGH; raw=paint | 1 | bucket | extra; action=Ask user to rewrite the row as item | quantity | unit.

## Rule

Any disputed row blocks final export until the user confirms or fixes it.
