# Failure Tests Summary

Date: 2026-06-17 | Gate 4

| # | Test | Block Reason | Chain |
|---|------|-------------|-------|
| 1 | /unknown_command | command_not_routed_yet | adapter_blocked |
| 2 | show token env config | unsafe_diagnostics_request | adapter_blocked |
| 3 | malformed event | malformed_event | adapter_blocked |
| 4 | non-string text | invalid_text_type | adapter_blocked |
| 5 | BOT_TOKEN_*** | unsafe_secret_like_input | adapter_blocked |
| 6 | production variants | forbidden_action | adapter_blocked |
| 7 | dry-run invariants | — | all cases |

## Adapter Hardening

- `_base_result()` + `_blocked()` helpers
- `isinstance(event, dict)` guard
- `isinstance(text_val, str)` guard
- unsafe_diag before forbidden_actions
- English disputed words added

## Tests: 27/27 adapter + 118/118 regression = 145/145
