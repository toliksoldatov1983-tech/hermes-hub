# Adapter Contract

Date: 2026-06-17

## Input

```yaml
event:
  source: "fake_telegram"
  chat_id: "fake_chat_001"
  message_id: "fake_msg_001"
  text: "фасады МДФ RAL 9010 1000 x 400 x 4"
  has_photo: false
```

## Output

```yaml
result:
  adapter_mode: "fake"
  dry_run: true
  source: "fake_telegram"
  telegram_api_called: false
  server_called: false
  side_effects: []
  allowed: true/false
  block_reason: null | "empty_message" | "photo_not_supported" | "command_not_routed" | "unsafe_secret_like_input" | "forbidden_action"
  handoff_allowed: true/false
  review_required: true/false
  production_ready: false
```

## Invariants

- adapter_mode always "fake"
- dry_run always true
- telegram_api_called always false
- server_called always false
- side_effects always []
- production_ready always false
