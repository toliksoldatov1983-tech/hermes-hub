# Server Adapter Phase 2 — Controlled Enable Plan

Date: 2026-06-18 | Status: PLANNING ONLY

## What Phase 2 Is

Temporary controlled enable of Hermes adapter for extended dry-run testing with real Telegram messages.

## What Phase 2 Is NOT

- ❌ Production rollout
- ❌ Permanent enable
- ❌ production_ready=true

## Prerequisites

- [ ] Feature flag currently OFF
- [ ] Bot running
- [ ] Reconnect kit ready
- [ ] RED approval obtained
- [ ] Backup fresh
- [ ] Rollback plan ready

## Procedure

1. Reconnect to server (Rescue if needed)
2. Create fresh backup
3. Set flag ON, syntax check
4. Restart bot controlled
5. Run test matrix (2-4 hours)
6. Monitor logs for errors (no secrets)
7. If issues: immediate rollback
8. Set flag OFF, restart bot
9. Remove temp key

## Success Criteria

- All test matrix passed
- No crashes
- No production actions triggered
- Flag successfully reverted OFF
