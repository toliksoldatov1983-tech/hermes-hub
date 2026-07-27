from __future__ import annotations

from hermes_core.safety.safety_gate import SafetyGate
from hermes_core.types import ActionDecision, HermesResponse, PlannedAction, UserRequest


class HermesRouter:
    def __init__(self, safety_gate: SafetyGate | None = None) -> None:
        self.safety_gate = safety_gate or SafetyGate()

    def plan(self, request: UserRequest) -> list[PlannedAction]:
        text = request.text.lower()
        if "удали" in text or "delete" in text:
            return [PlannedAction("delete", "Delete request blocked by policy.")]
        if "telegram live" in text or "live telegram" in text:
            return [PlannedAction("telegram_live", "Live Telegram needs approval.")]
        if "drive move" in text or "перенеси drive" in text:
            return [PlannedAction("drive_move_without_approval", "Google Drive move needs approval.")]
        return [PlannedAction("answer_text", "Prepare a local text response.")]

    def handle(self, request: UserRequest, approved: bool = False) -> HermesResponse:
        actions = self.plan(request)
        decision = self.safety_gate.block_if_needed(actions, approved=approved)
        warnings = []
        if decision is not ActionDecision.SAFE:
            warnings.append("Action requires approval or is blocked by policy.")
        return HermesResponse(
            text="Hermes-Clean planned the request safely.",
            decision=decision,
            planned_actions=actions,
            warnings=warnings,
            next_step="Review approval gate." if warnings else "Proceed with safe local work.",
        )
