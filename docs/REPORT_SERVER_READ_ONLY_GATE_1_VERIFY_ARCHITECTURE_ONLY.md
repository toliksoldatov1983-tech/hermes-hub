# REPORT — Server Read-Only Gate 1: Architecture Verification

Date: 2026-06-17 | Status: BLOCKED (timeout)

## Attempts

| # | Command | Result |
|---|---------|--------|
| 1 | ssh ubuntu@178.104.95.187 (15s) | Timeout |
| 2 | ssh ubuntu@178.104.95.187 (30s) | Timeout |

## Details

- Key: `hermes_temp_server_readonly` (ED25519)
- User confirmed public key added via Hetzner Console
- SSH connection timed out — server unreachable from Hermes

## Possible Causes

1. Firewall blocking port 22 from Hermes IP
2. Server not listening on SSH
3. Network routing issue
4. Hetzner security group

## Safety

```
private key: NOT read | token/env/config: NOT read
server: NO writes | live bot: NOT touched
```

## Next

User verifies Hetzner firewall allows SSH from Hermes host to 178.104.95.187:22.
