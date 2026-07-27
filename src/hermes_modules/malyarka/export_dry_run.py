"""Malyarka Export Dry-Run — contracts, previews, safety policy.

All dry-run. No real file creation. No real orders.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from enum import Enum, auto


class ExportFormat(Enum):
    COREL_TXT = "corel_txt"
    MALYARKA_EXCEL = "malyarka_excel"
    COMBINED_PREVIEW = "combined_preview"


@dataclass
class MalyarkaExportRequest:
    source_type: str = "dry-run"
    draft_id: str = ""
    order_title: str = ""
    confirmed_rows: list[dict] = field(default_factory=list)
    disputed_rows: list[dict] = field(default_factory=list)
    material: str = ""
    color: str = ""
    routing_type: str = ""
    notes: str = ""
    dry_run: bool = True
    requested_formats: list[ExportFormat] = field(default_factory=lambda: [ExportFormat.COREL_TXT, ExportFormat.MALYARKA_EXCEL])
    approval_state: str = "dry_run_only"
    audit_metadata: dict[str, Any] = field(default_factory=lambda: {
        "real_file_created": False, "env_read": False,
        "folder_write": False, "corel_launched": False,
        "artcam_launched": False, "google_drive_upload": False,
    })


@dataclass
class MalyarkaExportPreview:
    export_allowed: bool = False
    blocked_reason: str = ""
    corel_txt_preview: str = ""
    excel_preview: dict = field(default_factory=dict)
    confirmed_rows_count: int = 0
    disputed_rows_count: int = 0
    total_area_m2: float = 0.0
    warnings: list[str] = field(default_factory=list)
    next_step: str = ""
    audit_metadata: dict[str, Any] = field(default_factory=lambda: {
        "real_file_created": False, "dry_run_only": True,
    })

    def to_dict(self) -> dict:
        return {
            "export_allowed": self.export_allowed, "blocked_reason": self.blocked_reason,
            "corel_txt_preview": self.corel_txt_preview,
            "excel_preview": self.excel_preview,
            "confirmed_rows_count": self.confirmed_rows_count,
            "disputed_rows_count": self.disputed_rows_count,
            "total_area_m2": self.total_area_m2,
            "warnings": self.warnings, "next_step": self.next_step,
            "audit_metadata": self.audit_metadata,
        }


# ── Corel TXT Preview ──


def build_corel_txt_preview(confirmed_rows: list[dict]) -> str:
    """Build Corel TXT preview string.

    Rules:
    - First line empty
    - No headers
    - Each line: height width quantity (tab-separated)
    - Only confirmed rows
    - Height and width NOT swapped
    """
    lines = [""]  # First line empty
    for row in confirmed_rows:
        h = row.get("height", row.get("h", row.get("H", "")))
        w = row.get("width", row.get("w", row.get("W", "")))
        qty = row.get("quantity", row.get("qty", row.get("Qty", "1")))
        if h and w:
            lines.append(f"{h}\t{w}\t{qty}")
    return "\n".join(lines)


# ── Excel Preview ──


def build_excel_preview(confirmed_rows: list[dict], material: str = "", color: str = "", routing: str = "", notes: str = "") -> dict:
    """Build Excel preview structure without creating a file.

    Columns: №, H, W, Qty, m2, Material, Color, Routing, Notes
    Area: H * W * Qty / 1_000_000 (face side only, no edges)
    """
    headers = ["№", "H", "W", "Qty", "м²", "Материал", "Цвет", "Фрезеровка", "Примечание"]
    rows = []
    total_area = 0.0

    for i, row in enumerate(confirmed_rows, 1):
        h_val = row.get("height") or row.get("h") or row.get("H") or 0
        w_val = row.get("width") or row.get("w") or row.get("W") or 0
        h = float(h_val)
        w = float(w_val)
        qty = int(row.get("quantity", row.get("qty", row.get("Qty", 1)) or 1))
        area = (h * w * qty) / 1_000_000  # m2
        total_area += area

        rows.append([
            i, h, w, qty,
            round(area, 4),
            row.get("material", material),
            row.get("color", color),
            row.get("routing", routing),
            row.get("notes", notes),
        ])

    return {
        "headers": headers,
        "rows": rows,
        "total_area_m2": round(total_area, 4),
        "row_count": len(confirmed_rows),
    }


# ── Export Builder ──


def build_export_preview(request: MalyarkaExportRequest) -> MalyarkaExportPreview:
    """Build a full export preview from a request."""
    confirmed = request.confirmed_rows
    disputed = request.disputed_rows

    # Block if disputed rows exist
    if disputed:
        return MalyarkaExportPreview(
            export_allowed=False,
            blocked_reason="Export заблокирован: есть спорные строки. Исправьте спорные строки.",
            confirmed_rows_count=len(confirmed),
            disputed_rows_count=len(disputed),
            corel_txt_preview=build_corel_txt_preview(confirmed),
            excel_preview=build_excel_preview(confirmed, request.material, request.color, request.routing_type, request.notes),
            warnings=[f"⚠️ {len(disputed)} спорных строк. Real export заблокирован."],
            next_step="Исправьте спорные строки или запросите approval на controlled file creation.",
        )

    if not confirmed:
        return MalyarkaExportPreview(
            export_allowed=False,
            blocked_reason="Нет подтверждённых строк для export.",
            next_step="Добавьте подтверждённые строки в черновик.",
        )

    corel_preview = build_corel_txt_preview(confirmed)
    excel_preview = build_excel_preview(confirmed, request.material, request.color, request.routing_type, request.notes)

    return MalyarkaExportPreview(
        export_allowed=True,
        confirmed_rows_count=len(confirmed),
        disputed_rows_count=len(disputed),
        corel_txt_preview=corel_preview,
        excel_preview=excel_preview,
        total_area_m2=excel_preview.get("total_area_m2", 0),
        warnings=[],
        next_step="Preview готов. Реальный файл не создан. Для controlled file creation запросите approval в будущем batch.",
    )


# ── Export Safety Policy ──


class ExportSafetyPolicy:
    BLOCKED_PATHS = [
        "E:\\Заказы", "E:\\Orders", "C:\\Users\\user\\Desktop\\Заказы",
    ]

    @staticmethod
    def check_file_write(path: str) -> tuple[bool, str]:
        for blocked in ExportSafetyPolicy.BLOCKED_PATHS:
            if path.lower().startswith(blocked.lower()):
                return False, f"Запись в {blocked} запрещена в dry-run."
        return False, "Реальное создание файлов запрещено в dry-run. Используйте preview."

    @staticmethod
    def check_corel_launch() -> tuple[bool, str]:
        return False, "Запуск CorelDRAW запрещён в dry-run."

    @staticmethod
    def check_artcam_launch() -> tuple[bool, str]:
        return False, "Запуск ArtCAM запрещён в dry-run."

    @staticmethod
    def check_google_drive() -> tuple[bool, str]:
        return False, "Google Drive upload запрещён."


# ── Export Demo Data ──


DEMO_CONFIRMED_ROWS = [
    {"height": 720, "width": 300, "quantity": 2, "material": "МДФ", "color": "белый", "routing": "нет", "notes": ""},
    {"height": 800, "width": 400, "quantity": 1, "material": "МДФ", "color": "серый", "routing": "фаска", "notes": ""},
    {"height": 600, "width": 250, "quantity": 3, "material": "ЛДСП", "color": "белый", "routing": "нет", "notes": "полка"},
]

DEMO_DISPUTED_ROW = [
    {"raw_text": "broken row without data", "dispute_reason": "Нет разделителя '|'"},
]


# ── User Preview Format ──


EXPORT_USER_PREVIEW_TEMPLATE = """
📋 ЧЕРНОВИК ЗАКАЗА — EXPORT PREVIEW

Статус: {status}
Подтверждённых строк: {confirmed}
Спорных строк: {disputed}

--- COREL TXT PREVIEW ---
{corel_preview}

--- EXCEL PREVIEW ---
Колонки: №, H, W, Qty, м², Материал, Цвет, Фрезеровка, Примечание
Строк: {excel_rows}
Общая площадь: {total_area} м²

{badges}
Следующий шаг: {next_step}
"""
