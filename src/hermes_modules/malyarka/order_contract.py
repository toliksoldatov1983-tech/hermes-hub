from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class RowStatus(str, Enum):
    CONFIRMED = "CONFIRMED"
    DISPUTED = "DISPUTED"


@dataclass(frozen=True)
class MalyarkaOrderRow:
    raw_text: str
    item_name: str = ""
    quantity: float | None = None
    unit: str = ""
    status: RowStatus = RowStatus.DISPUTED
    dispute_reason: str = ""

    @property
    def is_confirmed(self) -> bool:
        return self.status is RowStatus.CONFIRMED


@dataclass(frozen=True)
class MalyarkaOrder:
    source_text: str
    rows: list[MalyarkaOrderRow] = field(default_factory=list)

    @property
    def confirmed_rows(self) -> list[MalyarkaOrderRow]:
        return [row for row in self.rows if row.status is RowStatus.CONFIRMED]

    @property
    def disputed_rows(self) -> list[MalyarkaOrderRow]:
        return [row for row in self.rows if row.status is RowStatus.DISPUTED]

    @property
    def final_ready(self) -> bool:
        return bool(self.rows) and not self.disputed_rows
