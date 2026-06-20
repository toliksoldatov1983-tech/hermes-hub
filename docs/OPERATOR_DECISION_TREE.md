# Operator Decision Tree

Date: 2026-06-17

```text
START
│
├─ SSH/Codex available?
│   ├─ YES → Server Read-Only Gate 1
│   │         → Safe File Review → Patch Plan → ...
│   └─ NO  → Continue local
│             ├─ More fake Telegram scenarios
│             ├─ More sandbox safe copies
│             └─ Docs/runbooks/decision maps
│
├─ Need production?
│   └─ YES → STOP — separate RED gate required
│
├─ Need live Telegram?
│   └─ YES → STOP — separate RED gate required
│
└─ All green tasks done?
    └─ YES → Wait for external access or new user direction
```
