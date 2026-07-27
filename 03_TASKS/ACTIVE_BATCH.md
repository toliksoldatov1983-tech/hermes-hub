# Active Batch

BATCH_091B_PROJECT_MEMORY_AND_CONTEXT_CONTROL_LAYER

Status: completed locally by Codex.

Summary:
- Created local memory/context-control layer in `00_MEMORY`.
- Added minimal context policy for new Hermes/Codex chats.
- Added do-not-autoload policy for reports, source, tests, old projects, archives, Google Drive and real orders.
- Added clean start prompts for Hermes and Codex.
- Preserved next large task as `BATCH_092_MACRO_AI_PROVIDER_INTEGRATION_AND_DAILY_ASSISTANT_MODE`.

Report:
- `05_REPORTS\BATCH_091B_PROJECT_MEMORY_AND_CONTEXT_CONTROL_LAYER_REPORT.md`

Safety:
- No `.env` reading.
- No token or key reading.
- No external APIs.
- No live Telegram.
- No polling/webhook.
- No real orders.
- No Google Drive changes.
- No old project scanning.
- No archive changes.
- No delete operations.
- No Malyarka logic changes.

---

BATCH_096_TELEGRAM_ROUTES_CLEANUP

Status: local fixed by Codex; pending confirmed live gateway restart and owner-only Telegram test.

Summary:
- Created backup before route cleanup.
- Found active gateway-like process chain for `hermes gateway run`.
- Fixed Malyarka Telegram routing so Hermes-Clean direct intents run before free chat and generic fallback.
- Added status, next-step, correction, price draft, LKM draft and backup direct intents.
- Moved hard safety gate before free chat/general fallback in handler path.
- Preserved legacy fallbacks; no files deleted.

Report:
- `05_REPORTS\TELEGRAM_ROUTE_MAP_BEFORE_CLEANUP.md`
- `05_REPORTS\TELEGRAM_ROUTES_CLEANUP_REPORT.md`

Safety:
- No `.env` reading.
- No token or key reading.
- No Google Drive changes.
- No Vision enablement.
- No production database.
- No git push.
- No E:\РАБОТА changes.
- No CorelDRAW / ArtCAM / CNC launch.
- No `bot_archive_20260703.py` changes.
- No reset / clear / prune / delete.

Next:
- Confirm gateway entrypoint/cwd without secrets.
- Restart only the confirmed Telegram polling/gateway process.
- Run owner-only live Telegram tests.

---

BATCH_097_TELEGRAM_SERVER_24_7_STATUS

Status: completed; server gateway running 24/7 and owner phone live-test passed.

Summary:
- Confirmed SSH alias `hermes-server` works.
- Confirmed `hermes-gateway.service` is `active` and `enabled`.
- Confirmed `Restart=always` and `Linger=yes`, so the gateway is configured for 24/7 server operation independent of the local PC.
- Confirmed only one visible server gateway/polling process in process list.
- Observed Telegram polling conflicts until `2026-07-04 08:20:11 UTC`; no newer conflict lines in checked logs.
- Owner phone `/status` reached the gateway at `2026-07-04 08:29:42 UTC`.
- Gateway rejected the Telegram user as unauthorized and showed a pairing code in Telegram.
- User explicitly approved pairing code `5MUQKKUT`.
- Server approved Telegram user `784990082` (`Soldatov Anatoliy`).
- Repeat `/status` from phone returned `Hermes Gateway Status`.
- Server gateway remained `active` and `enabled`.

Report:
- `05_REPORTS\TELEGRAM_SERVER_24_7_STATUS_2026-07-04.md`

Safety:
- No `.env` reading.
- No token or key reading.
- No live bot restart.
- No second polling.
- No real orders.
- No Google Drive changes.
- No deletes.

Next:
- Return to real-order waiting flow.
- Keep real export and real orders behind separate approval gates.

---

## MALYARKA_DRIVE_DOCUMENTS_LOCAL_IMPORT

Status: COMPLETED_LOCAL · DRIVE_UNCHANGED · DIRECT_COMPARE_BLOCKED
Date: 2026-07-24

Completed:
- read 17 DOCX from the local Google Drive export;
- created one active document index;
- added five normalized working templates;
- added three reference orders and reference-order rules;
- added synthetic UCH-002/UCH-003 fixtures and tests;
- added confirmed worker rates for modern and selection;
- marked historic prices and obsolete Space Agent settings as non-authoritative.

Checks:
- required files: 8/8;
- index links: 8, missing 0;
- targeted tests: 10 passed;
- full tests: 810 passed, 13 old path/CLI/environment failures.

Safety:
- Google Drive unchanged;
- no delete operations;
- no token or `.env` reading;
- no live gateway changes;
- no real export.

Next:
- restore read-only Drive access and compare before any deletion.
