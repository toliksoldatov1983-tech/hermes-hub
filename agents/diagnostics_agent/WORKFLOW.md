# Diagnostics Agent — Workflow

Date: 2026-06-17 | Status: `accepted`, not active

## Safe Checks (markdown-only)

1. Read registry → agent statuses
2. Check test reports → pass/fail counts
3. Check WORKLOG → last actions
4. Check STATE → current branches
5. Check blockers → LAUNCH_BLOCKERS.md
6. Generate safe report → SAFE_REPORT_TEMPLATE.md

## Forbidden

- Server/SSH
- Secrets/token/.env
- Live Telegram
- Real orders
- Network/API calls
