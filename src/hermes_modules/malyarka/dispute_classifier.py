from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from hermes_modules.malyarka.fixtures import run_all_fixtures
from hermes_modules.malyarka.order_contract import MalyarkaOrder, MalyarkaOrderRow


@dataclass(frozen=True)
class DisputeClassification:
    raw_text: str
    reason: str
    category: str
    severity: str
    blocks_final: bool
    recommended_action: str


@dataclass(frozen=True)
class DisputeClassificationSummary:
    total_disputes: int
    categories: dict[str, int]
    severities: dict[str, int]
    blocks_final: bool
    classifications: list[DisputeClassification]


@dataclass(frozen=True)
class DisputeReportResult:
    path: Path
    total_disputes: int
    categories_count: int


def classify_disputed_row(row: MalyarkaOrderRow) -> DisputeClassification:
    reason = row.dispute_reason.strip()
    lowered = reason.lower()

    if "expected format" in lowered:
        category = "FORMAT_ERROR"
        severity = "HIGH"
        action = "Ask user to rewrite the row as item | quantity | unit."
    elif "item name" in lowered:
        category = "MISSING_ITEM"
        severity = "HIGH"
        action = "Ask user to provide the missing item name."
    elif "not numeric" in lowered:
        category = "INVALID_QUANTITY"
        severity = "HIGH"
        action = "Ask user to replace quantity with a number."
    elif "positive" in lowered:
        category = "INVALID_QUANTITY"
        severity = "HIGH"
        action = "Ask user to provide a positive quantity."
    elif "unit" in lowered:
        category = "MISSING_UNIT"
        severity = "MEDIUM"
        action = "Ask user to provide the unit."
    else:
        category = "UNKNOWN_DISPUTE"
        severity = "HIGH"
        action = "Ask user to inspect the row manually before any export."

    return DisputeClassification(
        raw_text=row.raw_text,
        reason=reason,
        category=category,
        severity=severity,
        blocks_final=True,
        recommended_action=action,
    )


def classify_order_disputes(order: MalyarkaOrder) -> DisputeClassificationSummary:
    classifications = [classify_disputed_row(row) for row in order.disputed_rows]
    categories: dict[str, int] = {}
    severities: dict[str, int] = {}
    for classification in classifications:
        categories[classification.category] = categories.get(classification.category, 0) + 1
        severities[classification.severity] = severities.get(classification.severity, 0) + 1

    return DisputeClassificationSummary(
        total_disputes=len(classifications),
        categories=categories,
        severities=severities,
        blocks_final=bool(classifications),
        classifications=classifications,
    )


def build_fixture_dispute_summary() -> DisputeClassificationSummary:
    categories: dict[str, int] = {}
    severities: dict[str, int] = {}
    classifications: list[DisputeClassification] = []

    for fixture in run_all_fixtures():
        for dispute in fixture.disputes:
            raw_text, _, reason = dispute.partition(": ")
            pseudo_row = MalyarkaOrderRow(raw_text=raw_text, dispute_reason=reason)
            classification = classify_disputed_row(pseudo_row)
            classifications.append(classification)
            categories[classification.category] = categories.get(classification.category, 0) + 1
            severities[classification.severity] = severities.get(classification.severity, 0) + 1

    return DisputeClassificationSummary(
        total_disputes=len(classifications),
        categories=categories,
        severities=severities,
        blocks_final=bool(classifications),
        classifications=classifications,
    )


class MalyarkaDisputeClassificationReport:
    def __init__(self, project_root: Path | str) -> None:
        self.project_root = Path(project_root).resolve()

    def write(self) -> DisputeReportResult:
        summary = build_fixture_dispute_summary()
        report_path = self.project_root / "05_REPORTS" / "MALYARKA_DISPUTE_CLASSIFICATION_REPORT.md"
        lines = [
            "# Malyarka Dispute Classification Report",
            "",
            "## Scope",
            "",
            "This report uses only synthetic fixtures inside Hermes-Clean.",
            "No real orders, client documents, old archives, Google Drive files, secrets, tokens or `.env` files were read.",
            "",
            "## Summary",
            "",
            f"- total_disputes: {summary.total_disputes}",
            f"- blocks_final: {summary.blocks_final}",
            "",
            "## Categories",
            "",
        ]
        for category, count in sorted(summary.categories.items()):
            lines.append(f"- {category}: {count}")

        lines.extend(["", "## Severities", ""])
        for severity, count in sorted(summary.severities.items()):
            lines.append(f"- {severity}: {count}")

        lines.extend(["", "## Disputed Rows", ""])
        for classification in summary.classifications:
            lines.append(
                f"- category={classification.category}; severity={classification.severity}; "
                f"raw={classification.raw_text}; action={classification.recommended_action}"
            )

        lines.extend(
            [
                "",
                "## Rule",
                "",
                "Any disputed row blocks final export until the user confirms or fixes it.",
            ]
        )
        report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return DisputeReportResult(
            path=report_path,
            total_disputes=summary.total_disputes,
            categories_count=len(summary.categories),
        )
