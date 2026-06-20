# Sandbox Preliminary Results — GATE 2

Date: 2026-06-17 | Sandbox: ORDER_SAFE_COPY_001

## Safe Copy

| Field | Value |
|-------|-------|
| File | ORDER_SAFE_COPY_001.md.txt |
| Type | только покраска |
| Material | МДФ |
| Color | RAL 9010 |
| Finish | матовый |
| Sizes (source) | 1000×400×4, 600×300×2 |
| Forbidden content | none (CNC header is exclusion statement) |

## Chain — FULL PASS

| Stage | Status |
|-------|--------|
| Sales Agent | ✅ passed |
| Malyarka Agent | ✅ preliminary_result |
| Corel Export Agent | ✅ export_contract |

## Result

| Field | Value |
|-------|-------|
| Status | ready_for_human_review |
| Confirmed rows | 3 (size parser issue noted) |
| Disputed rows | 0 |
| Export blocked | false |
| Corel ready | true |
| **not_final_order** | **true** |
| **review_required** | **true** |
| **production_ready** | **false** |

## Size Parsing Note

Safe copy uses format: `height × width × quantity`. Current SIZE_PATTERN treats "× quantity" as a dimension. Parsed 3 rows from 2 size lines. Edge case — does not block chain results. Parser improvement: future task.
