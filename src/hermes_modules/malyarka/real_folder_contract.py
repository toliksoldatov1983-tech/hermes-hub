"""Real Order Folder Write Contract — plan only, no write to E:\\Заказы."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# ── Real Folder Write Request ──


@dataclass
class MalyarkaRealFolderWriteRequest:
    source_staging: str = "06_EXPORT_STAGING"
    target_root_preview: str = "E:\\Заказы (preview only — not accessed)"
    order_title: str = ""
    write_mode: str = "plan_only"  # plan_only, preflight_future, controlled_write_future
    real_write_allowed: bool = False
    overwrite_allowed: bool = False
    delete_allowed: bool = False
    files_to_copy: list[str] = field(default_factory=list)
    audit_metadata: dict[str, Any] = field(default_factory=lambda: {
        "e_disk_accessed": False, "real_folder_created": False,
        "files_copied": False, "env_read": False,
    })


# ── Destination Path Policy ──


DESTINATION_PATH_POLICY = """
DESTINATION PATH POLICY

Default state:
  write_mode = plan_only
  real_write_allowed = FALSE
  overwrite_allowed = FALSE
  delete_allowed = FALSE

Future root (not accessed now):
  E:\\Заказы — requires separate approval, NOT in BATCH_115

Path rules:
  - absolute path only
  - target must be user-approved
  - path traversal (../) BLOCKED
  - system folders BLOCKED
  - network/UNC paths BLOCKED
  - Google Drive BLOCKED
  - overwrite: BLOCKED by default
  - delete: BLOCKED by default
  - duplicate-safe names required
"""


# ── Real Folder Write Approval Gates ──


REAL_FOLDER_GATES = [
    {"id": "APPROVE_REAL_ORDER_ROOT", "risk": "critical", "state": "CLOSED"},
    {"id": "APPROVE_REAL_ORDER_FOLDER_CREATE", "risk": "critical", "state": "CLOSED"},
    {"id": "APPROVE_COPY_COREL_TXT_TO_REAL_ORDER", "risk": "high", "state": "CLOSED"},
    {"id": "APPROVE_COPY_EXCEL_TO_REAL_ORDER", "risk": "high", "state": "CLOSED"},
    {"id": "APPROVE_COPY_EXPORT_REPORT_TO_REAL_ORDER", "risk": "high", "state": "CLOSED"},
    {"id": "APPROVE_OVERWRITE_IN_REAL_ORDER_FOLDER", "risk": "critical", "state": "CLOSED"},
    {"id": "APPROVE_DELETE_IN_REAL_ORDER_FOLDER", "risk": "critical", "state": "CLOSED"},
    {"id": "APPROVE_OPEN_REAL_ORDER_FOLDER", "risk": "low", "state": "CLOSED"},
]


# ── Dry-Run Destination Resolver ──


def resolve_destination_dry_run(order_title: str = "demo_order") -> dict:
    """Build future destination path WITHOUT accessing E:\\Заказы."""
    return {
        "target_path_preview": f"E:\\Заказы\\2026\\07 Июль\\{order_title}\\",
        "path_allowed_if_approved": True,
        "blocked_now_reason": "E:\\Заказы access blocked in dry-run. Requires APPROVE_REAL_ORDER_ROOT.",
        "required_approval": "APPROVE_REAL_ORDER_ROOT",
        "risks": [
            "Write to real order folder",
            "Potential overwrite of existing order",
            "Requires operator manual review",
        ],
        "safe_alternative": "Continue working in 06_EXPORT_STAGING. Open manually when ready.",
        "audit": {"e_disk_accessed": False},
    }


# ── No-Write Rehearsal ──


NO_WRITE_REHEARSAL_TRANSCRIPT = """
NO-WRITE REAL FOLDER REHEARSAL

  [PASS] Staging files reviewed (4 files OK)
  [PASS] Destination path preview built (E:\\Заказы\\...\\demo_order)
  [PASS] Gates checked (8/8 CLOSED)
  [PASS] Write BLOCKED (real_folder_write gate closed)
  [PASS] Copy BLOCKED (copy gates closed)
  [PASS] No folders created
  [PASS] No files copied
  [PASS] No E:\\Заказы access

Result:
  real folder write = NO-GO
  plan readiness = GO
"""


# ── Rollback / Supersede Policy ──


ROLLBACK_SUPERSEDE_POLICY = """
ROLLBACK / SUPERSEDE POLICY

Rules:
  - DO NOT delete old export files
  - DO NOT overwrite existing files
  - Create duplicate-safe versions (_v2, _v3) on conflict
  - Mark erroneous staging files as SUPERSEDED in metadata
  - Real rollback for E:\\Заказы: separate plan + separate approval

Current state:
  No real folder files exist → nothing to rollback
"""


# ── Future Approval Wording ──


REAL_FOLDER_APPROVAL_WORDING = """
Для будущего preflight записи в реальные папки:
  ОДОБРЯЮ BATCH_116 MALYARKA REAL ORDER FOLDER WRITE PREFLIGHT

Разрешит: preflight plan + rehearsal (no actual write).
НЕ разрешит: автоматическую запись, overwrite, delete, Corel, ArtCAM, Drive.
"""


# ── Go/No-Go ──


REAL_FOLDER_GO_NOGO = """
╔══════════════════════════════════════════════════╗
║   MALYARKA REAL FOLDER — GO / NO-GO             ║
╠══════════════════════════════════════════════════╣
║ Staging review              │ GO ✅             ║
║ Operator checklist          │ GO ✅             ║
║ Destination resolver dry-run│ GO ✅             ║
║ No-write rehearsal          │ GO ✅             ║
║ Plan readiness              │ GO ✅             ║
╠══════════════════════════════════════════════════╣
║ Real folder write           │ NO-GO ❌          ║
║ E:\\Заказы access            │ NO-GO ❌          ║
║ Copy to real folder         │ NO-GO ❌          ║
║ Overwrite                   │ NO-GO ❌          ║
║ Delete                      │ NO-GO ❌          ║
║ Corel / ArtCAM / Drive      │ NO-GO ❌          ║
╚══════════════════════════════════════════════════╝
"""
