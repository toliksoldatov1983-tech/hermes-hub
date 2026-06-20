# Failure Matrix

Date: 2026-06-17 | Gate 3

| # | Input | Blocked At | Reason | Chain |
|---|-------|-----------|--------|-------|
| 1 | Empty message | Adapter | empty_message | ❌ |
| 2 | Token-like input | Adapter | unsafe_secret_like_input | ❌ |
| 3 | Production action | Adapter | forbidden_action | ❌ |
| 4 | Photo without text | Adapter | photo_not_supported | ❌ |
| 5 | Clean order | — | — | ✅ full |
| 6 | Disputed order | Sales | review_required | ⚠ blocked |
| 7 | Unknown command | Adapter | command_not_routed | ❌ |
| 8 | Unsafe diagnostics | Adapter | forbidden_action | ❌ |
| 9 | Missing fields | Sales | needs_clarification | ⚠ review |
| 10 | Unexpected exception | — | safe_failure | ❌ + false |

## Legend

- ✅ = full chain pass (adapter→sales→malyarka→corel)
- ⚠ = blocked with review_required, production_ready=false
- ❌ = blocked, no chain call, production_ready=false
