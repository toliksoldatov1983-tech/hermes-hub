"""Real Folder Preflight Package — no E:\\ disk access."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# ── Preflight Package ──


PREFLIGHT_PACKAGE = """
╔══════════════════════════════════════════════════════╗
║   REAL FOLDER PREFLIGHT PACKAGE                     ║
╠══════════════════════════════════════════════════════╣
║                                                    ║
║  SOURCE (staging, reviewed):                        ║
║  06_EXPORT_STAGING\\demo_order_corel.txt            ║
║  06_EXPORT_STAGING\\demo_order_malyarka.xlsx        ║
║  06_EXPORT_STAGING\\demo_order_export_preview.json  ║
║  06_EXPORT_STAGING\\demo_order_export_report.md     ║
║                                                    ║
║  TARGET PREVIEW (not accessed):                     ║
║  E:\\Заказы\\2026\\07 Июль\\demo_order\\               ║
║                                                    ║
║  REQUIRED APPROVALS (future):                       ║
║  APPROVE_REAL_ORDER_ROOT                            ║
║  APPROVE_REAL_ORDER_FOLDER_CREATE                   ║
║  APPROVE_COPY_COREL_TXT_TO_REAL_ORDER               ║
║  APPROVE_COPY_EXCEL_TO_REAL_ORDER                   ║
║  APPROVE_COPY_EXPORT_REPORT_TO_REAL_ORDER           ║
║                                                    ║
║  BLOCKED ACTIONS:                                   ║
║  E:\\Заказы access — NO-GO                          ║
║  Copy files — NO-GO                                 ║
║  Overwrite — NO-GO                                  ║
║  Delete — NO-GO                                     ║
║  Corel/ArtCAM/Drive — NO-GO                         ║
║                                                    ║
║  NEXT APPROVAL PHRASE:                              ║
║  ОДОБРЯЮ BATCH_117 MALYARKA                        ║
║  REAL FOLDER PREFLIGHT                             ║
║                                                    ║
╚══════════════════════════════════════════════════════╝
"""


# ── Source Lock Snapshot ──


SOURCE_LOCK_SNAPSHOT = {
    "snapshot_batch": "BATCH_116",
    "source_folder": "06_EXPORT_STAGING",
    "files": [
        {"name": "demo_order_corel.txt", "size": 33, "verified": True},
        {"name": "demo_order_malyarka.xlsx", "size": 5232, "verified": True},
        {"name": "demo_order_export_preview.json", "size": 767, "verified": True},
        {"name": "demo_order_export_report.md", "size": 1274, "verified": True},
    ],
    "source_type": "fake_dry_run",
    "staging_only": True,
    "locked_for_review": True,
    "real_folder_write_allowed": False,
    "overwrite_used": False,
    "delete_used": False,
    "audit": {"e_disk_accessed": False, "folders_created": False, "files_copied": False},
}


# ── Dry-Run Mapping ──


DRY_RUN_MAPPING = {
    "mapping_batch": "BATCH_116",
    "e_disk_accessed": False,
    "target_path_checked": False,
    "folders_created": False,
    "files_copied": False,
    "write_allowed_now": False,
    "target_root_preview": "E:\\Заказы\\2026\\07 Июль\\demo_order",
    "mappings": [
        {"source": "demo_order_corel.txt", "target_preview": "E:\\Заказы\\2026\\07 Июль\\demo_order\\demo_order_corel.txt"},
        {"source": "demo_order_malyarka.xlsx", "target_preview": "E:\\Заказы\\2026\\07 Июль\\demo_order\\demo_order_malyarka.xlsx"},
        {"source": "demo_order_export_report.md", "target_preview": "E:\\Заказы\\2026\\07 Июль\\demo_order\\demo_order_export_report.md"},
    ],
}


# ── Target Folder Naming Rules ──


TARGET_FOLDER_NAMING_RULES = """
TARGET FOLDER NAMING RULES

Root:
  E:\\Заказы — requires APPROVE_REAL_ORDER_ROOT

Structure:
  E:\\Заказы\\{year}\\{month} {month_name}\\{order_name}\\

Example (preview, not accessed):
  E:\\Заказы\\2026\\07 Июль\\demo_order\\

Rules:
  - Year + month in path
  - Order name: safe folder name
  - No path separators in order name
  - No reserved Windows names (CON, NUL, PRN, ...)
  - No control characters
  - Duplicate-safe suffix if exists (_v2)
  - Manual confirmation required before folder creation

Current status:
  Root NOT accessed. Folder NOT created.
  All paths are preview strings only.
"""


# ── Copy Plan (without copy) ──


COPY_PLAN_WITHOUT_COPY = """
COPY PLAN WITHOUT COPY

Candidates for future copy:
  1. demo_order_corel.txt → E:\\Заказы\\2026\\07 Июль\\demo_order\\
  2. demo_order_malyarka.xlsx → E:\\Заказы\\2026\\07 Июль\\demo_order\\
  3. demo_order_export_report.md → E:\\Заказы\\2026\\07 Июль\\demo_order\\

NOT to copy:
  - demo_order_export_preview.json (metadata only)

