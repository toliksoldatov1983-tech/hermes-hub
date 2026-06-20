# Server Hermes Adapter — Proposed Contract

Date: 2026-06-17 | No code

## Input

```yaml
event:
  text: str           # Telegram message text
  source: str         # "telegram"
  trace_id: str       # For debugging
```

## Output (allowed)

```yaml
output:
  blocked: false
  block_reason: null
  review_required: false
  handoff_allowed: true
  dry_run: true
  production_ready: false
  side_effects: []
  adapter_mode: "dry_run"
  source: "telegram"
```

## Output (blocked)

```yaml
output:
  blocked: true
  block_reason: "empty_message | unsafe_secret | forbidden_action | ..."
  handoff_allowed: false
  dry_run: true
  production_ready: false
  side_effects: []
```

## Output (error/fallback)

```yaml
output:
  blocked: false
  fallback_required: true
  reason: "adapter error — routing to original path"
  dry_run: true
  production_ready: false
```

## Block Reasons

`empty_message`, `unsafe_secret_like_input`, `forbidden_action`, `command_not_routed`, `photo_not_supported`, `missing_required_fields`, `malformed_event`, `invalid_text_type`, `safe_failure`
