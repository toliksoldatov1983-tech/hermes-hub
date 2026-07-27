# STAGING MANIFEST

- staging_batch_id: BATCH_114
- review_batch_id: BATCH_115
- source_type: fake_dry_run
- staging_only: TRUE
- real_order_folder_write_allowed: FALSE
- overwrite_used: FALSE
- delete_used: FALSE
- review_status: PASS

## Files

| File | Size |
|------|------|
| demo_order_corel.txt | 33 B |
| demo_order_export_preview.json | 767 B |
| demo_order_export_report.md | 1274 B |
| demo_order_malyarka.xlsx | 5232 B |

## Verification

- Corel TXT: first line empty ✓, no headers ✓, tab delimiter ✓, H/W/Qty ✓
- Excel XLSX: 9 columns ✓, area correct ✓, face only ✓
- JSON: staging_only=true ✓, audit metadata ✓
- Report: E:\Заказы not touched ✓

## Safety

- E:\Заказы: NOT touched
- Desktop\orders: NOT touched
- Google Drive: NOT touched
- CorelDRAW: NOT launched
- ArtCAM: NOT launched
- Overwrite: NOT used
- Delete: NOT used
