# LOCAL DASHBOARD

Generated: 2026-07-28T02:14:51

## Core

- Health: `OK`
- Smoke: `ATTENTION`
- Active batch: `BATCH_091B_PROJECT_MEMORY_AND_CONTEXT_CONTROL_LAYER`
- Next task: `missing`
- Done count: `455`
- Reports count: `175`
- .env files: `0`


## Smoke Top-10

- start-summary: OK
- health: OK
- reports: OK
- tasks: FAIL
- memory: OK
- app-status: OK
- project-audit: FAIL
- help-local: OK
- message: OK
- telegram-flow: OK

## Task Queue

- Active batch: `BATCH_091B_PROJECT_MEMORY_AND_CONTEXT_CONTROL_LAYER`
- Next task: `missing`
- Done count: `455`
- Blocked count: `2`
- Last done: `- Результат сохранён в `05_REPORTS\GOOGLE_DRIVE_REBUILD_RESULT_2026-07-24.json`.`


## Pending Approvals

# PENDING_APPROVALS ## Google Drive - Google Drive LOW move pending. - Требуется либо ручной перенос, либо переподключение Codex с нужными правами.

## Runtime Status

- App mode: `local-safe`
- Can start live services: `False`
- Can read secrets: `False`
- Can touch real orders: `False`
- Can change Google Drive: `False`

### Enabled

- `local_cli`: ENABLED; mode=local
- `dashboard`: ENABLED; mode=local markdown
- `smoke_tests`: ENABLED; mode=local
- `telegram_dry_run`: ENABLED; mode=dry-run
- `malyarka_synthetic`: ENABLED; mode=synthetic/manual test
- `mock_ai_provider`: ENABLED; mode=mock

### Disabled

- `live_telegram`: DISABLED; gate=APPROVE_TELEGRAM_LIVE
- `real_ai_providers`: DISABLED; gate=APPROVE_SECRET_SETUP
- `google_drive_write`: DISABLED; gate=APPROVE_GOOGLE_DRIVE_MOVE
- `real_order_access`: DISABLED; gate=APPROVE_REAL_ORDER_ACCESS
- `archive_import`: DISABLED; gate=APPROVE_ARCHIVE_UNPACK
- `delete_files`: DISABLED; gate=APPROVE_DELETE

## Malyarka Readiness

- Fixtures: `12` total, `4` ready
- Demo fixtures: `12`
- Ready fixtures: `4`
- Disputed fixtures: `8`
- Workflow status: `READY_FOR_USER_REVIEW`
- Export gated: `True`
- Real export blocked: `BLOCKED: export requires explicit user approval.`
- **Malyarka readiness: `NOT READY`**


## Telegram Dry-Run Readiness

- Aliases: `26`
- Scenarios: `18`
- Safety limits: `10`
- Blocked actions: `18`
- **Telegram readiness: `DRY-RUN ONLY`** (live blocked)


### Telegram Commands (first 15)

- `/status`
- `/task`
- `/memory`
- `/malyarka`
- `/malyarka-combined`
- `/engineer`
- `/report`
- `/check`
- `/order`
- `/disputes`
- `/fix`
- `/export-blocked`
- `/audit`
- `/safety`
- `/blocked`

### Telegram Scenarios (first 10)

- `morning_status` → `/status`
- `project_report` → `/report`
- `safety_check` → `/check`
- `malyarka_check` → `/malyarka`
- `malyarka_combined_preview` → `/malyarka-combined`
- `order_clean` → `/order paint | 2 | bucket\nroller | 3 | piece`
- `order_disputed` → `/order paint 2 bucket`
- `disputes_fixtures` → `/disputes`
- `disputes_input` → `/disputes paint 2 bucket`
- `fix_guidance` → `/fix paint 2 bucket`

## Blocked Actions

- export: 3 blocked
- external: 4 blocked
- orders: 3 blocked
- secrets: 4 blocked
- telegram: 4 blocked

## Command Center (first 15)

- `scripts\hermes.cmd status` — Show local Hermes-Clean status (local/read-only)
- `scripts\hermes.cmd start-summary` — Daily local startup summary (local/read-only)
- `scripts\hermes.cmd health` — Check required local files and .env presence (local/read-only)
- `scripts\hermes.cmd app-status` — Write local app runtime status (local/read-only)
- `scripts\hermes.cmd dashboard` — Write local Hermes-Clean dashboard (local/read-only)
- `scripts\hermes.cmd daily-report` — Write local daily project report (local/read-only)
- `scripts\hermes.cmd project-audit` — Audit local structure, safety, docs coverage (local/read-only)
- `scripts\hermes.cmd refresh-all` — Refresh all local Hermes-Clean summary reports (local)
- `scripts\hermes.cmd export-status` — Export status to markdown (local/read-only)
- `scripts\hermes.cmd release-checklist` — Write release checklist (local/read-only)
- `scripts\hermes.cmd reports` — List local reports from 05_REPORTS (local/read-only)
- `scripts\hermes.cmd tasks` — Show local task snapshot (local/read-only)
- `scripts\hermes.cmd memory` — Show trusted local memory snapshot (local/read-only)
- `scripts\hermes.cmd help-local` — Show all local commands and approval gates (local/read-only)
- `scripts\hermes.cmd message` — Simulate Telegram incoming message (dry-run)

## Safety Locks

- live polling disabled
- webhook disabled
- token reading disabled
- message sending disabled
- real order access disabled
- .env reading disabled
- API key access disabled
- file export disabled
- Google Drive write disabled
- archive reading disabled

## Safety

This dashboard is local. It does not read secrets, start live Telegram, change Google Drive, read real orders or unpack old archives.
