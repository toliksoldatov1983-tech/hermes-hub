from __future__ import annotations

from hermes_modules.malyarka.order_contract import MalyarkaOrder, MalyarkaOrderRow, RowStatus


class ParserContract:
    def parse(self, source_text: str) -> MalyarkaOrder:
        rows = [self._parse_line(line) for line in source_text.splitlines() if line.strip()]
        if not rows and source_text.strip():
            rows = [self._parse_line(source_text.strip())]
        return MalyarkaOrder(source_text=source_text, rows=rows)

    def _parse_line(self, line: str) -> MalyarkaOrderRow:
        raw = line.strip()
        parts = [part.strip() for part in raw.replace(";", "|").split("|")]
        if len(parts) != 3:
            return MalyarkaOrderRow(raw_text=raw, dispute_reason="Expected format: item | quantity | unit.")

        item_name, quantity_text, unit = parts
        if not item_name:
            return MalyarkaOrderRow(raw_text=raw, unit=unit, dispute_reason="Missing item name.")

        try:
            quantity = float(quantity_text.replace(",", "."))
        except ValueError:
            return MalyarkaOrderRow(raw_text=raw, item_name=item_name, unit=unit, dispute_reason="Quantity is not numeric.")

        if quantity <= 0:
            return MalyarkaOrderRow(raw_text=raw, item_name=item_name, quantity=quantity, unit=unit, dispute_reason="Quantity must be positive.")
        if not unit:
            return MalyarkaOrderRow(raw_text=raw, item_name=item_name, quantity=quantity, dispute_reason="Missing unit.")

        return MalyarkaOrderRow(raw_text=raw, item_name=item_name, quantity=quantity, unit=unit, status=RowStatus.CONFIRMED)
