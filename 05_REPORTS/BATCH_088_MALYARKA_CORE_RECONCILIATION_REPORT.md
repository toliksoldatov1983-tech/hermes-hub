# BATCH_088_MALYARKA_CORE_RECONCILIATION_REPORT

Date: 2026-07-02

## Summary

BATCH_088_MACRO_MALYARKA_CORE_RECONCILIATION completed as a safe local Codex block inside Hermes-Clean.

The main working Malyarka module remains:

```text
src\hermes_modules\malyarka
```

The reference / compatibility layer remains untouched:

```text
src\hermes_clean
```

No old Hermes executor was used.

## Implemented

- Added `validation_contract.py` for `MalyarkaOrder` validation.
- Added `dispute_questions.py` for local suggested questions from dispute reasons.
- Added `export_source_policy.py` to block real/archive/Drive/unknown sources.
- Hardened `export_contract.py` with source policy while keeping the old default synthetic behavior.
- Extended `export_preview.py` with `source_type` and blocked-source reason.
- Expanded synthetic Malyarka fixtures from 9 to 12.
- Updated Malyarka module exports in `__init__.py`.
- Updated `status.py` to include the new local contracts.

## Created Tests

- `tests\test_malyarka_validation_contract.py`
- `tests\test_malyarka_dispute_questions.py`
- `tests\test_malyarka_export_source_policy.py`
- `tests\test_malyarka_fixture_expansion.py`

## Verification

- `scripts\run_tests.cmd` passed: 299 tests.
- `scripts\hermes.cmd project-audit` passed: 25 checks, 0 failed.
- `scripts\hermes.cmd smoke` passed: 23 checks, 0 failed.
- `scripts\hermes.cmd malyarka-fixtures` passed: 12 fixtures.

## Safety

Not touched:

- `.env`, tokens, keys;
- Google Drive;
- live Telegram;
- polling/webhook;
- external APIs;
- real orders;
- archives;
- old projects;
- real export files;
- delete operations.

## Remaining Risks

- `src\hermes_clean` still exists and remains needed for compatibility tests and commands.
- Malyarka still has two supported local paths: main module and reference compatibility layer.
- Future dialog bridge work must keep existing CLI commands stable.

## Next Recommended Batch

```text
BATCH_089_MALYARKA_DIALOG_BRIDGE_TO_MAIN_MODULE
```

Goal: safely plan and then implement a bridge so Malyarka dialog flows can use `src\hermes_modules\malyarka` as the main source, while keeping `telegram-flow`, `malyarka-dialog` and `malyarka-transcript` dry-run only and compatible.
