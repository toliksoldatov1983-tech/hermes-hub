# Series 195-198 — Feature flags gate check report

Technical name: `BATCH_SERIES_195_198_HERMES_ADAPTER_FEATURE_FLAGS_GATE_CHECK`

## Result

Local focused tests were added for the fake adapter feature flags gate.

Created:

```text
E:\Hermes-Hub\local_tests\hermes_adapter_fake\test_fake_adapter_feature_flags_gate.py
E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_FEATURE_FLAGS_GATE_CHECK_195_198_REPORT.md
E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_FEATURE_FLAGS_GATE_CHECK_195_198_SUMMARY.md
```

`fake_adapter.py` was not changed. The existing implementation already satisfied the feature flags gate checks.

## Feature flags checks implemented

The new tests verify:

1. adapter is disabled by default;
2. safe read/dry-run actions are allowed only when `HERMES_ADAPTER_ENABLED=true`;
3. export actions are blocked when export callbacks are disabled;
4. admin actions are blocked when admin changes are disabled;
5. write actions are blocked when write/admin/export flags are disabled;
6. diagnostics are safe-only and unsafe diagnostics are blocked;
7. unknown action is blocked regardless of flags;
8. forbidden action is blocked regardless of flags;
9. `fallback_required=true` does not bypass feature flags;
10. `side_effects` is always `[]`;
11. response contains no token/env/config/server/db/polling markers.

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
99 passed in 0.12s
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

Series 199-202 — local diagnostics safety check for fake adapter contract, without server/live Telegram and without changing the existing bot.
