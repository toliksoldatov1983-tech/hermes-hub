# MALYARKA_MODULE_STATUS

Generated: 2026-07-28T03:17:06

## Ready Local Commands

- `scripts\hermes.cmd malyarka-preview`
- `scripts\hermes.cmd malyarka-fixtures`
- `scripts\hermes.cmd malyarka-resolve`
- `scripts\hermes.cmd malyarka-workflow`
- `scripts\hermes.cmd malyarka-status`

## Ready Contracts

- `order_contract`
- `parser_contract`
- `validation_contract`
- `preview_contract`
- `dispute_contract`
- `dispute_questions`
- `resolution_contract`
- `export_source_policy`
- `workflow`
- `export_contract gated stub`

## Gated Items

- real order access requires APPROVE_REAL_ORDER_ACCESS
- archive import requires APPROVE_MALYARKA_ARCHIVE_IMPORT or APPROVE_ARCHIVE_UNPACK
- real export requires a future explicit approval
- Excel integration is not enabled

## Safety

Malyarka status is local and synthetic. It does not read real orders, Excel files, Google Drive, old archives, secrets or client documents.
