# LOCAL RELEASE CHECKLIST (Release Candidate)

Generated: 2026-07-01T22:02:00

## Readiness

- Health: `OK`
- Smoke: `OK` (23 checks, 0 failed)
- Project audit: 25 checks, 0 failed
- Next task: `END_OF_PIPELINE`
- Reports: `111`
- .env files: `0`
- Approval gates: `8`


## Test Report

- Smoke: OK (23 checks)
- Project audit: 25 checks
- CLI commands: 35
- Telegram scenarios: 18
- Malyarka fixtures: 9
- Blocked actions: 18


## Acceptance Criteria

- [health] Health status = OK, 0 .env files
- [smoke] Smoke: 20/20 checks passed
- [tests] All 187+ tests passed
- [audit] Project audit: 25/25 checks, 0 failed
- [safety_gate] safety delete → BLOCKED, safety create_local_report → SAFE
- [secret_gate] Secret gate: 9/10 passed, real API blocked
- [telegram] Telegram dry-run: 18 сценариев, 26 команд, live blocked
- [malyarka] Malyarka: 9 fixtures, export gated, synthetic only
- [subsystems] 6 enabled, 6 disabled — все gate защищены
- [docs] USER_RUNBOOK_RU.md, SAFE_LOCAL_OPERATIONS_RU.md, START_HERE.md

## Enabled Subsystems

| Subsystem | Status | Mode | Gate |
|-----------|--------|------|------|
| `local_cli` | ENABLED | local | none |
| `dashboard` | ENABLED | local markdown | none |
| `smoke_tests` | ENABLED | local | none |
| `telegram_dry_run` | ENABLED | dry-run | none |
| `malyarka_synthetic` | ENABLED | synthetic/manual test | none |
| `mock_ai_provider` | ENABLED | mock | none |

## Disabled Subsystem Matrix

| Subsystem | Status | Mode | Gate |
|-----------|--------|------|------|
| `live_telegram` | DISABLED | live external | `APPROVE_TELEGRAM_LIVE` |
| `real_ai_providers` | DISABLED | external API | `APPROVE_SECRET_SETUP` |
| `google_drive_write` | DISABLED | external write | `APPROVE_GOOGLE_DRIVE_MOVE` |
| `real_order_access` | DISABLED | customer data | `APPROVE_REAL_ORDER_ACCESS` |
| `archive_import` | DISABLED | old archive import | `APPROVE_ARCHIVE_UNPACK` |
| `delete_files` | DISABLED | destructive | `APPROVE_DELETE` |

## Known Limitations

- Gemini API выключен — требуется APPROVE_SECRET_SETUP и ключ
- DeepSeek / DeepSig API выключен — требуется APPROVE_SECRET_SETUP
- Telegram — только dry-run, live polling/webhook заблокированы
- Malyarka — только synthetic/manual input, реальные заказы заблокированы
- Google Drive — write заблокирован (ошибка 403 appNotAuthorizedToFile)
- Экспорт файлов — заблокирован в dry-run режиме
- Удаление файлов — заблокировано глобально
- Архивы — не распакованы, импорт заблокирован
- Secret gate — 1 проверка не пройдена (no_key_in_memory), реальный API не готов
- Нет CI/CD — все проверки запускаются вручную

## All Local Commands

