# REPORT — Gate 4 Local Failure Tests

Date: 2026-06-17

## Added Tests — 7 new

| Test | Checks |
|------|--------|
| unknown command | blocked, no chain call |
| unsafe diagnostics | blocked (unsafe_diagnostics_request) |
| malformed event | blocked (malformed_event) |
| non-string text | blocked (invalid_text_type) |
| secret masking | blocked, "unsafe" in reason |
| production variants | 3 variants blocked |
| dry-run all failures | invariants for all cases |

## Adapter Updated

- `_base_result()` + `_blocked()` helpers
- `isinstance(event, dict)` guard
- `isinstance(text_val, str)` guard
- unsafe_diag check BEFORE forbidden_actions
- English disputed words added

## Tests

```text
Adapter: 27/27 (0.07s) + Regression: 118/118 (0.19s) = 145/145 ✅
```
