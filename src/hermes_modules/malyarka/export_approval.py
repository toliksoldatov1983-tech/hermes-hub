"""Malyarka Export Approval Gates + Controlled File Creation Plan.

All gates CLOSED. Real file creation blocked. Dry-run only.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# ── Export Approval Gates ──


@dataclass
class ExportApprovalGate:
    gate_id: str
    title: str
    risk_level: str
    default_state: str = "CLOSED"
    preview_allowed: bool = True
    staging_allowed: bool = False
    real_folder_allowed: bool = False
    blocked_actions: list[str] = field(default_factory=list)


EXPORT_APPROVAL_GATES = [
    ExportApprovalGate("APPROVE_MALYARKA_EXPORT_PREFLIGHT", "Export preflight plan", "low",
                       blocked_actions=["real_file_creation"]),
    ExportApprovalGate("APPROVE_CREATE_COREL_TXT_STAGING", "Создание Corel TXT в staging", "medium",
                       staging_allowed=False, blocked_actions=["corel_txt_write"]),
    ExportApprovalGate("APPROVE_CREATE_EXCEL_STAGING", "Создание Excel в staging", "medium",
                       staging_allowed=False, blocked_actions=["excel_write"]),
    ExportApprovalGate("APPROVE_CREATE_COMBINED_EXPORT_STAGING", "Создание combined export в staging", "medium",
                       staging_allowed=False, blocked_actions=["combined_export_write"]),
    ExportApprovalGate("APPROVE_WRITE_TO_PROJECT_STAGING_FOLDER", "Запись в staging папку проекта", "medium",
                       staging_allowed=False, blocked_actions=["staging_write"]),
    ExportApprovalGate("APPROVE_OVERWRITE_EXISTING_EXPORT", "Перезапись существующих export-файлов", "high",
                       blocked_actions=["overwrite"]),
    ExportApprovalGate("APPROVE_WRITE_TO_REAL_ORDER_FOLDER", "Запись в реальную папку заказов", "critical",
                       real_folder_allowed=False, blocked_actions=["real_folder_write", "E:\\Заказы"]),
    ExportApprovalGate("APPROVE_OPEN_EXPORT_FOLDER", "Открытие export-папки в проводнике", "low",
                       blocked_actions=["open_folder"]),
    ExportApprovalGate("APPROVE_COREL_AUTOMATION", "Запуск CorelDRAW automation", "critical",
                       blocked_actions=["corel_launch"]),
    ExportApprovalGate("APPROVE_ARTCAM_AUTOMATION", "Запуск ArtCAM automation", "critical",
                       blocked_actions=["artcam_launch"]),
    ExportApprovalGate("APPROVE_GOOGLE_DRIVE_UPLOAD", "Загрузка export-файлов в Google Drive", "critical",
                       blocked_actions=["google_drive_upload"]),
]


# ── Export Safety State ──


EXPORT_SAFETY_STATE = {
    "preview_allowed": True,
    "staging_file_creation_allowed": False,
    "real_order_folder_write_allowed": False,
    "overwrite_allowed": False,
    "delete_allowed": False,
    "corel_automation_allowed": False,
    "artcam_automation_allowed": False,
    "google_drive_allowed": False,
    "all_gates_closed": True,
    "staging_folder": "C:\\Users\\user\\Desktop\\Hermes-Clean\\06_EXPORT_STAGING (future)",
    "next_approval_phrase": "ОДОБРЯЮ BATCH_113 MALYARKA STAGING FILE CREATION",
}


# ── Staged File Creation Plan ──


FILE_CREATION_PLAN = """
╔══════════════════════════════════════════════════════╗
║   CONTROLLED FILE CREATION PLAN                     ║
╠══════════════════════════════════════════════════════╣
║ STAGE 0: dry-run preview                  │ ACTIVE  ║
║ STAGE 1: user approval export preflight   │ BLOCKED ║
║ STAGE 2: approval staging file creation   │ BLOCKED ║
║ STAGE 3: create files in staging folder   │ BLOCKED ║
║ STAGE 4: verify file contents             │ BLOCKED ║
║ STAGE 5: user manually reviews files      │ BLOCKED ║
║ STAGE 6: real order folder write (future) │ BLOCKED ║
║ STAGE 7: rollback / cleanup               │ READY   ║
╚══════════════════════════════════════════════════════╝
"""


# ── Staging Policy ──


STAGING_POLICY = """
SAFE STAGING FOLDER POLICY

