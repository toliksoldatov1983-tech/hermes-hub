# Phase 2 — Rollback Decision Tree

Date: 2026-06-18

```text
Problem detected?
│
├─ Bot crash → IMMEDIATE ROLLBACK
│   Set flag OFF, restart, verify
│
├─ Adapter blocking clean orders → ROLLBACK
│   Set flag OFF, restart, report issue
│
├─ Production action triggered → ROLLBACK
│   Set flag OFF, restart, audit
│
├─ Minor issue, flag OFF fixable → SOFT ROLLBACK
│   Set flag OFF, restart, no code restore
│
└─ telegram.py corrupted → HARD ROLLBACK
    Restore from backup (_hermes_backups/)
```

## When to Stop Test

- Any bot crash
- Any production action
- 2+ unexpected blocks on clean input
- After 4 hours max
