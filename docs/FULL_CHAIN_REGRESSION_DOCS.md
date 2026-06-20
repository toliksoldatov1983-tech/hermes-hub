# Full-Chain Regression Docs

Date: 2026-06-17 | Baseline: 118 tests passed

## What Regresses

1. Any change to Sales agent src/ → run 48+25 tests
2. Any change to Malyarka agent src/ → run 28 tests
3. Any change to Corel agent src/ → run 18 tests
4. Any agent interface change → run integration 12+12 tests
5. Any row order change → verify height_mm before width_mm

## Regression Gate

Run `OFFLINE_REGRESSION_CHECKLIST.md` after any code change.
All 118 must pass before proceeding.
