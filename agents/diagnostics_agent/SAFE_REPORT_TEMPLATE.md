# Diagnostics Agent — SAFE REPORT TEMPLATE

Date: 2026-06-17 | Status: `accepted`, not active

```yaml
diagnostics_report:
  timestamp: "2026-06-17T..."
  safe_only: true
  secrets_read: false
  server_touched: false

  agents:
    - name: "Sales + Client Intake"
      status: "accepted"
      tests: "48/48"
      active: false
    - name: "Malyarka"
      status: "accepted"
      tests: "28/28"
      active: false
    - name: "Corel Export"
      status: "accepted"
      tests: null
      active: false

  chain:
    sales_to_malyarka: "verified (12/12)"
    malyarka_to_corel: "not implemented"

  branches:
    server_patch: "paused (STOP_APPROVAL #9)"
    agent_factory: "active (4 passes, 40+/40)"

  warnings: []
  blockers: []
```
