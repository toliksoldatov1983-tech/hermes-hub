# BATCH_080_MALYARKA_TRANSCRIPT_REPORTS

Date: 2026-07-01

## Summary

BATCH_080 added local markdown transcript reports for Malyarka dry-run dialogs.

## Created

- `src/hermes_clean/malyarka_transcript_report.py`
- `scripts/malyarka_transcript.cmd`
- `tests/test_malyarka_transcript_report.py`
- `docs/MALYARKA_TRANSCRIPT_REPORTS.md`
- `05_REPORTS/MALYARKA_DIALOG_TRANSCRIPT.md`
- `05_REPORTS/MALYARKA_DIALOG_TRANSCRIPT_CLEAN.md`

## Updated

- `src/hermes_clean/__init__.py`
- `src/hermes_core/cli.py`
- `src/hermes_core/command_help.py`
- `src/hermes_core/smoke.py`

## Safety

The transcript feature is local dry-run only.

It does not:

- start Telegram;
- read tokens or `.env`;
- call external APIs;
- touch real orders;
- write real export files;
- change Google Drive;
- touch old projects or archives.

## Checks

- `scripts\malyarka_transcript.cmd --script disputed --output MALYARKA_DIALOG_TRANSCRIPT.md` passed.
- `scripts\hermes.cmd malyarka-transcript --script clean --output MALYARKA_DIALOG_TRANSCRIPT_CLEAN.md` passed.
- `pytest tests\test_malyarka_transcript_report.py -q` passed: 3 tests.
- `scripts\run_tests.cmd` passed: 255 tests.
- `scripts\hermes.cmd project-audit` passed: 25 checks, 0 failed.
- `scripts\hermes.cmd smoke` passed: 23 checks, 0 failed.
