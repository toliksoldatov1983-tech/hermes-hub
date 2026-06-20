# Phase 2 — Test Matrix

Date: 2026-06-18

| # | Input | Expected |
|---|-------|----------|
| 1 | `"фасады МДФ 1000x400x4"` | ✅ not blocked, preview created |
| 2 | `"фрезеровка покраска"` | ⚠ review_required, no export |
| 3 | `"/start"` | ❌ blocked (command) |
| 4 | `""` (empty) | ❌ blocked (empty) |
| 5 | `"production export now"` | ❌ blocked (forbidden) |
| 6 | `"BOT_TOKEN=*** | ❌ blocked (unsafe) |
| 7 | Random text without sizes | Fallback to original path |

## Invariants (all tests)

- dry_run=true, production_ready=false
- No export/admin/write
- No Telegram API calls from adapter
