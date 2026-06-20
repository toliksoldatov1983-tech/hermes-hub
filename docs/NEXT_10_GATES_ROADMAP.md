# Next 10 Gates Roadmap

Date: 2026-06-17

| # | Gate | Color | Description |
|---|------|-------|-------------|
| 1 | SERVER_READ_ONLY_GATE_1 | RED | Architecture verification |
| 2 | SERVER_READ_ONLY_GATE_2 | RED/YELLOW | Safe file review whitelist |
| 3 | SERVER_ADAPTER_GATE_3 | YELLOW | Dry-run patch plan (no code) |
| 4 | SERVER_ADAPTER_GATE_4 | YELLOW | Rollback/backup plan |
| 5 | SERVER_ADAPTER_GATE_5 | YELLOW | Staging patch plan (no apply) |
| 6 | SERVER_ADAPTER_GATE_6 | YELLOW | Local staging tests |
| 7 | SERVER_ADAPTER_GATE_7 | YELLOW | Feature flag off-by-default |
| 8 | SERVER_ADAPTER_GATE_8 | YELLOW | Controlled dry-run |
| 9 | TELEGRAM_LIVE_GATE_9 | RED | Limited test only |
| 10 | PRODUCTION_GATE_10 | RED | Separate approval |

## Key

- RED = requires explicit user approval
- YELLOW = requires approval, but limited scope
- GREEN = autonomous within limits
