# Server Access Decision Tree

Date: 2026-06-18

```text
START
│
├─ Need read-only server access?
│   └─ YES → Ask RED approval first
│
├─ Temp root key removed?
│   └─ YES → Use Rescue reconnect steps
│
├─ Need live restart?
│   └─ YES → Separate RED approval
│
├─ Need secrets/config/.env?
│   └─ YES → FORBIDDEN without explicit approval
│
├─ Need production enable?
│   └─ YES → Separate gate
│
└─ Need cleanup?
    └─ YES → Remove temp root key
```
