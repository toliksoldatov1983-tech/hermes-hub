# TELEGRAM_FLOW_LOCAL_RUNNER

## Purpose

This document describes the local Telegram-style Malyarka dialog runner.

It is not a real Telegram bot. It is a dry-run command that checks the local order dialog path:

1. receive order text;
2. detect disputed rows;
3. ask local clarification questions;
4. resolve disputes in dry-run mode;
5. build preview;
6. check export policy;
7. build final report summary.

## Safe Commands

```cmd
scripts\telegram_flow.cmd --case clean
scripts\telegram_flow.cmd --case disputed
scripts\hermes.cmd telegram-flow --case disputed
python tools\run_telegram_flow.py --case clean
```

## Safety

- No live Telegram polling.
- No webhook.
- No Telegram token.
- No `.env` reading.
- No external API.
- No real order access.
- No file export.
- No Google Drive change.

## Output

The command prints an ASCII-safe summary:

```text
telegram_flow=dry-run
scenario=disputed
confirmed_rows=1
initial_disputes=2
resolved_disputes=2
final_disputes=0
export_ready=true
blocked_actions=live_telegram_send,telegram_token_read,external_api_call,real_order_access,file_export_write
```

## Current Limit

This is a local test runner only. Real Telegram integration still requires `APPROVE_TELEGRAM_LIVE`.
