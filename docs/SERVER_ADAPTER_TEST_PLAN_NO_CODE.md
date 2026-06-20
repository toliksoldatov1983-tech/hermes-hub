# Server Adapter Test Plan — No Code

Date: 2026-06-17 | Future tests only

| # | Test | Expected |
|---|------|----------|
| 1 | Adapter off by default | Original flow, no Hermes call |
| 2 | dry_run always true | production_ready=false |
| 3 | Clean order passthrough | Full chain, not blocked |
| 4 | Disputed order blocked | review_required=true, no export |
| 5 | Forbidden export action blocked | blocked at adapter |
| 6 | Admin/write action blocked | blocked at adapter |
| 7 | Malformed adapter output | Fallback to original path |
| 8 | fallback_required on error | Original path, no crash |
| 9 | No token/env access | No env reads in adapter |
| 10 | No Telegram API calls | telegram_api_called=false |
| 11 | Feature flag respect | Off → original, On → Hermes |
