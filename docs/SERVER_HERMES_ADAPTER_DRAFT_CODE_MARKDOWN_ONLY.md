# Server Hermes Adapter — Draft Code (Markdown Only)

Date: 2026-06-17 | DO NOT create .py file

## Proposed file: `malyarka_core/adapters/hermes_adapter.py`

```python
"""
Hermes safety adapter for dry-run order validation.
No Telegram API. No secrets. No server writes. No DB access.
"""

from typing import Any, Dict

# === Config ===
_HERMES_DRY_RUN = True  # always true, off-by-default via parent flag


# Block patterns (safe, no regex injection possible)
UNSAFE_PATTERNS = [
    "BOT_TOKEN", "token=", "API_KEY", "secret",
    "config.py", ".env", "os.environ",
]

FORBIDDEN_ACTIONS = [
    "production", "export", "corel", "server",
    "ssh", "/opt", "производство", "отправь",
    "финальный", "final",
]


def check_hermes_safety(text: str) -> Dict[str, Any]:
    """Safety check. Deterministic, no side effects, no secrets access."""

    result = {
        "adapter_mode": "dry_run",
        "dry_run": True,
        "source": "telegram",
        "telegram_api_called": False,
        "server_called": False,
        "side_effects": [],
        "blocked": False,
        "block_reason": None,
        "review_required": True,  # conservative default
        "production_ready": False,
        "fallback_required": False,
    }

    # Guard: malformed input
    if not isinstance(text, str):
        result["blocked"] = True
        result["block_reason"] = "malformed_event"
        return result

    clean = text.strip()

    # Empty
    if not clean:
        result["blocked"] = True
        result["block_reason"] = "empty_message"
        return result

    # Commands
    if clean.startswith("/"):
        result["blocked"] = True
        result["block_reason"] = "command_not_routed_yet"
        return result

    # Unsafe patterns
    for pattern in UNSAFE_PATTERNS:
        if pattern in clean:
            result["blocked"] = True
            result["block_reason"] = "unsafe_secret_like_input"
            return result

    # Forbidden actions
    lower = clean.lower()
    for action in FORBIDDEN_ACTIONS:
        if action in lower:
            result["blocked"] = True
            result["block_reason"] = "forbidden_action"
            return result

    # Passed all checks
    result["blocked"] = False
    result["review_required"] = False
    return result
```

## Safety Invariants

- No imports beyond `typing`
- No network/API calls
- No file access
- No env/secrets reads
- Deterministic output
- `production_ready` always False