Future staging folder:
  C:\\Users\\user\\Desktop\\Hermes-Clean\\06_EXPORT_STAGING

BLOCKED PATHS:
  E:\\Заказы — PERMANENTLY BLOCKED
  Desktop\\orders — PERMANENTLY BLOCKED
  Google Drive — PERMANENTLY BLOCKED
  Archive folders — PERMANENTLY BLOCKED
  System folders — PERMANENTLY BLOCKED
  External paths — PERMANENTLY BLOCKED
  Relative path escape (../) — PERMANENTLY BLOCKED

OVERWRITE: disabled by default
DELETE: disabled by default

In BATCH_112: no real files are created in any folder.
"""


# ── File Naming Contract ──


FILE_NAMING_CONTRACT = """
FILE NAMING CONTRACT

Patterns:
  {order_slug}_corel.txt
  {order_slug}_malyarka.xlsx
  {order_slug}_export_preview.json
  {order_slug}_export_report.md

Rules:
  - Only safe characters: a-z, 0-9, -, _
  - Russian names: transliterated, original stored in metadata
  - No path separators (/ \\ :)
  - No reserved Windows names (CON, NUL, PRN, etc.)
  - No control characters
  - Max filename length: 120 chars
  - If exists: append _v2, _v3 suffix (future)

In BATCH_112: no files are created.
"""


# ── Content Verification Plan ──


CONTENT_VERIFICATION_PLAN = """
CONTENT VERIFICATION PLAN

Corel TXT checks:
  [ ] First line empty
  [ ] No headers
  [ ] Each line has 3 fields (H, W, Qty)
  [ ] H/W/Qty are numeric
  [ ] Only confirmed rows
  [ ] No disputed rows

Excel checks:
  [ ] 9 columns with correct headers
  [ ] m2 calculated correctly (H*W*Qty/1M)
  [ ] Totals correct
  [ ] Edges NOT counted
  [ ] Disputed rows NOT in export
  [ ] Metadata shows source draft

In BATCH_112: verification plan only. No files to verify.
"""


# ── Overwrite Protection ──


OVERWRITE_PROTECTION = """
OVERWRITE PROTECTION POLICY

Default:
  overwrite_allowed = False
  delete_allowed = False
  replace_allowed = False

If file exists:
  return BLOCKED response
  suggest duplicate-safe filename with _v2 suffix
  require APPROVE_OVERWRITE_EXISTING_EXPORT for overwrite

Delete:
  NEVER allowed for export files
  only staging cleanup through explicit approval
"""


# ── Preflight Dry-Run ──


EXPORT_PREFLIGHT = """
EXPORT PREFLIGHT DRY-RUN

Checks:
  [PASS] active draft exists
  [PASS] confirmed rows present
  [PASS] disputed rows absent (export-ready)
  [PASS] formats selected (corel_txt + excel)
  [PASS] staging path safe (inside project)
  [PASS] file names safe
  [PASS] all gates CLOSED (safe)
  [PASS] real creation BLOCKED
  [PASS] preview available

Result:
  Preview: GO
  Staging file creation: NO-GO (requires approval)
  Real folder write: NO-GO (permanently blocked)
"""


# ── Approval Wording ──


EXPORT_APPROVAL_WORDING = """
╔══════════════════════════════════════════════════════╗
║   EXPORT APPROVAL WORDING                           ║
╠══════════════════════════════════════════════════════╣
║                                                    ║
║  Для staging file creation:                        ║
║  ОДОБРЯЮ BATCH_113 MALYARKA                        ║
║  STAGING FILE CREATION                             ║
║                                                    ║
║  Разрешит:                                         ║
║  - создание файлов в staging папке Hermes-Clean    ║
║                                                    ║
║  НЕ разрешит:                                      ║
║  - запись в E:\\Заказы                              ║
║  - перезапись файлов                               ║
║  - удаление файлов                                 ║
║  - CorelDRAW / ArtCAM / CNC                        ║
║  - Google Drive                                    ║
║  - Telegram live                                   ║
║  - external API                                    ║
║                                                    ║
║  "BATCH_113" без ОДОБРЯЮ — не approval             ║
╚══════════════════════════════════════════════════════╝
"""
