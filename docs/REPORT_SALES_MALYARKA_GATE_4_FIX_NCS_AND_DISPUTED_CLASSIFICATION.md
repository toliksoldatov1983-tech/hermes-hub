# REPORT — Sales Malyarka Gate 4 Fix

Date: 2026-06-17 | Approval: YELLOW → Gate 4 COMPLETE

## Changes — intake_agent.py only

| Fix | What Changed |
|-----|-------------|
| NCS color | NCS_PATTERN regex widened, scheme="NCS" added |
| Milling type | "фрезеровк"/"фрезер" moved from TECHNICAL_QUESTION to MISSING_SPEC_WORDS |
| missing_spec | New _has_missing_spec() + disputed_order_field flag |
| Size qty | Already defaults to 1 (no change needed) |

## Tests

| Suite | Before | After |
|-------|--------|-------|
| Sales intake tests | 23 | 23 |
| Golden cases | 25 | 25 |
| **Total** | **48** | **48** |

```text
48 passed, 0 failed in 0.17s
```

## Gate 3 Recheck

- NCS S4050-R: ✅ detected as color_raw + scheme=NCS
- Missing milling type: ✅ disputed_order_field (not tech_advice)
- 600×300: ✅ qty defaults to 1
- Gate 3 text: NCS found, no false missing_color, no false tech_advice

## Next Gate

`REAL_ORDERS_SANDBOX_GATE_5_RECHECK_GATE_3_SCENARIO_AFTER_FIX`
