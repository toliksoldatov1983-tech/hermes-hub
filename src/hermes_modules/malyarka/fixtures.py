from __future__ import annotations

from dataclasses import dataclass

from hermes_modules.malyarka.dispute_contract import dispute_summary
from hermes_modules.malyarka.export_contract import export_blocked_until_confirmed
from hermes_modules.malyarka.parser_contract import ParserContract
from hermes_modules.malyarka.preview_contract import build_preview


@dataclass(frozen=True)
class MalyarkaFixture:
    name: str
    source_text: str
    expected_final_ready: bool
    purpose: str


@dataclass(frozen=True)
class MalyarkaFixtureResult:
    name: str
    confirmed_count: int
    disputed_count: int
    final_ready: bool
    export_status: str
    disputes: list[str]


SYNTHETIC_FIXTURES = [
    MalyarkaFixture("ready_single_line", "wall paint | 2 | bucket", True, "One valid synthetic order row."),
    MalyarkaFixture("ready_multi_line", "primer | 1 | bucket\nroller | 3 | piece", True, "Two valid synthetic rows."),
    MalyarkaFixture("missing_separator", "paint 2 bucket", False, "Dispute when row does not use item | quantity | unit."),
    MalyarkaFixture("bad_quantity", "paint | many | bucket", False, "Dispute when quantity is not numeric."),
    MalyarkaFixture("negative_quantity", "paint | -1 | bucket", False, "Dispute when quantity is not positive."),
    MalyarkaFixture("unknown_price_ready", "custom coating | 1 | bucket", True, "Ready row with no synthetic price."),
    MalyarkaFixture("empty_item", " | 1 | bucket", False, "Dispute when item name is empty."),
    MalyarkaFixture("empty_unit", "paint | 1 | ", False, "Dispute when unit is empty."),
    MalyarkaFixture("mixed_valid_and_disputed", "paint | 1 | bucket\nbroken row", False, "Mixed order blocks final readiness."),
    MalyarkaFixture("zero_quantity", "paint | 0 | bucket", False, "Dispute when quantity is zero."),
    MalyarkaFixture("malformed_extra_field", "paint | 1 | bucket | extra", False, "Dispute when row has too many fields."),
    MalyarkaFixture("manual_ready_unknown_unit", "sealant | 2 | cartridge", True, "Ready synthetic row with a unit not in pricing."),
]


def fixture_names() -> list[str]:
    return [fixture.name for fixture in SYNTHETIC_FIXTURES]


def run_fixture(fixture: MalyarkaFixture) -> MalyarkaFixtureResult:
    order = ParserContract().parse(fixture.source_text)
    preview = build_preview(order)
    return MalyarkaFixtureResult(
        name=fixture.name,
        confirmed_count=int(preview["confirmed_count"]),
        disputed_count=int(preview["disputed_count"]),
        final_ready=bool(preview["final_ready"]),
        export_status=export_blocked_until_confirmed(order, approved=True),
        disputes=dispute_summary(order),
    )


def run_all_fixtures() -> list[MalyarkaFixtureResult]:
    return [run_fixture(fixture) for fixture in SYNTHETIC_FIXTURES]
