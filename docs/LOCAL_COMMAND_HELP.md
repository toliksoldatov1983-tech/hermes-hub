# LOCAL_COMMAND_HELP

Use this command from `C:\Users\user\Desktop\Hermes-Clean`:

```cmd
scripts\hermes.cmd help-local
```

## Local commands

- `start-summary` — daily local startup summary.
- `health` — local required-path and `.env` presence check.
- `reports` — local report index from `05_REPORTS`.
- `tasks` — local task status snapshot.
- `memory` — trusted local memory snapshot.
- `message` — Telegram message simulation, dry-run only.
- `malyarka-preview` — Malyarka parser preview, dry-run only.
- `ai-provider` — mock/disabled AI provider selector.
- `review-provider` — mock/disabled review provider selector.
- `safety` — local safety classification.

## Approval gates

- `APPROVE_GOOGLE_DRIVE_MOVE`
- `APPROVE_GOOGLE_DRIVE_REAUTH`
- `APPROVE_SECRET_SETUP`
- `APPROVE_TELEGRAM_LIVE`
- `APPROVE_REAL_ORDER_ACCESS`
- `APPROVE_MALYARKA_ARCHIVE_IMPORT`
- `APPROVE_DELETE`
- `APPROVE_ARCHIVE_UNPACK`

No command in this file changes Google Drive, reads secrets, starts live Telegram, touches real orders or unpacks old archives.
