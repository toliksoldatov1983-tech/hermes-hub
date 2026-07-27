# LOCAL_PROJECT_AUDIT

Generated: 2026-07-28T02:14:51

## Summary

- status: `ATTENTION`
- checks: `25`
- failed: `2`

## Checks

- `required_paths`: OK; missing=0; env_files=0
- `no_env_anywhere`: OK; found=0
- `next_task_exists`: OK; 03_TASKS/NEXT_TASK.md
- `next_task_has_id`: FAIL; id=MISSING
- `reports_count_adequate`: OK; count=175
- `dashboard_exists`: OK; 05_REPORTS/LOCAL_DASHBOARD.md
- `daily_report_exists`: OK; 05_REPORTS/DAILY_LOCAL_REPORT.md
- `runtime_status_exists`: OK; 05_REPORTS/LOCAL_RUNTIME_STATUS.md
- `telegram_status_exists`: OK; 05_REPORTS/TELEGRAM_DRY_RUN_STATUS.md
- `live_services_disabled`: OK; live services disabled
- `secret_reading_disabled`: OK; secret reading disabled
- `real_order_access_disabled`: OK; real order access disabled
- `google_drive_write_disabled`: OK; google drive write disabled
- `disabled_live_telegram`: OK; live_telegram is DISABLED
- `disabled_real_ai_providers`: OK; real_ai_providers is DISABLED
- `disabled_google_drive_write`: OK; google_drive_write is DISABLED
- `disabled_real_order_access`: OK; real_order_access is DISABLED
- `disabled_archive_import`: OK; archive_import is DISABLED
- `disabled_delete_files`: OK; delete_files is DISABLED
- `enabled_subsystems_count`: OK; enabled=6
- `command_docs_exist`: OK; all found
- `command_coverage`: FAIL; missing=17: ai-provider-status, ai-provider-mock, ai-provider-capabilities, review-provider-mock, review-provider-disabled
- `git_status`: OK; git exists (not checked)
- `source_modules_exist`: OK; hermes_core modules=108
- `malyarka_module_exists`: OK; modules=27

## Actionable Findings

- **next_task_has_id**: id=MISSING → Update 03_TASKS/NEXT_TASK.md with a valid BATCH_ id, END_OF_PIPELINE or END_OF_PIPELINE_ARCHIVED.
- **command_coverage**: missing=17: ai-provider-status, ai-provider-mock, ai-provider-capabilities, review-provider-mock, review-provider-disabled → Update docs to cover missing commands.

## Safety

This audit is local to Hermes-Clean. It does not read `.env`, tokens, keys, real orders, client documents, Google Drive files or old archives.
