# README_FOR_CODEX.md
# BUNDLE_481_510_SERVER_PATCH_FINAL_APPROVAL_GATE

This bundle is part of the Hermes Hub accelerated conveyor.

## What to do

Follow `TASK.md`.

## Autonomy class

`STOP_APPROVAL`

Meaning:

Остановиться. Требуется отдельное explicit approval gate.

## Safety

Do not touch:
- server;
- `/opt/malyarka-telegram-bot`;
- live Telegram bot;
- polling / webhook;
- Telegram API calls;
- token;
- `.env`;
- `config.py` contents;
- `os.environ`;
- database/log/order contents;
- real orders;
- private IDs;
- API keys;
- production/staging code;
- Vision/API;
- `.git`;
- commit/push;
- Corel / ArtCAM / CNC;
- export/admin/write actions unless an individual accepted bundle explicitly allows a local no-op or markdown-only operation.


## Report

Return a compact report and the next safe bundle.

If any uncertainty or gate appears, stop and use `STOP_AND_REPORT_TEMPLATE.md`.
