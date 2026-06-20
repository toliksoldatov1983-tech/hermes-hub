# Server Adapter Precheck Checklist

Date: 2026-06-17 | Before any patch

- [ ] SSH access confirmed (root via temp key)
- [ ] Server path `/opt/malyarka-telegram-bot` exists
- [ ] `adapters/telegram.py` exists (original)
- [ ] Backup created and verified
- [ ] No live bot restart planned
- [ ] No systemctl operations
- [ ] No git dirty state on server
- [ ] No secrets read (token, .env, config.py)
- [ ] Feature flag `_HERMES_ADAPTER_ENABLED = False`
- [ ] dry_run always true in plan
- [ ] production_ready always false in plan
- [ ] User explicitly approved backup + patch
- [ ] Rollback plan ready and verified
