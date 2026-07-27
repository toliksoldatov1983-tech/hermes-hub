# BATCH_077_TELEGRAM_FLOW_LOCAL_RUNNER_REPORT

Date: 2026-07-01

## Summary

BATCH_077 added a safe local runner for the Malyarka Telegram-style dialog flow.

The runner proves that the project can locally execute:

- clean order path;
- disputed order path;
- dispute questions;
- dry-run dispute resolution;
- preview generation;
- export policy check;
- final report step.

## Created

- `src/hermes_clean/telegram_flow_runner.py`
- `tools/run_telegram_flow.py`
- `scripts/telegram_flow.cmd`
- `tests/test_telegram_flow_runner.py`
- `docs/TELEGRAM_FLOW_LOCAL_RUNNER.md`

## Updated

- `src/hermes_clean/__init__.py`
- `src/hermes_core/cli.py`
- `src/hermes_core/command_help.py`
- `src/hermes_core/smoke.py`

## Safety

The runner is local-only.

It does not:

- start Telegram;
- read Telegram tokens;
- read `.env`;
- call external APIs;
- touch real orders;
- write export files;
- change Google Drive;
- delete or move files.

## Checks

- `scripts\telegram_flow.cmd --case disputed` passed.
- `python tools\run_telegram_flow.py --case clean` passed.
- `pytest tests\test_telegram_flow_runner.py -q` passed: 4 tests.
- `scripts\run_tests.cmd` passed: 176 tests.
- `scripts\hermes.cmd project-audit` passed: OK, 25 checks, 0 failed.
- `scripts\hermes.cmd smoke` passed: OK, 21 checks, 0 failed.
