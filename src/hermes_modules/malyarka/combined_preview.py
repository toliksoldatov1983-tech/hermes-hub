from __future__ import annotations

from dataclasses import dataclass

from hermes_modules.malyarka.dispute_classifier import DisputeClassification, classify_order_disputes
from hermes_modules.malyarka.export_contract import export_blocked_until_confirmed
from hermes_modules.malyarka.parser_contract import ParserContract
from hermes_modules.malyarka.preview_contract import build_preview
from hermes_modules.malyarka.synthetic_pricing import SyntheticPricingPreview, build_synthetic_pricing_preview


DEFAULT_SYNTHETIC_ORDER = "wall paint | 2 | bucket\nroller | 3 | piece\nbroken row"


@dataclass(frozen=True)
class MalyarkaCombinedPreview:
    source_mode: str
    confirmed_count: int
    disputed_count: int
    final_ready: bool
    export_status: str
    dispute_categories: dict[str, int]
    dispute_classifications: list[DisputeClassification]
    pricing: SyntheticPricingPreview
    can_write_file: bool = False
    can_use_as_real_order: bool = False


def build_combined_preview(source_text: str | None = None) -> MalyarkaCombinedPreview:
    source_mode = "provided_text" if source_text and source_text.strip() else "default_synthetic"
    text = source_text.strip() if source_text and source_text.strip() else DEFAULT_SYNTHETIC_ORDER
    order = ParserContract().parse(text)
    preview = build_preview(order)
    disputes = classify_order_disputes(order)
    pricing = build_synthetic_pricing_preview(order)
    return MalyarkaCombinedPreview(
        source_mode=source_mode,
        confirmed_count=int(preview["confirmed_count"]),
        disputed_count=int(preview["disputed_count"]),
        final_ready=bool(preview["final_ready"]),
        export_status=export_blocked_until_confirmed(order),
        dispute_categories=disputes.categories,
        dispute_classifications=disputes.classifications,
        pricing=pricing,
    )
