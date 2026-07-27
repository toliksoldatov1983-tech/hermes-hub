# LOCAL_REFRESH_ALL

Use this command:

```cmd
scripts\hermes.cmd refresh-all
```

It refreshes local summary reports:

- `05_REPORTS\LOCAL_STATUS_EXPORT.md`
- `05_REPORTS\LOCAL_RELEASE_CHECKLIST.md`
- `05_REPORTS\TELEGRAM_DRY_RUN_STATUS.md`
- `05_REPORTS\MALYARKA_MODULE_STATUS.md`
- `05_REPORTS\LOCAL_DASHBOARD.md`

It does not call external APIs, read secrets, start live Telegram, change Google Drive, read real orders or unpack old archives.
