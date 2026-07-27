"""Phone Connectivity — pairing contract & connectivity policy for mobile access.

All dry-run/mock by default. Real access requires approval gates.
"""

from hermes_core.phone_connectivity.connectivity_policy import (
    CONNECTIVITY_OPTIONS,
    ConnectivityMode,
    ConnectivityOption,
    PhoneConnectivityPolicy,
    get_default_policy,
)
from hermes_core.phone_connectivity.pairing_contract import (
    ConnectionStatus,
    ConnectivityTier,
    DevicePairing,
    PairingMode,
)

__all__ = [
    "CONNECTIVITY_OPTIONS",
    "ConnectionStatus",
    "ConnectivityMode",
    "ConnectivityOption",
    "ConnectivityTier",
    "DevicePairing",
    "PairingMode",
    "PhoneConnectivityPolicy",
    "get_default_policy",
]
