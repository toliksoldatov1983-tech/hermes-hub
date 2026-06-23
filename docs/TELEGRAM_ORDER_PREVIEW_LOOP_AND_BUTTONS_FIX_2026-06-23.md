# Telegram order preview loop and extra buttons fix

Date: 2026-06-23
Executor: Codex

## Status

Fixed, deployed, and confirmed by the user in Telegram.

Current verified runtime:

```text
server: 178.104.95.187
service: malyarka-telegram-bot.service
service state: active/running
live path: /opt/malyarka-telegram-bot
local clean runtime: E:\Hermes-Hub\projects\malyarka-runtime-clean
tests: 441 passed
Telegram user sanity: order preview is shown correctly
```

## What happened

The user sent an order to the Telegram bot and reported that the bot looped.
The bot was stopped first to prevent repeated bad responses.

The likely behavior was:

- order-like text in neutral mode was routed to `suggest_order_mode`;
- the bot asked the user to switch to `/заказ` instead of parsing the order immediately;
- the live aiogram layer also attached the persistent main reply keyboard as a fallback;
- this made three unwanted buttons appear again.

## Root cause

Two separate pieces of logic combined into bad UX:

1. `malyarka_telegram/router.py`
   - neutral mode did not immediately parse size-like text;
   - it returned a route that suggested `/заказ`.

2. `malyarka_telegram/app.py`
   - when there was no inline result keyboard, the app sent the persistent main keyboard;
   - that keyboard showed the three mode buttons even when the user expected a clean order flow.

## Fix

Changed local clean runtime:

```text
E:\Hermes-Hub\projects\malyarka-runtime-clean\malyarka_telegram\router.py
E:\Hermes-Hub\projects\malyarka-runtime-clean\malyarka_telegram\app.py
```

Behavior after the fix:

- neutral-mode text like `1000*400` immediately switches to `ORDER`;
- the order parser runs immediately;
- the bot returns `Предпросмотр заказа`;
- the old `/заказ` hint is not shown for obvious order text;
- the persistent three-button reply keyboard is removed as fallback;
- only result-related inline buttons remain for a clean order:
  - `Скачать Excel для Corel`
  - `Скачать Файл Малярки`
  - `Скопировать для Corel`

Chat/ideas/engineer modes were kept separate:

- chat mode still does not auto-parse size-like text;
- engineer and ideas modes remain read-only/safe.

## Verification

Local:

```text
python -m pytest -q
441 passed
```

Deploy:

```text
ops/deploy_runtime_clean.ps1 -Apply
```

Server:

```text
systemctl is-active malyarka-telegram-bot.service -> active
recent journal -> clean
```

Server-side functional check:

```text
input: 1000*400
mode: order
has preview: true
has /заказ hint: false
buttons: Excel, Файл Малярки, copy for Corel
```

User confirmation:

```text
он дал мен предпросмор , все хорошо
```

## Deployment note

Deploy created a live backup before replacing runtime:

```text
/opt/malyarka-backups/malyarka-telegram-bot_before_runtime_clean_20260622_231531.tgz
```

Do not quote or reuse any Telegram token from chat history. Tokens were rotated earlier and must stay secret.

## Future rule

For Malyarka Telegram orders:

- obvious size/order text should parse immediately;
- do not force the user through `/заказ` for normal order entry;
- do not show generic mode buttons after order input;
- only show buttons directly related to the result.

