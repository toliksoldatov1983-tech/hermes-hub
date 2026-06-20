# Server Adapter Postcheck Checklist

Date: 2026-06-17 | After patch, before restart

- [ ] `hermes_adapter.py` imports without errors
- [ ] `adapters/telegram.py` syntax OK
- [ ] Feature flag `_HERMES_ADAPTER_ENABLED = False` confirmed
- [ ] Original preview path still works (flag off)
- [ ] Fallback path: no crashes on malformed input
- [ ] dry-run output only (no side effects)
- [ ] No Telegram API calls in adapter
- [ ] No DB/log/order reads in adapter
- [ ] No export/admin/write side effects
- [ ] production_ready false in all outputs
- [ ] Backup restorable (verified restore test)
- [ ] No live bot restart yet
