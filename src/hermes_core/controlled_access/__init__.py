"""Controlled Access — safe phone access layer.

Architecture:
    Android Shell → Mobile Web UI → Mobile Gateway
    → Runtime Bridge → Hermes-Clean modules

All real access blocked by default.
Tailscale/LAN require approval gates.
"""

from hermes_core.controlled_access.access_policy import (
    AccessDecision,
    AccessDecisionResult,
    AccessPolicy,
    AccessRequest,
    ClientType,
    get_access_policy,
)
from hermes_core.controlled_access.bind_mode import (
    BIND_MODE_POLICY,
    TAILSCALE_RECOMMENDATION,
    BindConfig,
    BindMode,
    classify_host,
    get_bind_config,
)
from hermes_core.controlled_access.tailscale_readiness import (
    TailscaleStatus,
    detect_tailscale,
    get_tailscale_access_plan,
)

__all__ = [
    "AccessDecision",
    "AccessDecisionResult",
    "AccessPolicy",
    "AccessRequest",
    "BIND_MODE_POLICY",
    "BindConfig",
    "BindMode",
    "ClientType",
    "TAILSCALE_RECOMMENDATION",
    "TailscaleStatus",
    "classify_host",
    "detect_tailscale",
    "get_access_policy",
    "get_bind_config",
    "get_tailscale_access_plan",
]
