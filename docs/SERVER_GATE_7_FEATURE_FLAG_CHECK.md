# Gate 7 — Feature Flag Check

Date: 2026-06-18 | Status: ✅ CONFIRMED

## telegram.py line 22

```python
_HERMES_ADAPTER_ENABLED = False  # off by default
```

## Impact

- Flag OFF → Hermes hook never executes
- Original `build_order_preview_from_text` path intact
- Feature flag can only be changed by root on server
