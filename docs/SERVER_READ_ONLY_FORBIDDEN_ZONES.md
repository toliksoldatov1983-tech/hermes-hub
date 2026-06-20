# Server Read-Only Forbidden Zones

Date: 2026-06-17 | RED gate

| Zone | Why |
|------|-----|
| token | NEVER read |
| .env | NEVER read |
| config.py contents | NEVER read |
| os.environ | NEVER read |
| database files | orders.db, user data |
| live logs with order contents | Real order data |
| orders.db | Production DB |
| secrets | Private keys, passwords |
| Telegram API | LIVE — never touch |
| polling/webhook | LIVE — never touch |
| systemctl restart/start/stop | Service control |
| git add/commit/push/pull | Write to repo |
| patch/apply | Write to files |
| production/staging code | Write to code |
| real order contents | Production data |
| Corel/ArtCAM/CNC files | Production files |

## Rule

If a file might contain secrets, orders, or live data → STOP.
Check whitelist BEFORE reading.
