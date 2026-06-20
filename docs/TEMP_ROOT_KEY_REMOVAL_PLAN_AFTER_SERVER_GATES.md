# Temp Root Key Removal Plan

Date: 2026-06-17 | DO NOT execute

## Key Info

| Field | Value |
|-------|-------|
| Comment | `hermes-temp-readonly` |
| Location | `/root/.ssh/authorized_keys` |
| Local file | `C:\Users\user\.ssh\hermes_temp_server_readonly` |

## When to Remove

After all server read-only gates complete (Gates 1-5) and no further server access needed.

## Removal Command (as root)

```bash
sed -i '/hermes-temp-readonly/d' /root/.ssh/authorized_keys
```

## NOT Now

- Gates 1-3 complete, Gates 4-5 pending
- Key still needed for future gates
- Do NOT remove until explicitly approved
