# Server Adapter — Forbidden Next Actions

Date: 2026-06-18

| Action | Gate |
|--------|------|
| Enable feature flag | RED |
| Live restart without approval | RED |
| Read .env/token/config.py | RED |
| Read DB/log/order contents | RED |
| Touch real orders | RED |
| Git/patch/apply | RED |
| Production enable | RED |
| systemctl without approval | RED |
