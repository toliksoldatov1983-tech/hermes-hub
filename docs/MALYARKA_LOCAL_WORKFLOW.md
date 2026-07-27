# MALYARKA_LOCAL_WORKFLOW

This document describes the current local dry-run Malyarka workflow.

## Command

```cmd
scripts\hermes.cmd malyarka-workflow
```

## Workflow

1. Parse synthetic input.
2. Build preview.
3. Detect disputed rows.
4. Resolve a disputed row with explicit replacement.
5. Keep export blocked until a future approved block.

## Safety

This workflow uses synthetic input only. It does not read real orders, Excel, Google Drive, old archives, secrets or client documents.
