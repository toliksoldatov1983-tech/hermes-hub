# Server Bot Controlled Start Command Plan

Date: 2026-06-20

Mode: future commands documented only.

Status: `PLAN_ONLY_COMMANDS_NOT_EXECUTED`

## Purpose

Document the future command sequence for a one-time controlled start of:

```text
malyarka-telegram-bot.service
```

None of these commands are executed by this plan.

## Future Read-Only Status Commands

Future precheck commands:

```text
systemctl is-active malyarka-telegram-bot.service
systemctl is-enabled malyarka-telegram-bot.service
systemctl show malyarka-telegram-bot.service -p FragmentPath -p ExecStart -p WorkingDirectory -p User -p LoadState -p ActiveState -p SubState --no-pager
pgrep -af 'malyarka|telegram|aiogram|python'
```

Expected before start:

```text
inactive
disabled
ActiveState=inactive
SubState=dead
```

## Future Start Command

Only after exact approval:

```text
systemctl start malyarka-telegram-bot.service
```

## Future Post-Start Status Commands

```text
systemctl is-active malyarka-telegram-bot.service
systemctl show malyarka-telegram-bot.service -p ActiveState -p SubState -p MainPID --no-pager
pgrep -af 'malyarka_telegram.app --run-polling'
```

Expected after successful start:

```text
active
ActiveState=active
SubState=running
one expected polling process
```

## Future Stop / Rollback Command

If unsafe or after a controlled start + stop scenario:

```text
systemctl stop malyarka-telegram-bot.service
```

Then:

```text
systemctl is-active malyarka-telegram-bot.service
```

Expected:

```text
inactive
```

## Strict Command Prohibitions

Do not run without separate approval:

```text
systemctl restart malyarka-telegram-bot.service
systemctl enable malyarka-telegram-bot.service
systemctl disable malyarka-telegram-bot.service
```

Do not read:

```text
.env
config.py
token
os.environ
DB
logs
real orders
```

Do not modify `.py` code or feature flags.

