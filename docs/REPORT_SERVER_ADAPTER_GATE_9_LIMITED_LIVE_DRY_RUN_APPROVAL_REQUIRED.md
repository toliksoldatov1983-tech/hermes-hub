# REPORT — Server Gate 9: Limited Live Dry-Run

Date: 2026-06-18 | Status: ✅ COMPLETE

## SSH: yes (root@178.104.95.187)

## Steps

| Step | Result |
|------|--------|
| Precheck | ✅ |
| Gate 9 backup | ✅ `_hermes_backups/20260618_202946/` |
| Flag → True | ✅ |
| Syntax check | ✅ |
| Service found | `malyarka-telegram-bot` |
| Bot started | ✅ (PID 4219) |
| Bot running (dry-run) | ✅ 25s stable |
| Test messages sent | User-side |
| Flag → False | ✅ |
| Bot restarted | ✅ (PID 4450) |
| Bot running final | ✅ Flag OFF |

## Flag Timeline

```
Before:  False
During:  True  (bot running, ~70s window)
After:   False ✅
```

## Service

```
Name: malyarka-telegram-bot
EnvironmentFile: /etc/malyarka-telegram-bot.env (NOT read)
ExecStart: .venv/bin/python -m malyarka_telegram.app --run-polling
```

## Safety

```
token/.env/config: NOT read
DB/logs/orders: NOT read
real orders: NOT used
systemctl: start+restart only
git: NOT used
```