- `status` — Show local Hermes-Clean status; mode: `local/read-only`; approval: `no`
- `start-summary` — Daily local startup summary; mode: `local/read-only`; approval: `no`
- `health` — Check required local files and .env presence; mode: `local/read-only`; approval: `no`
- `app-status` — Write local app runtime status; mode: `local/read-only`; approval: `no`
- `dashboard` — Write local Hermes-Clean dashboard; mode: `local/read-only`; approval: `no`
- `daily-report` — Write local daily project report; mode: `local/read-only`; approval: `no`
- `project-audit` — Audit local structure, safety, docs coverage; mode: `local/read-only`; approval: `no`
- `refresh-all` — Refresh all local Hermes-Clean summary reports; mode: `local`; approval: `no`
- `export-status` — Export status to markdown; mode: `local/read-only`; approval: `no`
- `release-checklist` — Write release checklist; mode: `local/read-only`; approval: `no`
- `reports` — List local reports from 05_REPORTS; mode: `local/read-only`; approval: `no`
- `tasks` — Show local task snapshot; mode: `local/read-only`; approval: `no`
- `memory` — Show trusted local memory snapshot; mode: `local/read-only`; approval: `no`
- `help-local` — Show all local commands and approval gates; mode: `local/read-only`; approval: `no`
- `message` — Simulate Telegram incoming message; mode: `dry-run`; approval: `no live send`
- `telegram-scenarios` — Run Telegram dry-run usage scenarios; mode: `dry-run`; approval: `no live send`
- `telegram-status` — Write Telegram dry-run status report; mode: `dry-run`; approval: `no live send`
- `telegram-flow` — Run local Malyarka Telegram dialog flow; mode: `dry-run`; approval: `no live send; no real orders`
- `malyarka-preview` — Preview Malyarka parsing contract; mode: `dry-run`; approval: `no real orders`
- `malyarka-dialog` — Run operator-style local Malyarka dialog commands; mode: `dry-run`; approval: `no real orders; no live Telegram`
- `malyarka-transcript` — Write local Malyarka dialog transcript report; mode: `local/dry-run`; approval: `no real orders; report only`
- `malyarka-fixtures` — Run synthetic Malyarka fixture scenarios; mode: `local/synthetic`; approval: `no real orders`
- `malyarka-disputes` — Classify synthetic Malyarka disputed rows; mode: `local/synthetic`; approval: `no real orders`
- `malyarka-combined` — Show parse, disputes and pricing together; mode: `local/synthetic`; approval: `no real orders`
- `malyarka-schema` — Show Malyarka export schema; mode: `local/synthetic`; approval: `no real orders`
- `malyarka-demo` — Show Malyarka module demo summary; mode: `local/synthetic`; approval: `no real orders`
- `malyarka-pricing` — Show synthetic Malyarka pricing; mode: `local/synthetic`; approval: `no real orders`
- `malyarka-resolve` — Dry-run disputed row replacement; mode: `dry-run`; approval: `no real orders`
- `malyarka-workflow` — Show synthetic Malyarka workflow; mode: `local/synthetic`; approval: `no real orders`
- `malyarka-status` — Write Malyarka module status report; mode: `local/synthetic`; approval: `no real orders`
- `ai-provider` — Select mock or disabled AI provider; mode: `dry-run/gated`; approval: `APPROVE_SECRET_SETUP`
- `review-provider` — Select mock or disabled review provider; mode: `dry-run/gated`; approval: `APPROVE_SECRET_SETUP`
- `safety` — Classify a requested action via safety gate; mode: `local/read-only`; approval: `no`
- `safety-audit` — Show local safety audit log; mode: `local/read-only`; approval: `no`
- `smoke` — Run local Hermes-Clean smoke checks; mode: `local/read-only`; approval: `no`

## Open Approval Gates

- `APPROVE_GOOGLE_DRIVE_MOVE`
- `APPROVE_GOOGLE_DRIVE_REAUTH`
- `APPROVE_SECRET_SETUP`
- `APPROVE_TELEGRAM_LIVE`
- `APPROVE_REAL_ORDER_ACCESS`
- `APPROVE_MALYARKA_ARCHIVE_IMPORT`
- `APPROVE_DELETE`
- `APPROVE_ARCHIVE_UNPACK`

## Next Direction Options

- BATCH_063B: План переноса Malyarka hardening из E:\«Гермес Клин» в Desktop
- Подключить Gemini API после APPROVE_SECRET_SETUP
- Подключить DeepSeek / DeepSig review после APPROVE_SECRET_SETUP
- Запустить live Telegram после APPROVE_TELEGRAM_LIVE
- Продолжить Malyarka module contracts без реальных заказов
- Вернуться к Google Drive cleanup после решения 403 ошибки
- Подготовить Hermes-Clean локальную сборку (pyproject.toml, requirements.txt)

## Safety

This checklist is local to Hermes-Clean. It does not read Google Drive, old archives, secrets, real orders or old projects.
