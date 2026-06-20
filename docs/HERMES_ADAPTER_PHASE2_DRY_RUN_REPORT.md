# HERMES_ADAPTER_PHASE2_DRY_RUN_REPORT

Дата: 2026-06-20

Итоговый статус:

```text
PHASE2_DRY_RUN_FAILED_ROLLBACK_DONE
```

## Approval

Phase 2 dry-run was explicitly approved by the user with:

```text
APPROVE_HERMES_ADAPTER_PHASE2_DRY_RUN_ONCE
```

## Precheck result

Precheck passed before enabling the flag:

```text
SSH: verified
service: active/running
autostart: disabled
feature flag before: OFF
adapter file: present
telegram hook: present
production: OFF
```

## Backup

Backup was created before changing the flag:

```text
/opt/malyarka-telegram-bot/malyarka_core/adapters/telegram.py.phase2_dry_run_backup_20260620
```

## Dry-run activation

Changed one allowed line:

```text
_HERMES_ADAPTER_ENABLED = False
```

to:

```text
_HERMES_ADAPTER_ENABLED = True
```

Controlled restart was performed to apply the temporary flag.

After restart:

```text
service: active/running
autostart: disabled
```

## Telegram test result

User performed safe Telegram test.

Result:

```text
/start -> bot answered with menu
700 x 500 -> wrong behavior
```

Observed wrong behavior:

```text
What is 700 x 500 for?
1. Image dimensions
2. Canvas size
3. Window size
4. Other
```

Interpretation:

```text
Hermes adapter interfered incorrectly with expected Malyarka order flow.
```

User confirmed no photos, files, real orders, Vision/API, personal data, or production commands were sent.

## Rollback

Rollback was executed immediately after failed Telegram test.

The feature flag was returned to:

```text
_HERMES_ADAPTER_ENABLED = False
```

Controlled restart was performed to apply rollback.

Final verified state:

```text
service: active/running
autostart: disabled
feature flag: OFF
production: OFF
process: /opt/malyarka-telegram-bot/.venv/bin/python -m malyarka_telegram.app --run-polling
```

## No-touch confirmation

Not performed:

- production enable;
- systemctl enable;
- systemctl stop;
- autostart change;
- `.env` read;
- `config.py` read;
- token read;
- `os.environ` read;
- database read;
- live log read;
- real order read;
- `.py` code changes beyond the one approved feature flag line and rollback;
- adapter logic changes;
- git/commit/push;
- launcher scripts;
- HERMES_PACKET_INBOX.

## Blocker

Phase 2 cannot proceed as-is.

Blocker:

```text
Adapter incorrectly diverts simple order-like input `700 x 500` into generic English clarification flow.
```

## Next safe step

Prepare a plan-only investigation of the Hermes adapter dry-run behavior using local/read-only documents first.

Do not re-enable the flag until a corrected plan is approved separately.

