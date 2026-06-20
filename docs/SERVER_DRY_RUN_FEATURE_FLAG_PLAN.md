# Server Dry-Run Feature Flag Plan

Date: 2026-06-17 | No code

## Flags

| Flag | Default | File |
|------|---------|------|
| `_HERMES_ADAPTER_ENABLED` | `False` | `adapters/telegram.py` |
| `_HERMES_DRY_RUN` | `True` | `adapters/hermes_adapter.py` |

## Behavior

| `_HERMES_ADAPTER_ENABLED` | Effect |
|---------------------------|--------|
| `False` (default) | Original path, no Hermes calls |
| `True` | Hermes checks run, block/route |

| `_HERMES_DRY_RUN` | Effect |
|-------------------|--------|
| `True` (default) | No side effects, production_ready=false |
| `False` | Requires separate RED approval |

## Diagnostics Fields (dry-run)

```yaml
trace_id: "uuid"
adapter_mode: "dry_run"
dry_run: true
telegram_api_called: false
server_called: false
side_effects: []
production_ready: false
```

## Rollback

Set `_HERMES_ADAPTER_ENABLED = False` → original path restored.
No code deletion needed.
