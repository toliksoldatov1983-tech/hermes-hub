# Server Read-Only Target Map

Date: 2026-06-17 | RED gate prep — hypothesis only

## Goal

Future RED gate: read-only verification of server architecture.

## Known Server Path

```
/opt/malyarka-telegram-bot
```

## Known Architecture (from inventory)

```
Telegram → app.py → aiogram Dispatcher → router.py → handlers.py
→ malyarka_core/services/orders.py → parsing/validation/calculations → exports/files
```

## Future Adapter Layer

```
Telegram → app.py → router.py / handlers.py
→ Hermes adapter → malyarka_core/services/orders.py
```

## Verification Goals

1. Confirm file existence/structure
2. Identify insertion point for adapter
3. Map router/handler boundaries
4. Verify feature-flags infrastructure
5. Confirm NO secrets in visible files

## Status

Hypothesis only. NOT verified. NOT patched.
