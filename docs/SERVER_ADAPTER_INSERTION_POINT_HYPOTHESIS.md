# Server Adapter Insertion Point Hypothesis

Date: 2026-06-17 | Hypothesis only — NOT verified

## Where Telegram enters

```
app.py → aiogram Dispatcher → router.py → handlers.py
```

## Where adapter could fit

```python
# handlers.py (before processing)
@router.message()
async def handle_message(message: Message):
    # === HERMES ADAPTER INSERTION ===
    hermes_result = hermes_adapter.process(message.text)
    if hermes_result.blocked:
        return  # blocked by adapter
    
    # === Existing processing ===
    order = parse_order(message.text)
    ...
```

## Target file

`malyarka_telegram/handlers.py` (based on inventory)

## Why NO patch yet

1. Server file contents unknown
2. No SSH access confirmed
3. config.py/token/.env — NEVER touched
4. Live bot must not be disrupted
5. No staging environment

## Questions to verify

1. Does handlers.py exist at expected path?
2. Is there an existing message handler?
3. Is there feature-flags infrastructure?
4. Can adapter be inserted without breaking flow?
5. What imports are needed?
