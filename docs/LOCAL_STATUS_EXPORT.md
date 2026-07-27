# LOCAL_STATUS_EXPORT

Use this command from `C:\Users\user\Desktop\Hermes-Clean`:

```cmd
scripts\hermes.cmd export-status
```

It writes:

`05_REPORTS\LOCAL_STATUS_EXPORT.md`

## Included

- health status;
- smoke status;
- active batch;
- next task;
- done count;
- reports count;
- safe commands;
- pending approvals preview.

## Safety

The export is local to Hermes-Clean. It does not call external APIs, read Google Drive, read old archives, read secrets or touch real orders.
