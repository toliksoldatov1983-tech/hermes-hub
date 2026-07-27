# MALYARKA_DISPUTE_RESOLUTION_CONTRACT

This is a local dry-run contract for resolving disputed Malyarka rows.

## Command

```cmd
scripts\hermes.cmd malyarka-resolve "paint 2 bucket" --replacement "paint | 2 | bucket"
```

## Rule

A disputed row can only be replaced by an explicit replacement row in this format:

`item | quantity | unit`

## Safety

This contract does not read real orders, Excel files, Google Drive, old archives, secrets or client documents. Final export remains blocked until a future approved block.
