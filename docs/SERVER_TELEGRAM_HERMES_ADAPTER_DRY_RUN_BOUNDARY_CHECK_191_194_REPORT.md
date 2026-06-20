# Series 191-194 — Dry-run contract boundary check report

Technical name: `BATCH_SERIES_191_194_HERMES_ADAPTER_DRY_RUN_CONTRACT_BOUNDARY_CHECK`

## Result

Local focused boundary tests were added for the fake adapter response contract.

Created:

```text
E:\Hermes-Hub\local_tests\hermes_adapter_fake\test_fake_adapter_dry_run_boundary.py
E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_DRY_RUN_BOUNDARY_CHECK_191_194_REPORT.md
E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_DRY_RUN_BOUNDARY_CHECK_191_194_SUMMARY.md
```

`fake_adapter.py` was not changed. The existing implementation already satisfied the boundary checks.

## Boundary checks implemented

The new tests verify:

1. fake adapter response contains all required dry-run boundary fields;
2. `dry_run=true` is preserved in response;
3. `side_effects` is always `[]`;
4. blocked output is compatible with the dry-run contract;
5. fallback output is compatible with the dry-run contract;
6. malformed output returns controlled fallback;
7. unsafe diagnostics do not leak token/env/config/server paths;
8. export/admin/write actions remain blocked with disabled feature flags;
9. adapter off by default remains blocked;
10. response does not contain live Telegram identifiers, token values, env values, server paths, database paths, or polling/restart commands.

## Boundary fields

```text
ok
status
action
dry_run
blocked
fallback_required
reason
diagnostics_safe
side_effects
output_type
```

## Local test command

```text
cd /d E:\Hermes-Hub && python -m pytest local_tests\hermes_adapter_fake -q
```

PowerShell equivalent used:

```text
Set-Location E:\Hermes-Hub; python -m pytest local_tests\hermes_adapter_fake -q
```

Result:

```text
66 passed in 0.09s
```

## Safety boundary

Not touched:

- server;
- live Telegram bot;
- polling/webhook;
- token;
- `.env`;
- `config.py`;
- environment variables;
- databases;
- live logs;
- `.git`;
- real orders;
- Corel;
- ArtCAM;
- CNC;
- Vision/API;
- commit/push;
- existing bot code;
- staging bot code;
- production handlers/router/app;
- `/opt/malyarka-telegram-bot`.

No live bot modules, `aiogram`, Telegram API clients, server files, collectors, polling, webhook, network/API calls, databases, or real orders were used.

## Next safe step

Series 195-198 — local feature flags gate check for fake adapter contract, without server/live Telegram and without changing the existing bot.
