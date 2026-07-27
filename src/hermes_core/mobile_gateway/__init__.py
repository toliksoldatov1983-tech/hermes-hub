"""Mobile Gateway — safe-local API for mobile clients.

Uses Runtime Bridge. 127.0.0.1 only.
"""

from hermes_core.mobile_gateway.contract import (
    ALLOWED_ENDPOINTS,
    BLOCKED_ENDPOINTS,
    MobileAPIEndpoint,
    MobileAPIResponse,
)
from hermes_core.mobile_gateway.gateway import MobileGateway
from hermes_core.mobile_gateway.local_api_server import LocalAPIServer

__all__ = [
    "ALLOWED_ENDPOINTS",
    "BLOCKED_ENDPOINTS",
    "LocalAPIServer",
    "MobileAPIEndpoint",
    "MobileAPIResponse",
    "MobileGateway",
]
