# LOCAL_APP_RUNTIME

Hermes-Clean can be used as a local dry-run application from:

`C:\Users\user\Desktop\Hermes-Clean`

## First command

```cmd
scripts\start_hermes.cmd
```

## Runtime checks

```cmd
scripts\smoke.cmd
scripts\export_status.cmd
scripts\release_checklist.cmd
scripts\run_tests.cmd
```

## Direct CLI

```cmd
scripts\hermes.cmd start-summary
scripts\hermes.cmd health
scripts\hermes.cmd reports
scripts\hermes.cmd smoke
scripts\hermes.cmd export-status
scripts\hermes.cmd release-checklist
```

## Safety

This local runtime does not call external APIs, read Google Drive, read old archives, read secrets, launch live Telegram or touch real orders.
