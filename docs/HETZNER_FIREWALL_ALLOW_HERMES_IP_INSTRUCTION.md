# Hetzner Firewall — Allow Hermes IP (not needed now)

Date: 2026-06-17

## Status

Firewall is NOT the issue. TCP 22 is already open. But for reference:

## Hermes Outbound IP

```
185.13.22.202
```

## Rule (if needed later)

```text
Direction: INBOUND
Protocol: TCP
Port: 22
Source: 185.13.22.202/32
Server: 178.104.95.187
```

## Current Issue

Not firewall — public key not accepted by server. Check `authorized_keys`.
