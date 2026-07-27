# BATCH_083_USER_DOCS_REFRESH

Date: 2026-07-01

## Summary

BATCH_083 refreshed user-facing documentation so it matches the current Hermes-Clean state.

## Updated

- `README.md`
- `START_HERE.md`
- `docs/WINDOWS_COMMANDS.md`
- `docs/USER_GUIDE_RU.md`
- `docs/WHAT_IS_DONE.md`
- `docs/WINDOWS_COMMANDS.md` coverage fix for `malyarka-resolve`

## Current State Reflected

- 35 CLI commands.
- 278 tests passed.
- 25 project-audit checks passed.
- 23 smoke checks passed.
- Telegram remains dry-run only.
- Malyarka remains synthetic/manual dry-run only.
- External/live systems remain approval-gated.

## Safety

This batch only updated local documentation.

It did not:

- read `.env`;
- read tokens or keys;
- call external APIs;
- start live Telegram;
- touch real orders;
- change Google Drive;
- change old projects or archives;
- delete files.

## Checks

- `scripts\run_tests.cmd` passed: 278 tests.
- `scripts\hermes.cmd project-audit` passed after command-doc fix: 25 checks, 0 failed.
- `scripts\hermes.cmd smoke` passed: 23 checks, 0 failed.
- `scripts\hermes.cmd release-checklist` passed.
