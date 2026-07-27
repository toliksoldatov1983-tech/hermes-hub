from __future__ import annotations

from dataclasses import dataclass

from hermes_modules.malyarka.fixtures import run_all_fixtures
from hermes_modules.malyarka.schema_contract import export_preview_columns
from hermes_modules.malyarka.workflow import build_synthetic_workflow


@dataclass(frozen=True)
class MalyarkaDemo:
    fixtures_count: int
    ready_fixtures: int
    disputed_fixtures: int
    workflow_status: str
    export_columns: list[str]
    export_gated: bool


def build_demo() -> MalyarkaDemo:
    fixtures = run_all_fixtures()
    workflow = build_synthetic_workflow()
    return MalyarkaDemo(
        fixtures_count=len(fixtures),
        ready_fixtures=sum(1 for fixture in fixtures if fixture.final_ready),
        disputed_fixtures=sum(1 for fixture in fixtures if fixture.disputed_count > 0),
        workflow_status=workflow.final_status,
        export_columns=export_preview_columns(),
        export_gated=True,
    )
