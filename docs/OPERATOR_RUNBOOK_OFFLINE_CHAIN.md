# Operator Runbook — Offline Chain

Date: 2026-06-17

## Quick Start

```bash
cd E:\Hermes-Hub

# Run all agent tests
python -m pytest agents/sales_client_intake_agent/tests/ agents/malyarka_agent/tests/ agents/corel_export_agent/tests/ -v

# Run Sales → Malyarka integration
python -m pytest agents/local_simulation/sales_to_malyarka/test_sales_to_malyarka_integration.py -v

# Run full-chain simulation
python agents/local_simulation/full_chain_sales_malyarka_corel/run_full_chain_simulation.py
```

## Expected Results

- Sales: 48/48
- Malyarka: 28/28
- Corel: 18/18
- Integration: 12/12
- Full-chain: 12/12
- Total: 118 ✅

## What NOT to do

- Never touch server
- Never read secrets
- Never connect Telegram
- Never launch Corel
