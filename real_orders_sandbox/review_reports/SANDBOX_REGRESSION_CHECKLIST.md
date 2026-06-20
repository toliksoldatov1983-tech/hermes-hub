# Sandbox Regression Checklist

Date: 2026-06-17

## After each chain change

| # | Check | Gate |
|---|-------|------|
| 1 | Sales agent tests | 48/48 |
| 2 | Malyarka agent tests | 28/28 |
| 3 | Corel agent tests | 18/18 |
| 4 | S→M integration | 12/12 |
| 5 | Full-chain simulation | 12/12 |
| 6 | Sandbox safe copy run | chain pass |
| 7 | not_final_order=true | always |
| 8 | Real folders not read | always |

## After new safe copy

| # | Check |
|---|-------|
| 1 | Manifest filled by user |
| 2 | No .cdr/.art/CNC |
| 3 | Chain processes successfully |
| 4 | Results not_final/review_required |
