# Phase 2 — Monitoring Plan

Date: 2026-06-18

## Before Enable

- [ ] Flag OFF confirmed
- [ ] Bot running confirmed
- [ ] Backup fresh
- [ ] Rollback plan printed

## During Enable (2-4 hours)

- Watch bot uptime (systemctl status)
- Watch for crash/restart loops
- Check adapter blocks/passes if safe logging added
- NO reading DB/logs/orders contents

## After Disable

- [ ] Flag OFF confirmed
- [ ] Bot running confirmed
- [ ] No persistent errors

## Signs of Safe Dry-Run

- Bot stays up
- Clean orders process normally
- Blocked inputs blocked correctly
- No production exports triggered

## Signs of Problem

- Bot crashes or restarts
- Handler errors
- Unexpected behavior on clean input
