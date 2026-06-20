# Gate 3 Bugfix Plan — NO CODE

Date: 2026-06-17 | Status: PLAN ONLY — code NOT modified

## Fix 1: NCS Color (intake_agent.py)

| What | Where | How |
|------|-------|-----|
| Add NCS pattern | COLOR_INDICATORS | Add regex: `r'NCS\s*S?\s*\d{4}\s*-\w'` |
| Add color scheme | _extract_color | Return `color_scheme: "NCS"` |
| Add test | test_golden_cases.py | GC_NCS_color_detected |

## Fix 2: Disputed Classification (intake_agent.py)

| What | Where | How |
|------|-------|-----|
| Split TECHNICAL_QUESTION_WORDS | constants | Remove "фрезеровк" from tech questions |
| Add MISSING_SPEC_WORDS | constants | New list: ["фрезеровк", "тип фрезеровки"] |
| Add flag | analyze_client_message | `disputed_order_field` instead of `technical_advice_requested` |
| Add test | test_golden_cases.py | GC_milling_without_type |

## Fix 3: Size Ambiguity (intake_agent.py)

| What | Where | How |
|------|-------|-----|
| Detect quantity context | _extract_sizes | Check if adjacent lines use "x N" quantity format |
| Default qty=1 | _extract_sizes | When no quantity in context |
| Mark ambiguous | _extract_sizes | When trailing quantity possible |
| Add test | test_golden_cases.py | GC_size_without_qty |

## Target File

`agents/sales_client_intake_agent/src/intake_agent.py` — ONLY this file.

## Approval Needed

YELLOW — requires code modification. Tests will be added. Existing agents not affected at runtime.
