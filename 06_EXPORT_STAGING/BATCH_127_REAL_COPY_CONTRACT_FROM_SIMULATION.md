# REAL COPY CONTRACT (from simulation to real folder)

## Files to copy (3)

1. demo_order_corel.txt
2. demo_order_malyarka.xlsx
3. demo_order_export_report.md

## Rules

- Copy ONLY (not move)
- No overwrite — if target exists, STOP
- No delete
- No move
- Target = {root}\{year}\{month}\{order_name}\

## Collision

- If target file exists → STOP, no overwrite
- Duplicate-safe suffix only by explicit plan
- Never delete target

## Verification

- Source staging files must remain unchanged
- Target file names match source
- Target file sizes match source
- Manifest required in target folder

## Source

- Staging: `06_EXPORT_STAGING\`
- Contract: Corel TXT (empty first line, tab, H/W/Qty), Excel (9 cols)
