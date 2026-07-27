# LOCAL_RUNTIME_STATUS

- project_root: `C:\Users\user\Desktop\Hermes-Clean`
- app_mode: `local-safe`
- source_of_truth: `Hermes-Clean`
- next_task: `BATCH_092_MACRO_AI_PROVIDER_INTEGRATION_AND_DAILY_ASSISTANT_MODE`

## Enabled Subsystems

- `local_cli`: ENABLED; mode=local; approval=none
- `dashboard`: ENABLED; mode=local markdown; approval=none
- `smoke_tests`: ENABLED; mode=local; approval=none
- `telegram_dry_run`: ENABLED; mode=dry-run; approval=none
- `malyarka_synthetic`: ENABLED; mode=synthetic/manual test; approval=none
- `mock_ai_provider`: ENABLED; mode=mock; approval=none

## Disabled Subsystems

- `live_telegram`: DISABLED; mode=live external; approval=APPROVE_TELEGRAM_LIVE
- `real_ai_providers`: DISABLED; mode=external API; approval=APPROVE_SECRET_SETUP
- `google_drive_write`: DISABLED; mode=external write; approval=APPROVE_GOOGLE_DRIVE_MOVE
- `real_order_access`: DISABLED; mode=customer data; approval=APPROVE_REAL_ORDER_ACCESS
- `archive_import`: DISABLED; mode=old archive import; approval=APPROVE_ARCHIVE_UNPACK
- `delete_files`: DISABLED; mode=destructive; approval=APPROVE_DELETE

## Hard Runtime Gates

- can_start_live_services: `False`
- can_read_secrets: `False`
- can_touch_real_orders: `False`
- can_change_google_drive: `False`

This report is local. It does not read `.env`, tokens, keys, real orders, Google Drive files or old archives.
