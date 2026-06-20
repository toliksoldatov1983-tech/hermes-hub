# Block Reasons

Date: 2026-06-17 | Gate 3

| # | Reason | When |
|---|--------|------|
| 1 | `empty_message` | text="" and no photo |
| 2 | `unsafe_secret_like_input` | contains token, env, secret patterns |
| 3 | `production_action_blocked` | содержит "производство", "production" |
| 4 | `forbidden_action` | admin/export/server/corel patterns |
| 5 | `photo_not_supported_in_fake_adapter` | has_photo=true, no text |
| 6 | `command_not_routed_yet` | starts with "/" |
| 7 | `unsafe_diagnostics_request` | server/SSH diagnostics attempt |
| 8 | `missing_required_fields` | no sizes/material/color (after Sales) |
| 9 | `disputed_order_field` | milling without type (after Sales) |
| 10 | `manager_review_required` | discount/tech_advice (after Sales) |
| 11 | `safe_failure` | unexpected, no production |

## Priority

Adapter-level blocks (1-7) stop before Sales. Sales-level blocks (8-10) stop before Malyarka/Corel.