Required gates (must open before copy):
  - APPROVE_REAL_ORDER_ROOT
  - APPROVE_REAL_ORDER_FOLDER_CREATE
  - APPROVE_COPY_COREL_TXT_TO_REAL_ORDER
  - APPROVE_COPY_EXCEL_TO_REAL_ORDER
  - APPROVE_COPY_EXPORT_REPORT_TO_REAL_ORDER

Collision handling:
  - DO NOT overwrite
  - Use duplicate-safe suffix (_v2) if target exists
  - Require APPROVE_OVERWRITE_IN_REAL_ORDER_FOLDER for overwrite

Current status:
  COPY NOT PERFORMED. All gates closed.
"""


# ── Operator Approval Checklist ──


OPERATOR_APPROVAL_CHECKLIST = """
OPERATOR APPROVAL CHECKLIST — Real Folder Write

  [ ] Я проверил Corel TXT (demo_order_corel.txt)
  [ ] Я проверил Excel XLSX (demo_order_malyarka.xlsx)
  [ ] Я понимаю, что это fake/dry-run демо-данные
  [ ] Я понимаю, что E:\\Заказы сейчас НЕ трогался
  [ ] Я понимаю, что следующий batch (BATCH_117) может читать E:\\Заказы только после approval
  [ ] Я понимаю, что overwrite/delete запрещены
  [ ] Я понимаю, что CorelDRAW/ArtCAM/Google Drive не запускаются
  [ ] Я понимаю, что запись в реальные папки заказов будет отдельным этапом
  [ ] Я даю approval на BATCH_117 preflight БЕЗ записи в реальные папки

Approval phrase for BATCH_117:
  ОДОБРЯЮ BATCH_117 MALYARKA REAL FOLDER PREFLIGHT
"""


# ── Risk Register ──


RISK_REGISTER = {
    "risks": [
        {"id": "R01", "title": "Неверный target path", "severity": "high",
         "mitigation": "Path preview only. User confirms before write.", "status": "safe (preview only)"},
        {"id": "R02", "title": "Случайная запись не туда", "severity": "critical",
         "mitigation": "All gates closed. No write allowed.", "status": "blocked"},
        {"id": "R03", "title": "Collision с существующим заказом", "severity": "medium",
         "mitigation": "Duplicate-safe suffix. Overwrite blocked.", "status": "safe (not writing)"},
        {"id": "R04", "title": "Перезапись существующего файла", "severity": "critical",
         "mitigation": "Overwrite gate CLOSED.", "status": "blocked"},
        {"id": "R05", "title": "Удаление файла", "severity": "critical",
         "mitigation": "Delete gate CLOSED. NEVER allowed.", "status": "blocked"},
        {"id": "R06", "title": "Ошибка формата TXT", "severity": "medium",
         "mitigation": "Verified in staging (BATCH_114).", "status": "verified"},
        {"id": "R07", "title": "Ошибка Excel", "severity": "medium",
         "mitigation": "Verified in staging (BATCH_114).", "status": "verified"},
        {"id": "R08", "title": "Путаница fake/real заказа", "severity": "high",
         "mitigation": "Metadata: source_type=fake_dry_run, staging_only=true.", "status": "mitigated"},
        {"id": "R09", "title": "Ручное открытие не того файла", "severity": "low",
         "mitigation": "Operator checklist explains which file to open.", "status": "mitigated"},
        {"id": "R10", "title": "Будущая интеграция Corel/ArtCAM", "severity": "critical",
         "mitigation": "Separate approval required. Gates CLOSED.", "status": "blocked"},
    ]
}


# ── Readiness Snapshot ──


READINESS_SNAPSHOT = """
╔══════════════════════════════════════════════════╗
║   REAL FOLDER WRITE — READINESS SNAPSHOT         ║
╠══════════════════════════════════════════════════╣
║ Staging files reviewed         │ GO ✅          ║
║ Manifest                       │ GO ✅          ║
║ Operator checklist             │ GO ✅          ║
║ Source lock snapshot           │ GO ✅          ║
║ Dry-run mapping                │ GO ✅          ║
║ Copy plan                      │ GO ✅          ║
║ Risk register                  │ GO ✅          ║
║ Preflight package              │ GO ✅          ║
╠══════════════════════════════════════════════════╣
║ E:\\Заказы access               │ NO-GO ❌       ║
║ Target path checked            │ NO-GO ❌       ║
║ Folder created                 │ NO-GO ❌       ║
║ Files copied                   │ NO-GO ❌       ║
║ Overwrite                      │ NO-GO ❌       ║
║ Delete                         │ NO-GO ❌       ║
║ Corel / ArtCAM / Drive         │ NO-GO ❌       ║
╚══════════════════════════════════════════════════╝
"""


# ── Future Approval ──


APPROVAL_WORDING_B117 = """
ОДОБРЯЮ BATCH_117 MALYARKA REAL FOLDER PREFLIGHT

Разрешит: controlled preflight (reading E:\\Заказы, checking target path).
НЕ разрешит: copy files, create folders, overwrite, delete, Corel, ArtCAM, Drive.
"""
