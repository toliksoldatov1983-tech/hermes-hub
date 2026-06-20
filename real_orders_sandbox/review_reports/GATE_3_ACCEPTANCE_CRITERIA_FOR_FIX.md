# Gate 3 Acceptance Criteria for Fix

Date: 2026-06-17 | Approval: YELLOW — SALES_MALYARKA_GATE_4

## Fix 1: NCS Color

- [ ] NCS S4050-R → `color_raw: "NCS S4050-R"`, `color_scheme: "NCS"`
- [ ] NCS S 4050-R → same
- [ ] RAL 9010 → still `color_structured: "RAL 9010"`
- [ ] Plain "белый" → still raw, no scheme

## Fix 2: Disputed Classification

- [ ] "фрезеровка" without type → `disputed_order_field`, NOT `technical_advice_requested`
- [ ] "какой тип фрезеровки лучше?" → still `technical_advice_requested`
- [ ] "фрезеровка + покраска" without details → `disputed_order_field`

## Fix 3: Size Ambiguity

- [ ] "600 x 300" standalone → 600×300×1, confirmed
- [ ] "600 x 300" in file with "x 4" elsewhere → disputed or confirmed with note
- [ ] "1000 x 400 x 4" → still 1000×400×4

## Regression

- [ ] All 48 sales tests still pass
- [ ] All 25 golden cases still pass
- [ ] Integration tests unaffected
- [ ] Sandbox Gate 2 safe copy still chains correctly
