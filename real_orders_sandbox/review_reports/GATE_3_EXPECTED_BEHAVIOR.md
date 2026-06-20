# Gate 3 Expected Behavior

Date: 2026-06-17

## Fix 1: NCS Color Detection

| Input | Expected |
|-------|----------|
| NCS S4050-R | `color_raw: "NCS S4050-R"`, `color_scheme: "NCS"` |
| NCS S 4050-R | `color_raw: "NCS S 4050-R"`, `color_scheme: "NCS"` |
| RAL 9010 | `color_structured: "RAL 9010"` (unchanged) |

**Rule:** NCS colors are valid structured colors. Detect "NCS S..." or "NCS S..." patterns. Never treat as missing.

## Fix 2: Disputed Field Classification

| Input | Expected |
|-------|----------|
| "фрезеровка" without type | `disputed_order_field`, reason: `missing_milling_type` |
| "фрезеровка + покраска" without details | `disputed_order_field`, reason: `missing_milling_type` |
| Client asks "какой тип фрезеровки лучше?" | `technical_advice_requested` (unchanged) |

**Rule:** Missing specification ≠ technical advice request. Only client questions trigger `technical_advice_requested`. Missing fields trigger `disputed_order_field`.

## Fix 3: Size Without Quantity

| Input | Expected |
|-------|----------|
| "600 x 300" (standalone) | `600×300×1`, confirmed |
| "600 x 300" next to "x 4" | ambiguous → disputed |
| "1000 x 400 x 4" | `1000×400×4` (unchanged) |

**Rule:** Single "N x M" without trailing quantity → default qty=1. If ambiguous context (next to "x Q" lines) → disputed.
