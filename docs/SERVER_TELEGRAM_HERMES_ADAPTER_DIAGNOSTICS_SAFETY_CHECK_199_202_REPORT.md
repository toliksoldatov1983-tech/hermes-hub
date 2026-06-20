# Series 199-202 — Diagnostics safety check report

Technical name: `BATCH_SERIES_199_202_HERMES_ADAPTER_DIAGNOSTICS_SAFETY_CHECK`

## Result

Local focused tests were added for diagnostics safety in the fake adapter contract.

Created:

```text
E:\Hermes-Hub\local_tests\hermes_adapter_fake\test_fake_adapter_diagnostics_safety.py
E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_DIAGNOSTICS_SAFETY_CHECK_199_202_REPORT.md
E:\Hermes-Hub\docs\SERVER_TELEGRAM_HERMES_ADAPTER_DIAGNOSTICS_SAFETY_CHECK_199_202_SUMMARY.md
```

Changed:

```text
E:\Hermes-Hub\local_tests\hermes_adapter_fake\fake_adapter.py
```

Reason for change: the new diagnostics safety tests found that server path and live log path markers were not blocked. The local fake adapter sensitive marker list was extended with:

```text
/opt/malyarka-telegram-bot
/var/log
live.log
```

No live bot code was changed.

## Diagnostics safety checks implemented

The new tests verify:

1. diagnostics does not reveal token values;
2. diagnostics does not reveal `.env`;
3. diagnostics does not reveal `config.py`;
4. diagnostics does not reveal `os.environ` or environment values;
5. diagnostics does not reveal server paths;
6. diagnostics does not reveal database paths;
7. diagnostics does not reveal live logs paths;
8. diagnostics does not reveal polling/webhook identifiers;
9. unsafe diagnostics is blocked;
10. diagnostics without adapter flag is blocked by default;
11. diagnostics response preserves `side_effects == []`;
12. diagnostics response preserves `dry_run`;
13. diagnostics does not make network/API calls;
14. diagnostics does not import live bot modules.

## Local test command

```text
cd /d E:\Hermes-Hub && python -m pytest local_tests\hermes_adapter_fake -q
```

PowerShell equivalent used:

```text
Set-Location E:\Hermes-Hub; python -m pytest local_tests\hermes_adapter_fake -q
```

First run:

```text
2 failed, 112 passed
```

Reason: server path and live log path diagnostics were not blocked.

After the local marker fix:

```text
114 passed in 0.12s
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

Series 203-206 — local rollback/no-side-effects contract check for fake adapter, without server/live Telegram and without changing the existing bot.
