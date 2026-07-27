from __future__ import annotations

from dataclasses import dataclass

from hermes_modules.malyarka.order_contract import MalyarkaOrder, MalyarkaOrderRow, RowStatus


@dataclass(frozen=True)
class ValidationIssue:
    row_number: int
    raw_text: str
    code: str
    message: str
    blocks_final: bool = True


@dataclass(frozen=True)
class MalyarkaValidationResult:
    valid: bool
    blocked: bool
    confirmed_count: int
    disputed_count: int
    issues: list[ValidationIssue]

    @property
    def summary(self) -> str:
        if self.valid:
            return "valid"
        return "; ".join(f"{issue.code}:{issue.row_number}" for issue in self.issues)


def validate_order(order: MalyarkaOrder) -> MalyarkaValidationResult:
    issues: list[ValidationIssue] = []
    if not order.rows:
        issues.append(
            ValidationIssue(
                row_number=0,
                raw_text="",
                code="empty_order",
                message="Order must contain at least one synthetic row.",
            )
        )

    for index, row in enumerate(order.rows, start=1):
        issues.extend(validate_row(row, row_number=index))

    return MalyarkaValidationResult(
        valid=not issues,
        blocked=bool(issues),
        confirmed_count=len(order.confirmed_rows),
        disputed_count=len(order.disputed_rows),
        issues=issues,
    )


def validate_row(row: MalyarkaOrderRow, *, row_number: int = 1) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    reason = row.dispute_reason.strip()

    if row.status is RowStatus.DISPUTED:
        issues.append(
            ValidationIssue(
                row_number=row_number,
                raw_text=row.raw_text,
                code=_issue_code_from_reason(reason),
                message=reason or "Row is disputed.",
            )
        )
        return issues

    if not row.item_name.strip():
        issues.append(_issue(row, row_number, "missing_item", "Item name is required."))
    if row.quantity is None:
        issues.append(_issue(row, row_number, "missing_quantity", "Quantity is required."))
    elif row.quantity <= 0:
        issues.append(_issue(row, row_number, "invalid_quantity", "Quantity must be positive."))
    if not row.unit.strip():
        issues.append(_issue(row, row_number, "missing_unit", "Unit is required."))

    return issues


def _issue(row: MalyarkaOrderRow, row_number: int, code: str, message: str) -> ValidationIssue:
    return ValidationIssue(row_number=row_number, raw_text=row.raw_text, code=code, message=message)


def _issue_code_from_reason(reason: str) -> str:
    lowered = reason.lower()
    if "expected format" in lowered:
        return "malformed_row"
    if "item name" in lowered:
        return "missing_item"
    if "not numeric" in lowered:
        return "invalid_quantity"
    if "positive" in lowered:
        return "invalid_quantity"
    if "unit" in lowered:
        return "missing_unit"
    return "disputed_row"
