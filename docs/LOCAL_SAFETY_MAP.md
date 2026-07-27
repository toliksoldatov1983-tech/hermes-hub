# LOCAL_SAFETY_MAP

## Source Of Truth

The current source of truth is:

```text
C:\Users\user\Desktop\Hermes-Clean
```

Old archives, old folders, old Drive docs, Obsidian memory and Open WebUI memory are archive sources only. They are not current project truth.

## Safe Local Layers

| Layer | Role | External Access |
|---|---|---|
| Safety Gate | classify actions | none |
| Secret Guard | block and redact secrets | none |
| Memory Sync | record decisions and prohibitions | none |
| Malyarka dry-run | test synthetic dialog flow | none |
| Transcript reports | write local markdown reports | none |
| Mock AI providers | simulate provider responses | none |

## Blocked Without Separate Approval

- real `.env` reading;
- real tokens;
- real API keys;
- live Telegram;
- real orders;
- Google Drive writes;
- old project changes;
- archive unpacking as a working project;
- delete operations.

## Pending Approval Gates

```text
APPROVE_GOOGLE_DRIVE_MOVE
APPROVE_GOOGLE_DRIVE_REAUTH
APPROVE_SECRET_SETUP
APPROVE_TELEGRAM_LIVE
APPROVE_REAL_ORDER_ACCESS
APPROVE_MALYARKA_ARCHIVE_IMPORT
APPROVE_DELETE
APPROVE_ARCHIVE_UNPACK
```

## Current Practical Rule

If a task can be completed by writing local code, docs, tests or reports inside Hermes-Clean, it is safe.

If a task needs real secrets, real Telegram, real orders, Google Drive writes, deletes or old archive imports, it must stop at the matching approval gate.
