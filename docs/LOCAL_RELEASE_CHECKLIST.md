# LOCAL_RELEASE_CHECKLIST

Use this command from `C:\Users\user\Desktop\Hermes-Clean`:

```cmd
scripts\hermes.cmd release-checklist
```

It writes:

`05_REPORTS\LOCAL_RELEASE_CHECKLIST.md`

## Included

- readiness status;
- ready local commands;
- passed checks;
- open approval gates;
- pending approvals preview;
- next direction options.

## Safety

The checklist is local to Hermes-Clean. It does not call external APIs, read Google Drive, read old archives, read secrets or touch real orders.
