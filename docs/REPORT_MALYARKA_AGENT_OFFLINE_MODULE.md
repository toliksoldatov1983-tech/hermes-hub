# REPORT — Malyarka Agent Offline Module

Date: 2026-06-17
Agent: Malyarka Agent (#2)
Status: accepted, offline_module_created, not active

## Result

```text
Tests: 28 passed, 0 failed in 0.10s
```

## Module

| File | Size |
|------|------|
| `src/__init__.py` | 48 B |
| `src/malyarka_agent.py` | 10 405 B |
| `tests/test_malyarka_agent.py` | 18 359 B |

## Functions

| # | Function | Purpose |
|---|----------|---------|
| 1 | `analyze_intake_card` | Analyze card structure |
| 2 | `build_preliminary_result` | Build full preliminary result |
| 3 | `split_confirmed_and_disputed` | Split rows by confirmation |
| 4 | `detect_missing_fields` | List missing required fields |
| 5 | `detect_blocking_flags` | List flags blocking finalization |
| 6 | `determine_order_status` | needs_clarification / blocked / ready |

## Tests (28)

| Group | Count |
|-------|-------|
| Scenarios 1-15 | 15 |
| Safety (not_final, separated, no_price) | 3 |
| Fake cards 001-010 | 10 |

## Safety

- ✅ Never counts final price
- ✅ Always `not_final_order: true`
- ✅ Confirmed/disputed always separated
- ✅ Material ambiguous → disputed
- ✅ Discount/tech/manager → blocked

## Status

`accepted, offline_module_created, not active`
