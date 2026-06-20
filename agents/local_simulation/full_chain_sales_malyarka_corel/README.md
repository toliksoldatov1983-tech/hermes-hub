# Full-Chain Simulation: Sales → Malyarka → Corel Export

Date: 2026-06-17 | Active agents: 0

## Chain

```text
Fake Message → Sales Agent → Intake Card → Malyarka Agent → Preliminary Result → Corel Export Agent → Export Contract
```

## Rules

- Only `ready_for_malyarka_agent=true` cards reach Malyarka
- Only `ready_for_human_review` + `export_blocked=false` reach Corel
- Corel rows: height_mm, width_mm, quantity
- Always `not_final_order=true`, `not_final_export=true`
