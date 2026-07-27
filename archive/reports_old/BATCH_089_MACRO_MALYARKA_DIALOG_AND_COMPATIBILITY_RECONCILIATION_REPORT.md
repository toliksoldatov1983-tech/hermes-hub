# BATCH_089_MACRO_MALYARKA_DIALOG_AND_COMPATIBILITY_RECONCILIATION_REPORT

Date: 2026-07-02

## Summary

BATCH_089 completed as a safe local Codex block inside Hermes-Clean.

The Malyarka dialog / transcript / telegram-flow dry-run path is now bridged to the main working module:

```text
src\hermes_modules\malyarka
```

The compatibility layer remains:

```text
src\hermes_clean
```

No old Hermes executor was used.

## Implemented

- Added `src\hermes_modules\malyarka\dialog_bridge.py`.
- `malyarka-dialog` now uses `hermes_modules.malyarka` through the compatibility wrapper.
- `malyarka-transcript` uses the same bridge and records `main_module`.
- `telegram-flow` runner now uses the main Malyarka dialog bridge.
- Default dialog dry-run scripts now use `item | quantity | unit`.
- Existing `src\hermes_clean` imports remain compatible.
- `hardening_adapter.py` remains intact.
- Telegram dry-run remains dry-run only.

## Compatibility Role

`src\hermes_clean` remains a reference / compatibility layer for:

- old import paths used by tests and CLI;
- transcript/report wrappers;
- `telegram-flow` command compatibility;
- RC2 hardening reference components;
- `hardening_adapter.py` compatibility checks.

It was not deleted, renamed or merged.

## Tests Added / Updated

- Added `tests\test_malyarka_dialog_bridge.py`.
- Added `tests\test_malyarka_compatibility_layer.py`.
- Added `tests\test_telegram_dry_run_safety_bridge.py`.
- Updated dialog command tests to verify `main_module=hermes_modules.malyarka`.
- Updated transcript tests to verify main module reference.
- Updated telegram-flow runner tests to use the main Malyarka format.

## Required Checks

Passed:

- `scripts\hermes.cmd malyarka-dialog`
- `scripts\hermes.cmd malyarka-transcript`
- `scripts\hermes.cmd telegram-flow`
- `scripts\hermes.cmd malyarka-status`
- `scripts\hermes.cmd malyarka-fixtures`
- `scripts\hermes.cmd malyarka-disputes`
- `scripts\hermes.cmd malyarka-combined`
- `scripts\hermes.cmd dashboard`
- `scripts\hermes.cmd daily-report`
- `scripts\hermes.cmd project-audit`
- `scripts\hermes.cmd smoke`
- `scripts\run_tests.cmd`

Additional command coverage also passed:

- `scripts\hermes.cmd malyarka-preview "paint | 2 | bucket"`
- `scripts\hermes.cmd malyarka-resolve "paint 2 bucket" --replacement "paint | 2 | bucket"`
- `scripts\hermes.cmd malyarka-workflow`
- `scripts\hermes.cmd malyarka-schema`
- `scripts\hermes.cmd malyarka-demo`
- `scripts\hermes.cmd malyarka-pricing`

## Verification Summary

- Tests: 309 passed.
- Project audit: 25 checks, 0 failed.
- Smoke: 23 checks, 0 failed.
- Malyarka fixtures: 12.
- Malyarka disputes: 8 disputes, 4 categories.
- Dialog bridge: `module=hermes_modules.malyarka`.
- Telegram flow: dry-run, 2 initial disputes resolved locally, export_ready=true.

## Safety

Confirmed by implementation and tests:

- `.env` was not read.
- Tokens were not read.
- Keys were not read.
- Google Drive was not touched.
- Live Telegram was not started.
- Polling/webhook were not started.
- Real orders were not used.
- External APIs were not called.
- No files were deleted.
- No old projects were changed.
- No archives were touched.
- No real export files were created.

## Risks / Remaining Tails

- `src\hermes_clean` is still required for compatibility imports and should not be removed.
- `src\hermes_modules\malyarka` is now the main dialog business source, but some old RC2 components remain reference-only.
- Future packaging should make the one-command launch path clearer for a user.

## Next Batch

```text
BATCH_090_PROJECT_PACKAGING_AND_ONE_COMMAND_LAUNCH
```

Goal: prepare a clean local packaging / launch layer so the user can run Hermes-Clean with one safe command, still without live Telegram, secrets, Google Drive, real orders or external APIs.
