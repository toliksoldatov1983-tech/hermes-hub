# Local to Server Adapter Mapping

Date: 2026-06-17

| Local (E:\Hermes-Hub) | Future Server (/opt/...) |
|-----------------------|--------------------------|
| `fake_telegram_adapter.py` | Server adapter layer |
| `fake_full_chain_simulation.py` | Server dry-run simulation |
| Sales Agent | Intake classification layer |
| Malyarka Agent | Preliminary order analysis |
| Corel Export Agent | Contract only, not production |
| Safety invariants | Feature flags, dry-run, off-by-default |
| Failure matrix | Server blocking rules |
| Block reasons | Production action prevention |
| adapter_mode="fake" | adapter_mode="dry-run" (future) |
| production_ready=false | production_ready=false |
| 145 tests local | Future server regression |

## Key Insight

Local fake adapter already implements the contract that the server adapter must follow:
- Validate input before processing
- Block unsafe/production actions
- Never call Telegram API
- Never touch secrets
- Always dry-run until approved
