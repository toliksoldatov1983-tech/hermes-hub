# Server Bot Controlled Start Rollback Plan

Date: 2026-06-20

Mode: markdown-only rollback plan.

Status: `PLAN_ONLY`

## Purpose

Define rollback for a future approved controlled start of:

```text
malyarka-telegram-bot.service
```

## Fast Stop

If future controlled start is unsafe:

```text
systemctl stop malyarka-telegram-bot.service
```

Then confirm:

```text
systemctl is-active malyarka-telegram-bot.service
```

Expected:

```text
inactive
```

## Feature Flag

Feature flag must stay OFF.

Expected:

```text
_HERMES_ADAPTER_ENABLED = False
```

If a future approved operation ever changes it, rollback must return it to OFF before any further action.

Changing the flag is not authorized by this plan.

## Do Not Touch During Rollback

Do not read or modify:

- `.env`;
- `config.py`;
- token;
- `os.environ`;
- databases;
- logs;
- real orders;
- production data;
- `.py` files, unless a separate rollback patch is explicitly approved.

## Failure Report

If rollback is needed, report:

- why rollback was needed;
- whether stop command succeeded;
- final service state;
- final feature flag state if safely confirmed;
- whether secrets remained untouched;
- whether DB/log/orders remained untouched;
- whether bot sent/received only safe test messages.

## Rollback Success Criteria

Rollback is successful if:

- service is inactive;
- no autostart was enabled;
- feature flag remains OFF or was not changed;
- no secrets were read;
- no production actions occurred;
- result is documented.

