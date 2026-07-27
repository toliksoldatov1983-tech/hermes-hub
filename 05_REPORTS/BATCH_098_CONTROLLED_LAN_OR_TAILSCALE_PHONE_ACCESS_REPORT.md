# BATCH_098 — Controlled Phone Access

Дата: 2026-07-02 · Статус: **COMPLETED** · 614 passed

---

## CONTROLLED PHONE ACCESS ARCHITECTURE

```
Android Shell → Mobile Web UI → Mobile Gateway → Runtime Bridge → Hermes-Clean
```

Модули:
- `controlled_access/bind_mode.py` — 5 режимов, localhost default
- `controlled_access/access_policy.py` — проверка доступа по хосту/действиям
- `controlled_access/tailscale_readiness.py` — safe detection

## ACCESS POLICY

`AccessPolicy.check()`:
- localhost → ALLOWED
- Tailscale IP → PENDING_APPROVAL (нужен APPROVE_TAILSCALE_MODE)
- LAN IP → PENDING_APPROVAL (нужен APPROVE_LAN_MODE)
- 0.0.0.0 / public → PERMANENTLY_BLOCKED

10 hard-blocked действий: secret-read, live-telegram, google-drive, external-api, real-orders, delete, archive, gemini, deepseek.

## TAILSCALE READINESS

`detect_tailscale()` — проверяет наличие без установки/логина:
- `tailscale version` + `tailscale status --json`
- audit: no_install=True, no_network_change=True

## LAN READINESS

LAN disabled. Требует APPROVE_LAN_MODE + APPROVE_PHONE_PAIRING.
Tailscale рекомендован как более безопасный вариант.

## CLI COMMANDS (12 новых)

| Команда | Результат |
|---------|-----------|
| `phone-access-status` | OK |
| `phone-access-plan` | OK (Tailscale recommendation) |
| `tailscale-status-dry-run` | OK |
| `tailscale-access-plan` | OK |
| `tailscale-approval-check` | OK (pending_approval) |
| `lan-access-plan` | OK |
| `lan-approval-check` | OK (pending_approval) |
| `lan-security-dry-run` | OK |
| `pairing-status` | OK (dry-run) |
| `pairing-security-check` | OK |
| `phone-security-check` | OK |

## БЕЗОПАСНОСТЬ

Все пункты: .env не читался, firewall не менялся, сеть не менялась, Tailscale не устанавливался.

## СЛЕДУЮЩИЙ ШАГ

`BATCH_099_USER_DECISION_TAILSCALE_ENABLE_OR_TELEGRAM_INTENT_ROUTER`
