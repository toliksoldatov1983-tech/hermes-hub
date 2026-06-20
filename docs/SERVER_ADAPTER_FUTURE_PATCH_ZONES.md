# Server Adapter Future Patch Zones

Date: 2026-06-17 | No patch created

## Patch Zone A: New File

```
malyarka_core/adapters/hermes_adapter.py  ← CREATE (new)
```
Content: `check_hermes_safety(text)` function from Gate 3 contract.

## Patch Zone B: Hook Insertion

```
malyarka_core/adapters/telegram.py  ← MODIFY (3-line hook)
```
Insert at top of `build_order_preview_from_text`:
```python
if _HERMES_ADAPTER_ENABLED:
    # Hermes safety check
```

## Forbidden Zones

| File | Reason |
|------|--------|
| `handlers.py` | No changes needed |
| `router.py` | No changes needed |
| `orders.py` | No changes needed |
| `config.py` (any) | ⛔ Secrets |
| `.env` | ⛔ Secrets |
| DB/logs | ⛔ Live data |
