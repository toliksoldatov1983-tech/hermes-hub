# Server Bot Startup Gated Plan Only

Technical name: `SERVER_BOT_STARTUP_GATED_PLAN_ONLY`

Date: 2026-06-20

Mode: markdown-only plan.

This document does not authorize starting, restarting, enabling, modifying, or deploying anything on the server.

## 1. Known Service Facts

Server:

```text
178.104.95.187
```

Project path:

```text
/opt/malyarka-telegram-bot
```

Systemd service:

```text
malyarka-telegram-bot.service
```

Current recorded service state:

```text
ActiveState=inactive
SubState=dead
is-enabled=disabled
```

Known entrypoint:

```text
/opt/malyarka-telegram-bot/.venv/bin/python -m malyarka_telegram.app --run-polling
```

Working directory:

```text
/opt/malyarka-telegram-bot
```

Service user:

```text
malyarka-bot
```

Current adapter state:

```text
Hermes adapter is installed.
Feature flag should be OFF according to project documents.
Live dry-run is not currently confirmed.
Production enable has not been performed.
Gate 9 must not be treated as complete without separate user decision.
```

## 2. Pre-Start Checks For A Future Approved Run

These checks are for a future approval-gated run only.

Allowed only after explicit approval:

```text
systemctl is-active malyarka-telegram-bot.service
systemctl is-enabled malyarka-telegram-bot.service
systemctl show malyarka-telegram-bot.service -p ExecStart -p WorkingDirectory -p User -p ActiveState -p SubState --no-pager
pgrep -af 'malyarka|telegram|aiogram|python'
```

The future pre-start check must confirm:

- service still exists;
- service is not already running twice;
- entrypoint is still the expected `--run-polling` command;
- working directory is `/opt/malyarka-telegram-bot`;
- service user is `malyarka-bot`;
- adapter files are present;
- feature flag is OFF before start;
- no production enable is requested.

Forbidden even during pre-start:

- reading `.env`;
- reading token values;
- reading `config.py` secret values;
- reading databases;
- reading logs;
- reading real orders;
- changing files;
- starting/restarting/enabling service without the dedicated start approval.

## 3. Confirming Feature Flag OFF

The feature flag must be confirmed OFF before any real start.

Preferred safe method for a future approved pre-start check:

- inspect only the non-secret adapter file containing the flag;
- do not read `.env`;
- do not read token/config secret values;
- do not change the flag.

Expected flag state:

```text
_HERMES_ADAPTER_ENABLED = False
```

If the flag cannot be confirmed safely, stop and request a separate decision.

## 4. Future Startup Command

The service start command for a future approved controlled run would be:

```text
systemctl start malyarka-telegram-bot.service
```

This command is not authorized by this document.

Do not run:

```text
systemctl restart malyarka-telegram-bot.service
systemctl enable malyarka-telegram-bot.service
```

unless the user gives separate explicit approval for those exact actions.

## 5. Post-Start Checks For A Future Approved Run

After a future approved start, check only operational status and safe process facts:

```text
systemctl is-active malyarka-telegram-bot.service
systemctl show malyarka-telegram-bot.service -p ActiveState -p SubState -p MainPID --no-pager
pgrep -af 'malyarka_telegram.app --run-polling'
```

Expected successful state:

```text
ActiveState=active
SubState=running
```

Do not read live logs unless separately approved.

Do not send Telegram messages unless separately approved.

Do not perform production validation unless separately approved.

## 6. Fast Stop / Rollback Command

If a future approved start causes an unexpected state, the fast stop command would be:

```text
systemctl stop malyarka-telegram-bot.service
```

After stop:

```text
systemctl is-active malyarka-telegram-bot.service
```

Expected stopped state:

```text
inactive
```

Do not enable autostart as part of rollback.

Do not modify adapter files as part of rollback unless separately approved.

## 7. Conditions Required Before Real Startup Approval

A real controlled startup may be considered only if all conditions are met:

- user gives separate explicit approval for controlled service start;
- approval names the exact service: `malyarka-telegram-bot.service`;
- approval confirms no service enable/autostart unless separately requested;
- pre-start checks are allowed;
- feature flag OFF is confirmed safely;
- adapter remains installed but not production-enabled;
- rollback/stop command is accepted;
- monitoring window is defined;
- secret-bearing files remain forbidden;
- no real orders or production workflow are involved;
- result must be documented after the run.

Suggested approval phrase:

```text
Разрешаю controlled service start только для malyarka-telegram-bot.service: pre-check, systemctl start, status check, no enable, no restart, no secrets, no logs/orders/db, feature flag must stay OFF, stop if unsafe.
```

## 8. Strictly Forbidden Without Separate Approval

Do not do any of the following without separate explicit approval:

- touch the server;
- start service;
- restart service;
- enable service/autostart;
- disable service/autostart;
- change feature flag;
- edit `.py` code;
- read `.env`;
- read `config.py`;
- read token;
- read `os.environ`;
- read databases;
- read logs;
- read real orders;
- send Telegram messages;
- call Telegram/API/network;
- run production workflow;
- use git/commit/push;
- change permissions;
- create/delete server files;
- perform deployment.

## 9. Current Safe Next Step

Stop here.

Next step requires a separate explicit approval for controlled service start, or a separate decision to keep the service stopped.

