# Rollback & Backup Requirements

Date: 2026-06-17

## Offline Modules

| Module | Rollback |
|--------|----------|
| Sales agent | revert to last git / copy from archive |
| Malyarka agent | revert to last git / copy from archive |
| Corel Export | revert to last git / copy from archive |
| Simulation | regenerate from source agents |

## Rollback Procedure

1. Stop all running processes
2. Restore agent src/ from backup
3. Run regression suite (118 tests)
4. Confirm all pass → done
5. If fail → escalate

## Backup Policy

- All agent src/ — committed to git when ready (future)
- All docs/ — in markdown, self-documenting
- No secrets in backups
