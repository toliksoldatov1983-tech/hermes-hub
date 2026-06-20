# Server Gate 8 — Dry-Run Activation Plan Inputs

Date: 2026-06-18

## Goal

Plan for enabling feature flag to True on server for limited dry-run test.

## Requirements

- Feature flag `_HERMES_ADAPTER_ENABLED = True`
- Bot restart MAY be needed (requires RED approval)
- Limited time window
- Rollback plan ready
- Backup verified restorable

## NOT Yet

- Do NOT enable flag without separate RED approval
- Do NOT restart bot without separate RED approval
- Temp root key still active

## Status

Gate 7 passed → ready for Gate 8 planning.
