# Agent Registry

Date: 2026-06-17 | Active: **0**

| # | Agent | Tests | Chain |
|---|-------|-------|-------|
| 1 | Sales + Client Intake | 48/48 | ✅ → Malyarka |
| 2 | Malyarka | 28/28 | ✅ ← Sales, → Corel |
| 3 | Corel Export | 18/18 | ✅ ← Malyarka |
| 4-6 | Telegram/Memory/Diagnostics | — | spec only |

## Full-Chain Verified

```text
Sales (#1) → Malyarka (#2) → Corel Export (#3)
  ✅ 12/12 integration tests (0.07s)
  ✅ 4/10 messages passed full chain
```
