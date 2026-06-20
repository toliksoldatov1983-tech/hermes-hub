# Full-Chain Acceptance Criteria

Date: 2026-06-17 | Tests: 12/12

1. Sales blocks cards with discount/tech/ambiguous material
2. Malyarka returns only preliminary_result (not_final_order=true)
3. Malyarka blocks disputed/blocked cards from reaching Corel
4. Corel uses only confirmed_rows (not disputed)
5. Corel row order: height_mm, width_mm, quantity
6. Corel returns not_final_export=true
7. No prices anywhere in chain
8. Existing modules NOT modified
