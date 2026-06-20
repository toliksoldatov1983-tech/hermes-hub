# Offline Regression Checklist

Date: 2026-06-17

| # | Check | Suite | Expected |
|---|-------|-------|----------|
| 1 | Sales agent tests | test_intake_agent.py | 48/48 |
| 2 | Sales golden cases | test_golden_cases.py | 25/25 |
| 3 | Malyarka agent tests | test_malyarka_agent.py | 28/28 |
| 4 | Corel agent tests | test_corel_export_agent.py | 18/18 |
| 5 | Sales→Malyarka integration | test_sales_to_malyarka_integration.py | 12/12 |
| 6 | Full-chain integration | test_full_chain_simulation.py | 12/12 |
| 7 | Row order check | height_mm before width_mm | ✅ |
| 8 | Not final order | all agents | true |
| 9 | No price | all agents | absent |
