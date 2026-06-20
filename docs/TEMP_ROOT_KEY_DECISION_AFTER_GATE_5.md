# Temp Root Key Decision After Gate 5

Date: 2026-06-17

## Status

| Field | Value |
|-------|-------|
| Key | `hermes_temp_server_readonly` (ED25519) |
| Server | 178.104.95.187 |
| User | root |
| Active | YES (needed for Gate 6) |

## Why Still Needed

Gate 6 (RED) requires SSH for:
- Creating backup on server
- Writing `hermes_adapter.py`
- Modifying `adapters/telegram.py`

## When to Remove

After Gate 6 (or after all server write gates complete).

## Why Remove

- Temp key should not persist
- Security best practice
- Only needed for Hermes read-only/write gates

## Removal

```bash
sed -i '/hermes-temp-readonly/d' /root/.ssh/authorized_keys
```

Requires **separate approval** after all server gates.
