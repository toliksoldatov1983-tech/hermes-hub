# Simulation Runbook

Date: 2026-06-17

## Sales → Malyarka

```bash
python agents/local_simulation/sales_to_malyarka/run_simulation.py
pytest agents/local_simulation/sales_to_malyarka/test_sales_to_malyarka_integration.py -v
```

## Full-Chain

```bash
python agents/local_simulation/full_chain_sales_malyarka_corel/run_full_chain_simulation.py
pytest agents/local_simulation/full_chain_sales_malyarka_corel/test_full_chain_simulation.py -v
```

## Expected

- S→M: 10 messages, ~4 passed, ~6 blocked
- Full-chain: 12/12 tests
