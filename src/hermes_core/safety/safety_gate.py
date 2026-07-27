from __future__ import annotations

from hermes_core.safety.action_policy import classify_action
from hermes_core.types import ActionDecision, PlannedAction


class SafetyGate:
    """Classifies planned actions before execution."""

    def evaluate(self, action: PlannedAction, approved: bool = False) -> ActionDecision:
        return classify_action(action.action_type, approved=approved).decision

    def explain(self, action: PlannedAction, approved: bool = False) -> str:
        return classify_action(action.action_type, approved=approved).reason

    def block_if_needed(self, actions: list[PlannedAction], approved: bool = False) -> ActionDecision:
        decisions = [self.evaluate(action, approved=approved) for action in actions]
        if ActionDecision.BLOCKED in decisions:
            return ActionDecision.BLOCKED
        if ActionDecision.CONFIRM_REQUIRED in decisions:
            return ActionDecision.CONFIRM_REQUIRED
        return ActionDecision.SAFE
