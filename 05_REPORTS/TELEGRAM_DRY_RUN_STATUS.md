# TELEGRAM_DRY_RUN_STATUS

Generated: 2026-07-28T03:17:06

## Summary

- Aliases: 26
- Scenarios: 18
- Safety limits: 10
- Blocked actions: 18

## Aliases

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
- `/статус`
- `/задача`
- `/память`
- `/малярка`
- `/инженер`
- `/отчёт`
- `/заказ`
- `/споры`
- `/исправить`
- `/экспорт-заблокирован`
- `/аудит`

## Scenarios

- `morning_status` → `/status` — Start the day with local Hermes-Clean status.
- `project_report` → `/report` — Read local report index summary.
- `safety_check` → `/check` — Run local smoke summary.
- `malyarka_check` → `/malyarka` — Check local synthetic Malyarka module state.
- `malyarka_combined_preview` → `/malyarka-combined` — Preview local Malyarka parse, disputes and synthetic pricing.
- `order_clean` → `/order paint | 2 | bucket\nroller | 3 | piece` — Parse a clean synthetic order in dry-run.
- `order_disputed` → `/order paint 2 bucket` — Parse a disputed format in dry-run.
- `disputes_fixtures` → `/disputes` — Show synthetic dispute classification summary.
- `disputes_input` → `/disputes paint 2 bucket` — Classify disputes for a specific input.
- `fix_guidance` → `/fix paint 2 bucket` — Show how to fix a disputed row.
- `export_blocked_info` → `/export-blocked` — Show why export is blocked in dry-run.
- `blocked_actions_list` → `/blocked` — Show all dry-run blocked actions.
- `safety_classify` → `/safety delete` — Classify a deletion action via safety gate.
- `audit_summary` → `/audit` — Show audit log summary.
- `status_ru` → `/статус` — Russian alias for /status.
- `order_ru` → `/заказ краска | 2 | ведро` — Russian alias for /order.
- `disputes_ru` → `/споры` — Russian alias for /disputes.
- `export_blocked_ru` → `/экспорт-заблокирован` — Russian alias for /export-blocked.

## Safety Limits

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

## Blocked Actions — Telegram

- live_polling: Live Telegram polling
- live_webhook: Live Telegram webhook
- send_message: Outbound Telegram messages
- live_bot_start: Live bot start

## Blocked Actions — Secrets

- token_read: Telegram token reading
- env_read: .env file reading
- key_access: API key / token access
- secret_storage: Secret storage in code/docs

## Blocked Actions — Orders

- real_order_read: Real order reading
- real_order_modify: Real order modification
- client_data_access: Client personal data access

## Blocked Actions — Export

- file_export: Real file export (Excel, Corel)
- real_excel_create: Real Excel file creation
- external_send: Sending files externally

## Blocked Actions — External

- external_api: External API call
- google_drive_write: Google Drive write
- google_drive_move: Google Drive move without approval
- archives_access: Old archive reading

## Approval Gate

`APPROVE_TELEGRAM_LIVE` is required before live Telegram polling, webhook, token use or outbound messages.
