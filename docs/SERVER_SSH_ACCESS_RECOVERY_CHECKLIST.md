# SSH Access Recovery Checklist

Date: 2026-06-17

| # | Check | Status |
|---|-------|--------|
| 1 | Private key file exists | ✅ |
| 2 | Public key file exists | ✅ |
| 3 | Fingerprints match | ✅ |
| 4 | Key type ED25519 | ✅ |
| 5 | Private key permissions 600 | ❌ (644) |
| 6 | SSH config exists | ❌ |
| 7 | Server IP correct | ? (49.13.76.163) |
| 8 | Username correct | ? (ubuntu) |
| 9 | Public key in authorized_keys | ? (server-side) |
| 10 | Hetzner firewall allows SSH | ? |
