# Test Scenarios

Date: 2026-06-17

| # | Scenario | Expected |
|---|----------|----------|
| 1 | Clean order | allowed, handoff=true |
| 2 | Disputed order | review_required=true |
| 3 | Empty message | blocked |
| 4 | Production action | blocked |
| 5 | Token-like input | blocked |
| 6 | Command /start | blocked |
| 7 | Photo placeholder | blocked |
| 8 | dry_run invariant | always true |
| 9 | production_ready invariant | always false |
| 10 | No telegram API | always false |
| 11 | No server | always false |
| 12 | No side effects | always [] |
