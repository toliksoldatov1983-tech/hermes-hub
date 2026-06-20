# HERMES_ADAPTER_PHASE2_ROLLBACK_PLAN

Дата: 2026-06-20

## Required rollback rule

After any future Phase 2 dry-run, the Hermes adapter feature flag must return to OFF.

```text
_HERMES_ADAPTER_ENABLED = False
```

## Rollback triggers

Rollback immediately if:

- the bot response is incorrect;
- the adapter blocks normal safe behavior unexpectedly;
- Telegram behavior becomes unstable;
- service becomes unstable;
- diagnostics are unsafe;
- any secret/DB/log/order access is required;
- production risk appears.

## Service instability rule

If service is unstable, stop the Phase 2 path and wait for a separate user decision.

Do not improvise production changes.

## Always forbidden

- production enable;
- autostart enable;
- reading `.env`, `config.py`, token, `os.environ`;
- reading DB/live logs/real orders;
- changing prices/materials/rules;
- Vision/API;
- git/commit/push.

## Final rollback report must confirm

```text
feature flag: OFF
production: OFF
service state: recorded
no secrets read
no DB/log/order contents read
```

