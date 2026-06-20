# REPORT — SSH Access Recovery Prep

Date: 2026-06-17

## Findings

| Check | Result |
|-------|--------|
| Key exists | ✅ ED25519, 399B |
| Fingerprint match | ✅ Both SHA256:Ca/i3mcrkZQiQqm0S72BthD7AcyJ5ZPQ6uA9YEWm2og |
| Private key perms | 644 (should be 600) |
| SSH config | Not found |
| New SSH attempts | 0 (none) |

## Most Likely Cause

Public key not present in server `authorized_keys` for user ubuntu.

## Created

| Doc | Purpose |
|-----|---------|
| Recovery prep | Analysis |
| Checklist | 10 checks |
| User steps | Manual actions |
| Retry prompt | Ready RED gate prompt |
