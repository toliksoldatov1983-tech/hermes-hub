# BATCH_122 — SAFE-LOCAL FALLBACK PLAN

## Plan

Если оператор выберет вариант C, выполнить safe-local simulation.

## Source

```
C:\Users\user\Desktop\Hermes-Clean\06_EXPORT_STAGING\
```

## Simulation Target

```
C:\Users\user\Desktop\Hermes-Clean\07_REAL_FOLDER_SIMULATION\demo_order\
```

## Allowed Actions (inside Hermes-Clean only)

1. Create simulation folder `07_REAL_FOLDER_SIMULATION\demo_order\`
2. Copy staging files using **no-overwrite**:
   - `demo_order_corel.txt`
   - `demo_order_malyarka.xlsx`
   - `demo_order_export_report.md`
3. Create copy manifest in target folder
4. Verify file names and sizes
5. Confirm source files unchanged

## Explicit Disclaimer

- ⚠️ Это НЕ real order folder
- ⚠️ Это НЕ E:\Заказы
- ⚠️ Это НЕ production copy
- ℹ️ Это ТОЛЬКО simulation для проверки механики

## Required Approvals

- No dangerous approvals needed (simulation only)
- All actions inside Hermes-Clean
- No real order folders touched

## Next After Simulation

- BATCH_123 — simulation execution
- BATCH_124 — simulation verification
- BATCH_125 — simulation closeout
