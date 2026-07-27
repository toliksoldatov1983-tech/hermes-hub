# MALYARKA_FUTURE_WORKFLOW

Input data -> primary parse -> preview -> confirmed / disputed rows -> dispute correction -> new version -> final readiness.

A disputed row blocks final action.

## Local dry-run row format

Current local parser contract accepts manually provided dry-run lines:

```text
item name | quantity | unit
```

Examples:

```text
краска | 2 | л
шпаклёвка | 5 | кг
```

## Preview result

The preview separates:

- confirmed rows;
- disputed rows;
- final readiness.

Final export remains blocked until:

1. all disputed rows are resolved;
2. user explicitly approves export in a future block;
3. real order access is approved if real data is involved.

## Current limitations

- No real orders.
- No Excel/client sheets.
- No archive import.
- No Google Drive documents.
- No final export.
