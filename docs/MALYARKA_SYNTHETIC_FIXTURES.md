# MALYARKA_SYNTHETIC_FIXTURES

The Malyarka fixtures are synthetic examples only.

They are not real orders, not imported from archives, not read from Google Drive and not based on client documents.

## Command

```cmd
scripts\hermes.cmd malyarka-fixtures
```

## Covered Cases

- ready single-line order;
- ready multi-line order;
- missing separator dispute;
- non-numeric quantity dispute;
- negative quantity dispute.
- ready row with unknown synthetic price;
- empty item dispute;
- empty unit dispute;
- mixed valid/disputed rows.

## Safety

The command uses hardcoded synthetic strings inside Hermes-Clean. It does not read external files, Excel workbooks, old archives, Google Drive, secrets or real order data.
