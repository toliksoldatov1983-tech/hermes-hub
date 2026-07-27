from __future__ import annotations

from dataclasses import dataclass

from hermes_modules.malyarka.export_contract import export_blocked_until_confirmed
from hermes_modules.malyarka.order_contract import MalyarkaOrder
from hermes_modules.malyarka.parser_contract import ParserContract
from hermes_modules.malyarka.preview_contract import build_preview


@dataclass(frozen=True)
class ResolutionResult:
    original_final_ready: bool
    resolved_final_ready: bool
    original_disputed_count: int
    resolved_disputed_count: int
    replacement_accepted: bool
    export_status: str


def resolve_with_replacement(source_text: str, replacement_text: str) -> ResolutionResult:
    parser = ParserContract()
    original = parser.parse(source_text)
    replacement = parser.parse(replacement_text)
    resolved = _merge_first_dispute(original, replacement)
    original_preview = build_preview(original)
    resolved_preview = build_preview(resolved)
    replacement_accepted = bool(replacement.final_ready and original.disputed_rows)
    return ResolutionResult(
        original_final_ready=bool(original_preview["final_ready"]),
        resolved_final_ready=bool(resolved_preview["final_ready"]),
        original_disputed_count=int(original_preview["disputed_count"]),
        resolved_disputed_count=int(resolved_preview["disputed_count"]),
        replacement_accepted=replacement_accepted,
        export_status=export_blocked_until_confirmed(resolved, approved=False),
    )


def _merge_first_dispute(original: MalyarkaOrder, replacement: MalyarkaOrder) -> MalyarkaOrder:
    if not original.disputed_rows or not replacement.final_ready:
        return original
    replacement_row = replacement.confirmed_rows[0]
    rows = []
    replaced = False
    for row in original.rows:
        if not replaced and row in original.disputed_rows:
            rows.append(replacement_row)
            replaced = True
        else:
            rows.append(row)
    return MalyarkaOrder(source_text=original.source_text, rows=rows)
