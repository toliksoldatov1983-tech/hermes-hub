# BATCH_079_MALYARKA_DIALOG_COMMANDS_REPORT

Date: 2026-07-01

## Summary

BATCH_079 added local operator-style Malyarka dialog commands.

The new command path supports:

- `/order <text>`;
- `/questions`;
- `/resolve-delete <id>`;
- `/resolve-all-delete`;
- `/preview`;
- `/export`;
- `/report`;
- `/reset`;
- `/help`.

## Created

- `src/hermes_clean/malyarka_dialog_commands.py`
- `scripts/malyarka_dialog.cmd`
- `tests/test_malyarka_dialog_commands.py`
- `docs/MALYARKA_DIALOG_COMMANDS.md`

## Updated

- `src/hermes_clean/__init__.py`
- `src/hermes_core/cli.py`
- `src/hermes_core/command_help.py`
- `src/hermes_core/smoke.py`

## Safety

The command layer is dry-run only.

It does not:

- start Telegram;
- read tokens or `.env`;
- call external APIs;
- touch real orders;
- write export files;
- change Google Drive;
- touch old projects or archives.

## Checks

- `scripts\malyarka_dialog.cmd --script disputed` passed.
- `scripts\hermes.cmd malyarka-dialog --script clean` passed.
- `pytest tests\test_malyarka_dialog_commands.py -q` passed: 5 tests.
- `scripts\run_tests.cmd` passed: 219 tests.
- `scripts\hermes.cmd project-audit` passed: 25 checks, 0 failed.
- `scripts\hermes.cmd smoke` passed: 22 checks, 0 failed.
