"""Runtime Bridge for Old Hermes → Hermes-Clean communication.

Safe-local only. All real/external actions blocked.
"""

from hermes_core.runtime_bridge.contract import (
    ALLOWED_SAFE_ACTIONS,
    ACTION_TO_ROUTE,
    BLOCKED_ACTIONS,
    BridgeActionType,
    BridgeRequest,
    BridgeResponse,
)
from hermes_core.runtime_bridge.router import BridgeRouter
from hermes_core.runtime_bridge.safety import BridgeSafetyPolicy, get_default_policy

__all__ = [
    "ALLOWED_SAFE_ACTIONS",
    "ACTION_TO_ROUTE",
    "BLOCKED_ACTIONS",
    "BridgeActionType",
    "BridgeRequest",
    "BridgeResponse",
    "BridgeRouter",
    "BridgeSafetyPolicy",
    "get_default_policy",
]
