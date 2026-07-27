# DAILY LOCAL REPORT

Generated: 2026-07-28T02:14:48

## Today Status

- Health: `OK`
- Smoke: `ATTENTION`
- Active batch: `BATCH_091B_PROJECT_MEMORY_AND_CONTEXT_CONTROL_LAYER`
- Next task: `missing`
- Done count: `455`
- Reports count: `175`
- .env files: `0`

## Smoke Checks

- start-summary: OK — missing
- health: OK — env_files_found=0
- reports: OK — reports_count=175
- tasks: FAIL — missing
- memory: OK — documents=6
- app-status: OK — enabled=6; disabled=6
- project-audit: FAIL — checks=25; failed=2
- help-local: OK — commands=62
- message: OK — Open NEXT_TASK.md or choose the next safe local block.
- telegram-flow: OK — resolved=2; export_ready=True
- malyarka-preview: OK — export_blocked=True
- malyarka-dialog: OK — commands=4; export_ready=True
- malyarka-transcript: OK — path=MALYARKA_DIALOG_TRANSCRIPT_SMOKE.md; export_ready=True
- malyarka-fixtures: OK — fixtures=12
- malyarka-schema: OK — columns=10
- malyarka-pricing: OK — total=200.0
- malyarka-disputes: OK — disputes=8; categories=4
- malyarka-combined: OK — confirmed=2; disputed=1
- malyarka-demo: OK — fixtures=12
- ai-provider: OK — Gemini is disabled until APPROVE_SECRET_SETUP.
- review-provider: OK — DeepSeek review is disabled until APPROVE_SECRET_SETUP.
- safety: OK — Action is blocked by Hermes-Clean policy.
- ai-provider-registry: FAIL — providers=8; mock=True; gemini=True
- ai-provider-router-mock: OK — provider=mock; blocked=False
- ai-provider-router-unknown: OK — blocked=True; reason=Unknown provider: nonexistent. Use 'ai-
- ai-provider-gemini-disabled: OK — blocked=True; reason=Gemini is disabled until APPROVE_SECRET

## Task Queue

- Active batch: `BATCH_091B_PROJECT_MEMORY_AND_CONTEXT_CONTROL_LAYER`
- Next task: `missing`
- Done count: `455`
- Blocked count: `2`
- Last done: `- Результат сохранён в `05_REPORTS\GOOGLE_DRIVE_REBUILD_RESULT_2026-07-24.json`.`


## Runtime

- App mode: `local-safe`
- Enabled: `6`
- Disabled: `6`
- Can read secrets: `False`
- Can start live services: `False`
- Can touch real orders: `False`
- Can change Google Drive: `False`

## Disabled Subsystems

- `live_telegram`: DISABLED; gate=APPROVE_TELEGRAM_LIVE
- `real_ai_providers`: DISABLED; gate=APPROVE_SECRET_SETUP
- `google_drive_write`: DISABLED; gate=APPROVE_GOOGLE_DRIVE_MOVE
- `real_order_access`: DISABLED; gate=APPROVE_REAL_ORDER_ACCESS
- `archive_import`: DISABLED; gate=APPROVE_ARCHIVE_UNPACK
- `delete_files`: DISABLED; gate=APPROVE_DELETE

## Malyarka Readiness

- Confirmed: `2`
- Disputed: `1`
- Pricing total: `245.0`
- Can write file: `False`
- Can use as real order: `False`
- Demo fixtures: `12`
- Export gated: `True`
- **Malyarka readiness: `DRY-RUN`**


## Telegram Dry-Run

Scenarios: `18`

- `morning_status` → `/status`
- `project_report` → `/report`
- `safety_check` → `/check`
- `malyarka_check` → `/malyarka`
- `malyarka_combined_preview` → `/malyarka-combined`
- `order_clean` → `/order paint | 2 | bucket\nroller | 3 | piece`
- `order_disputed` → `/order paint 2 bucket`
- `disputes_fixtures` → `/disputes`

## Blocked Actions

- export: 3
- external: 4
- orders: 3
- secrets: 4
- telegram: 4

## Safe Commands

- `scripts\hermes.cmd start-summary`
- `scripts\hermes.cmd status`
- `scripts\hermes.cmd health`
- `scripts\hermes.cmd reports`
- `scripts\hermes.cmd tasks`
- `scripts\hermes.cmd memory`
- `scripts\hermes.cmd dashboard`
- `scripts\hermes.cmd daily-report`
- `scripts\hermes.cmd project-audit`
- `scripts\hermes.cmd refresh-all`
- `scripts\hermes.cmd app-status`
- `scripts\hermes.cmd smoke`
- `scripts\hermes.cmd safety delete`
- `scripts\hermes.cmd safety-audit`
- `scripts\hermes.cmd telegram-scenarios`
- `scripts\hermes.cmd telegram-status`
- `scripts\hermes.cmd malyarka-demo`
- `scripts\hermes.cmd malyarka-fixtures`
- `scripts\hermes.cmd malyarka-combined`
- `scripts\run_tests.cmd`

## Pending Approvals

# PENDING_APPROVALS ## Google Drive - Google Drive LOW move pending. - Требуется либо ручной перенос, либо переподключение Codex с нужными правами.

## Safety

This report is local to Hermes-Clean. It does not read secrets, `.env`, Google Drive, real orders, client documents, old archives or live Telegram.
