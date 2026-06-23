"""Domain models for the first safe Malyarka core stage."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class OrderItem:
    """Confirmed order item with dimensions and optional separate properties."""

    height: int
    width: int
    quantity: int = 1
    item_type: str | None = None
    material: str | None = None
    thickness: str | None = None
    color: str | None = None
    coating: str | None = None
    milling_type: str | None = None
    milling_side: str | None = None
    painting_side: str | None = None
    edge_processing: str | None = None
    group: str | None = None
    subgroup: str | None = None
    status: str | None = None
    note: str | None = None
    source: str | None = None
    confidence: float | None = None


@dataclass(slots=True)
class DisputedItem:
    """Line that cannot be safely treated as a confirmed item."""

    raw: str
    reason: str
    note: str | None = None
    source: str | None = None
    confidence: float | None = None


@dataclass(slots=True)
class OrderDraft:
    """Draft order containing confirmed and disputed items."""

    items: list[OrderItem] = field(default_factory=list)
    disputed_items: list[DisputedItem] = field(default_factory=list)
