# Series 187-190 — Hermes adapter fake adapter implementation report

Technical name: `BATCH_SERIES_187_190_HERMES_ADAPTER_FAKE_ADAPTER_TEST_DOUBLE_IMPLEMENTATION`

## Result

Local fake adapter / local test double has been implemented only inside:

```text
E:\Hermes-Hub\local_tests\hermes_adapter_fake
```

Created files:

```text
E:\Hermes-Hub\local_tests\hermes_adapter_fake\fake_adapter.py
E:\Hermes-Hub\local_tests\hermes_adapter_fake\test_fake_adapter_contract.py
```

The fake adapter accepts a plain `dict` request and returns a plain `dict` response. It is not a live Hermes adapter and is not connected to Telegram.

## Implemented scenarios

- safe allowed action;
- forbidden action;
- unknown action;
- empty output validation;
- missing required fields;
- wrong field types;
- unsafe diagnostics;
- `fallback_required=true`;
- adapter off by default;
- feature flags blocking export/admin/write actions.

## Checked outputs

- valid output;
- blocked output;
- unsafe output;
- malformed output;
- fallback output.

## Contract rules fixed by tests

- `side_effects` is always `[]`;
- adapter is off by default;
- `dry_run` is preserved in the response;
- write/admin/export actions are blocked when unsafe or forbidden;
- malformed input returns a controlled fallback instead of crashing;
- `fallback_required=true` returns fallback output;
- unsafe diagnostics are blocked as unsafe output.

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
33 passed in 0.06s
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

The fake adapter does not import live bot modules, `aiogram`, Telegram API clients, network clients, or subprocess.

## Next safe step

Series 191-194 — local contract boundary check between fake adapter and dry-run contract schema, without server/live Telegram and without changing the existing bot.
