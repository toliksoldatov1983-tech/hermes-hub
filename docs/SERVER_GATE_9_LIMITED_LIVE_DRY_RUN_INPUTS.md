# Server Gate 9 — Limited Live Dry-Run Inputs

Date: 2026-06-18 | Approval: RED

## Goal

Enable feature flag to True and verify Hermes adapter in live bot (limited window).

## What Changes

- `_HERMES_ADAPTER_ENABLED = True` in telegram.py file
- Bot restart MAY be required (RED)

## Preconditions

- [ ] Backup restored and verified
- [ ] Rollback plan ready
- [ ] Feature flag test passed (in-memory ✅)
- [ ] User explicitly approves RED gate

## NOT Yet

- Gate 8 complete → Gate 9 awaits RED approval
- Temp key still active
