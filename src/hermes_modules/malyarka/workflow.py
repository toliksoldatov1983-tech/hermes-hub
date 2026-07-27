from __future__ import annotations

from dataclasses import dataclass

from hermes_modules.malyarka.dispute_contract import has_blocking_disputes
from hermes_modules.malyarka.export_contract import export_blocked_until_confirmed
from hermes_modules.malyarka.parser_contract import ParserContract
from hermes_modules.malyarka.resolution_contract import resolve_with_replacement


@dataclass(frozen=True)
class WorkflowStep:
    name: str
    status: str
    detail: str


@dataclass(frozen=True)
class MalyarkaWorkflow:
    steps: list[WorkflowStep]

    @property
    def final_status(self) -> str:
        return "READY_FOR_USER_REVIEW"


def build_synthetic_workflow() -> MalyarkaWorkflow:
    source = "paint 2 bucket"
    replacement = "paint | 2 | bucket"
    order = ParserContract().parse(source)
    resolution = resolve_with_replacement(source, replacement)
    steps = [
        WorkflowStep("parse", "OK", "Synthetic source parsed locally."),
        WorkflowStep(
            "preview",
            "DISPUTED" if has_blocking_disputes(order) else "READY",
            f"original_disputed_count={resolution.original_disputed_count}",
        ),
        WorkflowStep("disputes", "BLOCKING", "A disputed row blocks final action."),
        WorkflowStep(
            "resolution",
            "READY" if resolution.replacement_accepted else "DISPUTED",
            f"resolved_disputed_count={resolution.resolved_disputed_count}",
        ),
        WorkflowStep("export_gate", "BLOCKED", export_blocked_until_confirmed(None)),
        WorkflowStep("future_export", "GATED", resolution.export_status),
    ]
    return MalyarkaWorkflow(steps=steps)
