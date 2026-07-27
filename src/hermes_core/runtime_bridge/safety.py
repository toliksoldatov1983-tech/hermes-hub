"""Runtime bridge safety policy — enforces safe-local only."""

from __future__ import annotations

from hermes_core.runtime_bridge.contract import (
    ALLOWED_SAFE_ACTIONS,
    BridgeActionType,
    BridgeRequest,
    BridgeResponse,
)


class BridgeSafetyPolicy:
    """Enforces safety policy for bridge requests.

    In safe-local mode:
      - Allowed actions: status, dashboard, daily-assistant, malyarka dry-run, etc.
      - Blocked actions: live Telegram, external API, Google Drive, real orders, deletes, secrets.
    """

    # Allow-list only
    ALLOWED = ALLOWED_SAFE_ACTIONS

    # Hard blocked — never allowed through bridge in any mode
    HARD_BLOCKED: frozenset[BridgeActionType] = frozenset({
        BridgeActionType.SECRET_READ,
        BridgeActionType.DELETE_OPERATION,
    })

    def check(self, request: BridgeRequest) -> BridgeResponse:
        """Check if a bridge request is allowed.

        Returns a blocking response if the action is not allowed,
        or None if the action is safe to proceed.
        """
        action = request.action

        # Hard blocked — never allowed
        if action in self.HARD_BLOCKED:
            return BridgeResponse.blocked_action(
                action.name,
                f"Action '{action.name}' is permanently blocked through the bridge.",
            )

        # Explicitly allowed
        if action in self.ALLOWED:
            return None  # Safe to proceed

        # Unknown action — blocked by default (fail-safe)
        return BridgeResponse.blocked_action(
            action.name,
            f"Action '{action.name}' is not in the safe-local allow-list. "
            f"Available actions: {sorted(a.name for a in self.ALLOWED)}",
        )

    def is_allowed(self, action: BridgeActionType) -> bool:
        return action in self.ALLOWED and action not in self.HARD_BLOCKED


# Singleton for convenient import
_default_policy = BridgeSafetyPolicy()


def get_default_policy() -> BridgeSafetyPolicy:
    return _default_policy
