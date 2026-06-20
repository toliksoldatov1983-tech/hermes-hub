# REPORT — Corel Export Agent Offline Module

Date: 2026-06-17 | Status: accepted, offline_module_created, not active

## Result

```text
Tests: 18/18 passed (0.08s)
```

## Revision: row-order corrected (2026-06-17)

**Before:** width_mm, height_mm, quantity (W×H in preview)
**After:** **height_mm, width_mm, quantity** (H×W in preview)

Changed:
- `extract_corel_rows` — dict keys: height_mm, width_mm, quantity
- `build_corel_preview` — display: H×W mm
- `EXPORT_CONTRACT.md` — documented order
- `test_corel_row_format` — strict key order check
- `test_preview_format` — verifies H×W display

## Corrected count

Previous report: "создано 5" — actual was **4** files (__init__.py, corel_export_agent.py, test_corel_export_agent.py, EXPORT_CONTRACT.md). REGISTRY was updated (not created). Corrected.
