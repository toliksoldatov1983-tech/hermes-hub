"""Mobile Gateway — safe-local bridge between mobile clients and Hermes-Clean.

Uses existing Runtime Bridge — does NOT duplicate logic.

Architecture:
    Android / Web UI → Mobile Gateway → Runtime Bridge → Hermes-Clean modules
"""

from __future__ import annotations

from hermes_core.mobile_gateway.contract import (
    ALLOWED_ENDPOINTS,
    BLOCKED_ENDPOINTS,
    MobileAPIEndpoint,
    MobileAPIResponse,
)
from hermes_core.runtime_bridge import BridgeRouter, BridgeRequest, BridgeActionType
from hermes_core.runtime_bridge.contract import ROUTE_TO_ACTION


class MobileGateway:
    """Safe-local mobile gateway using Runtime Bridge.

    All mobile requests go through the bridge safety policy.
    No direct module access — everything is routed.
    """

    def __init__(self) -> None:
        self._bridge = BridgeRouter()

    def handle(self, endpoint: MobileAPIEndpoint, payload: dict | None = None) -> MobileAPIResponse:
        """Handle a mobile API request through the runtime bridge.

        Args:
            endpoint: The mobile API endpoint.
            payload: Optional payload (for POST endpoints).

        Returns:
            MobileAPIResponse with standardized JSON format.
        """
        payload = payload or {}

        # Blocked endpoints — never allowed
        if endpoint in BLOCKED_ENDPOINTS:
            return MobileAPIResponse.blocked(
                endpoint=endpoint.value,
                action=endpoint.name,
                reason=f"Endpoint '{endpoint.value}' is permanently blocked in safe-local mode.",
            )

        # Unknown endpoint — blocked (fail-safe)
        if endpoint not in ALLOWED_ENDPOINTS:
            return MobileAPIResponse.blocked(
                endpoint=str(endpoint),
                action="unknown",
                reason=f"Unknown endpoint. Allowed: {[e.value for e in ALLOWED_ENDPOINTS]}",
            )

        # Route through bridge
        return self._route(endpoint, payload)

    def _route(self, endpoint: MobileAPIEndpoint, payload: dict) -> MobileAPIResponse:
        """Route a mobile endpoint to the runtime bridge."""
        bridge_action = _ENDPOINT_TO_BRIDGE.get(endpoint)

        if bridge_action is None:
            return MobileAPIResponse.error(
                endpoint=endpoint.value,
                action=endpoint.name,
                message=f"No bridge action mapped for {endpoint.name}",
            )

        request = BridgeRequest(action=bridge_action, payload=payload)
        bridge_resp = self._bridge.handle(request)

        if bridge_resp.is_blocked:
            return MobileAPIResponse.blocked(
                endpoint=endpoint.value,
                action=endpoint.name,
                reason=bridge_resp.blocked_reason,
            )

        if bridge_resp.status == "ERROR":
            return MobileAPIResponse.error(
                endpoint=endpoint.value,
                action=endpoint.name,
                message=bridge_resp.blocked_reason or "Bridge routing error",
            )

        # Parse bridge output into structured data
        data = _parse_bridge_output(bridge_resp.output_lines)

        return MobileAPIResponse.ok(
            endpoint=endpoint.value,
            action=endpoint.name,
            data=data,
            next_step="Check 'what-next' for recommended actions.",
        )

    def status(self) -> MobileAPIResponse:
        """Get mobile gateway status."""
        return self.handle(MobileAPIEndpoint.STATUS)

    def dashboard(self) -> MobileAPIResponse:
        return self.handle(MobileAPIEndpoint.DASHBOARD)

    def daily_assistant(self) -> MobileAPIResponse:
        return self.handle(MobileAPIEndpoint.DAILY_ASSISTANT)

    def what_next(self) -> MobileAPIResponse:
        return self.handle(MobileAPIEndpoint.WHAT_NEXT)

    def local_health(self) -> MobileAPIResponse:
        return self.handle(MobileAPIEndpoint.LOCAL_HEALTH)

    def malyarka_status(self) -> MobileAPIResponse:
        return self.handle(MobileAPIEndpoint.MALYARKA_STATUS)

    def malyarka_dialog(self, script: str = "clean") -> MobileAPIResponse:
        return self.handle(MobileAPIEndpoint.MALYARKA_DIALOG, {"script": script})

    def ai_provider_status(self) -> MobileAPIResponse:
        return self.handle(MobileAPIEndpoint.AI_PROVIDER_STATUS)

    def bridge_status(self) -> MobileAPIResponse:
        return self.handle(MobileAPIEndpoint.BRIDGE_STATUS)

    def bridge_route(self, action: str) -> MobileAPIResponse:
        return self.handle(MobileAPIEndpoint.BRIDGE_ROUTE, {"action": action})


# ── Endpoint → BridgeAction mapping ──

_ENDPOINT_TO_BRIDGE: dict[MobileAPIEndpoint, BridgeActionType] = {
    MobileAPIEndpoint.STATUS: BridgeActionType.STATUS,
    MobileAPIEndpoint.DASHBOARD: BridgeActionType.DASHBOARD,
    MobileAPIEndpoint.DAILY_REPORT: BridgeActionType.DAILY_REPORT,
    MobileAPIEndpoint.DAILY_ASSISTANT: BridgeActionType.DAILY_ASSISTANT,
    MobileAPIEndpoint.WHAT_NEXT: BridgeActionType.WHAT_NEXT,
    MobileAPIEndpoint.LOCAL_HEALTH: BridgeActionType.LOCAL_HEALTH,
    MobileAPIEndpoint.MALYARKA_STATUS: BridgeActionType.MALYARKA_STATUS,
    MobileAPIEndpoint.MALYARKA_DIALOG: BridgeActionType.MALYARKA_DIALOG,
    MobileAPIEndpoint.AI_PROVIDER_STATUS: BridgeActionType.AI_PROVIDER_STATUS,
    MobileAPIEndpoint.BRIDGE_STATUS: BridgeActionType.STATUS,
    MobileAPIEndpoint.BRIDGE_ROUTE: BridgeActionType.STATUS,
}


# ── Output parsing ──


def _parse_bridge_output(lines: list[str]) -> dict[str, str]:
    """Parse bridge text output into key-value dict for JSON.

    Format: key=value or key: value
    """
    data: dict[str, str] = {}
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # key=value format
        if "=" in line:
            key, _, val = line.partition("=")
            data[key.strip()] = val.strip()
        # key: value format (dashboard, reports)
        elif ": " in line:
            key, _, val = line.partition(": ")
            data[key.strip()] = val.strip()
        else:
            # Plain line — store under "output_N"
            idx = len([k for k in data if k.startswith("output_")])
            data[f"output_{idx}"] = line
    return data
