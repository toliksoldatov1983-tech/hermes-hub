# Sales → Malyarka Local Simulation

Date: 2026-06-17
Status: yellow-approved integration test (offline only)

## Chain

```text
Fake Client Message → Sales Agent → Intake Card → Handoff Check → Malyarka Agent → Preliminary Result
```

## What This Is

Local simulation connecting two existing offline modules WITHOUT modifying them.
No Telegram. No API. No server. No live. No real orders.

## Files

| File | Purpose |
|------|---------|
| `FAKE_CLIENT_MESSAGES.md` | 10 fake messages |
| `SIMULATION_OUTPUTS.md` | Expected outputs |
| `run_simulation.py` | Runner |
| `test_sales_to_malyarka_integration.py` | Integration tests |
| `README.md` | This file |
