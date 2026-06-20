# Server Safe File Review Map

Date: 2026-06-17

## Architecture Flow

```text
Telegram Message
    │
    ▼
handlers.py::handle_text_message
    │  _looks_like_order(text)?
    │  dangerous_words check ✅
    ▼
adapters/telegram.py::build_order_preview_from_text
    │  parses text, builds OrderDraft
    │  calculates area, validates
    ▼
services/orders.py::build_order_from_text
    │  delegates to parsing.py
    ▼
parsing.py::parse_sizes_text
    │  returns OrderDraft(items, disputed_items)
    ▼
exports/corel.py::build_corel_rows
    exports/corel.py::export_corel_xlsx
```

## Local → Server Mapping

| Local (Hermes Hub) | Server (/opt/...) |
|---------------------|-------------------|
| `fake_telegram_adapter.py` | `adapters/telegram.py` |
| `intake_agent.py` (Sales) | `handlers.py` (intent+dispatch) |
| `malyarka_agent.py` | `adapters/telegram.py` + `services/orders.py` |
| `corel_export_agent.py` | `exports/corel.py` |

## Hermes Insertion Point

`adapters/telegram.py::build_order_preview_from_text(text)` — wrap with Hermes safety layer:

```python
def build_order_preview_from_text(text):
    hermes_result = hermes_adapter.process(text)  # NEW
    if hermes_result.blocked:
        return hermes_result.block_message        # NEW
    # ... existing logic
```
