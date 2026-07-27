from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SchemaField:
    name: str
    type_name: str
    required: bool
    description: str


ORDER_SCHEMA = [
    SchemaField("item_name", "string", True, "Synthetic item or service name."),
    SchemaField("quantity", "number", True, "Positive numeric quantity."),
    SchemaField("unit", "string", True, "Measurement unit."),
    SchemaField("unit_price", "number", False, "Synthetic unit price for dry-run calculations only."),
    SchemaField("line_total", "number", False, "Synthetic quantity * unit_price result."),
    SchemaField("customer_label", "string", False, "Synthetic customer label, never a real client name."),
    SchemaField("order_reference", "string", False, "Synthetic local order reference."),
    SchemaField("row_status", "CONFIRMED|DISPUTED", True, "Current row validation status."),
    SchemaField("dispute_reason", "string", False, "Reason when row is disputed."),
    SchemaField("source_line", "string", True, "Original synthetic input line."),
]

EXPORT_PREVIEW_COLUMNS = [
    "row_number",
    "item_name",
    "quantity",
    "unit",
    "unit_price",
    "line_total",
    "customer_label",
    "order_reference",
    "row_status",
    "dispute_reason",
]


def order_schema() -> list[SchemaField]:
    return list(ORDER_SCHEMA)


def export_preview_columns() -> list[str]:
    return list(EXPORT_PREVIEW_COLUMNS)


def schema_as_lines() -> list[str]:
    return [
        f"{field.name}: type={field.type_name}; required={field.required}; {field.description}"
        for field in ORDER_SCHEMA
    ]
