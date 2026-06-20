# README_FOR_CODEX.md
# BUNDLE_271_300_LOCAL_ADAPTER_IMPLEMENTATION_AND_TESTS

This bundle is part of the Hermes Hub accelerated conveyor.

## What to do

Follow `TASK.md`.

## Autonomy class

`AUTO_LOCAL_ONLY`

Meaning:

Можно выполнять автоматически только local sandbox actions explicitly described in this bundle. No server/live/secrets/real orders.

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
