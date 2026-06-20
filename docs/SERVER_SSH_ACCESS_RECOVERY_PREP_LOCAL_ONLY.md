# Server SSH Access Recovery Prep — Local Only

Date: 2026-06-17 | NO server connection

## Key Status

| Check | Result |
|-------|--------|
| Private key exists | ✅ /c/Users/user/.ssh/hetzner_hermes (399B) |
| Public key exists | ✅ hetzner_hermes.pub (92B) |
| Fingerprint match | ✅ Both: SHA256:Ca/i3mcrkZQiQqm0S72BthD7AcyJ5ZPQ6uA9YEWm2og |
| Key type | ED25519 |
| Private key perms | 644 (should be 600 for SSH) |
| SSH config | No ~/.ssh/config |

## Connection Attempt (Gate 1)

```
ssh -i ~/.ssh/hetzner_hermes ubuntu@49.13.76.163
Result: Permission denied (publickey)
```

## Possible Causes

1. Public key not in server `~ubuntu/.ssh/authorized_keys`
2. Wrong username (not ubuntu?)
3. Private key permissions too open (644 vs required 600)
4. Server replaced/changed
5. Hetzner firewall/security group
