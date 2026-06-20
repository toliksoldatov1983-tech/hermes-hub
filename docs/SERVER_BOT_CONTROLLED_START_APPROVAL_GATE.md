# Server Bot Controlled Start Approval Gate

Date: 2026-06-20

Mode: markdown-only approval gate.

Status: `START_FORBIDDEN_UNTIL_EXACT_APPROVAL`

## Purpose

Define the exact user approval required before a future controlled service start.

## Required Approval Phrase

The only approval phrase for the future controlled start is:

```text
APPROVE_SERVER_BOT_CONTROLLED_START_ONCE
```

Without this exact phrase, do not start the service.

## Approval Scope

The phrase authorizes only a one-time controlled start flow:

1. precheck;
2. confirm feature flag OFF;
3. start service once;
4. check status;
5. perform safe Telegram phone test;
6. stop only if unsafe or if user explicitly selected start+stop scenario;
7. write report.

It does not authorize:

- restart;
- enable/autostart;
- production enable;
- Phase 2;
- feature flag changes;
- code edits;
- reading secrets;
- DB/log/order access;
- real orders.

## Conditions Before Accepting Approval

Before acting on approval, confirm:

- the user used the exact phrase;
- the target is `malyarka-telegram-bot.service`;
- no production or Phase 2 action is bundled into the request;
- no secrets/logs/DB/orders are requested;
- rollback/stop plan is accepted;
- report template is ready.

## Non-Approval Examples

These are not enough:

```text
да
+
запускай
делай дальше
можно
start
restart
Phase 2
```

## Stop Rule

If approval scope is unclear, stop and ask for the exact phrase.

