from __future__ import annotations

from dataclasses import dataclass

from hermes_modules.malyarka.order_contract import MalyarkaOrder


SYNTHETIC_PRICE_TABLE = {
    "wall paint": 100.0,
    "primer": 70.0,
    "roller": 15.0,
    "paint": 100.0,
}


@dataclass(frozen=True)
class SyntheticOrderMetadata:
    customer_label: str = "SYNTHETIC_CUSTOMER"
    order_reference: str = "SYNTHETIC_ORDER_001"


@dataclass(frozen=True)
class SyntheticPricedLine:
    item_name: str
    quantity: float
    unit: str
    unit_price: float
    line_total: float
    customer_label: str
    order_reference: str


@dataclass(frozen=True)
class SyntheticPricingPreview:
    lines: list[SyntheticPricedLine]
    total: float
    missing_prices: list[str]
    can_use_as_real_price: bool = False


def build_synthetic_pricing_preview(
    order: MalyarkaOrder,
    metadata: SyntheticOrderMetadata | None = None,
) -> SyntheticPricingPreview:
    metadata = metadata or SyntheticOrderMetadata()
    lines = []
    missing = []
    for row in order.confirmed_rows:
        price = SYNTHETIC_PRICE_TABLE.get(row.item_name.lower())
        if price is None:
            missing.append(row.item_name)
            continue
        quantity = float(row.quantity or 0)
        lines.append(
            SyntheticPricedLine(
                item_name=row.item_name,
                quantity=quantity,
                unit=row.unit,
                unit_price=price,
                line_total=quantity * price,
                customer_label=metadata.customer_label,
                order_reference=metadata.order_reference,
            )
        )
    return SyntheticPricingPreview(
        lines=lines,
        total=sum(line.line_total for line in lines),
        missing_prices=missing,
    )
