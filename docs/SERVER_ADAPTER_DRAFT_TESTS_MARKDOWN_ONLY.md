# Server Adapter Draft Tests (Markdown Only)

Date: 2026-06-17 | DO NOT create test files

## Proposed tests for future `test_hermes_adapter.py`

### Test: Feature Flag Off
```python
# Flag OFF → original path, no Hermes call
_HERMES_ADAPTER_ENABLED = False
result = build_order_preview_from_text("фасады МДФ")
assert "blocked" not in result  # original path
```

### Test: Clean Order, Flag ON
```python
_HERMES_ADAPTER_ENABLED = True
result = build_order_preview_from_text("фасады МДФ 1000x400x4")
assert result["confirmed_count"] > 0
```

### Test: Empty Message Blocked
```python
result = check_hermes_safety("")
assert result["blocked"] is True
assert result["block_reason"] == "empty_message"
```

### Test: Token Input Blocked
```python
result = check_hermes_safety("BOT_TOKEN=***assert result["blocked"] is True
assert result["block_reason"] == "unsafe_secret_like_input"
```

### Test: Production Action Blocked
```python
result = check_hermes_safety("production order")
assert result["blocked"] is True
assert result["block_reason"] == "forbidden_action"
```

### Test: Malformed Input
```python
result = check_hermes_safety(None)
assert result["blocked"] is True
assert result["block_reason"] == "malformed_event"
```

### Test: Invariants
```python
for text in ["", "фасады", "production"]:
    r = check_hermes_safety(text)
    assert r["dry_run"] is True
    assert r["production_ready"] is False
    assert r["telegram_api_called"] is False
    assert r["server_called"] is False
    assert r["side_effects"] == []
```

## NOT Created

No real test files. Draft only.
