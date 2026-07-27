# BATCH_115 — Staging Review + Real Order Folder Write Plan

Дата: 2026-07-02 · Статус: **COMPLETED**

---

## STAGING FILE REVIEW

4/4 файлов проверены. Все в 06_EXPORT_STAGING. Corel TXT: 4 строки (первая пустая), 3 data строки. Excel: 9 колонок. Все контракты соблюдены.

## STAGING MANIFEST (2 новых файла)

`STAGING_MANIFEST.md` + checklist в staging folder.

## OPERATOR REVIEW CHECKLIST

`OPERATOR_REVIEW_CHECKLIST_RU.md` — 12 пунктов проверки TXT + Excel.

## REAL ORDER FOLDER WRITE CONTRACT

`MalyarkaRealFolderWriteRequest`: plan_only, все writes=false. 8 gates CLOSED.

## DESTINATION PATH POLICY

E:\Заказы — future only. Path traversal/system/network/Drive BLOCKED.

## DRY-RUN DESTINATION RESOLVER

Строит preview путь без доступа к E:\Заказы. audit: e_disk_accessed=False.

## REAL FOLDER APPROVAL GATES (8, all CLOSED)

APPROVE_REAL_ORDER_ROOT, APPROVE_REAL_ORDER_FOLDER_CREATE, APPROVE_COPY_COREL_TXT_TO_REAL_ORDER,
APPROVE_COPY_EXCEL_TO_REAL_ORDER, APPROVE_COPY_EXPORT_REPORT_TO_REAL_ORDER,
APPROVE_OVERWRITE_IN_REAL_ORDER_FOLDER, APPROVE_DELETE_IN_REAL_ORDER_FOLDER,
APPROVE_OPEN_REAL_ORDER_FOLDER.

## NO-WRITE REHEARSAL

8/8 PASS. Real folder write=NO-GO. Plan readiness=GO.

## FUTURE APPROVAL PHRASE

ОДОБРЯЮ BATCH_116 MALYARKA REAL ORDER FOLDER WRITE PREFLIGHT

## CLI (10 новых) + ТЕСТЫ (11 новых)

## GO / NO-GO

| Staging review / manifest / checklist / resolver / rehearsal | GO ✅ |
| Real folder write / E:\Заказы / copy / overwrite / delete / Corel / ArtCAM / Drive | NO-GO ❌ |

## СЛЕДУЮЩИЙ ШАГ

`BATCH_116_MALYARKA_REAL_ORDER_FOLDER_WRITE_PREFLIGHT_IF_EXPLICITLY_APPROVED_OR_CONTINUE_STAGING_LINE`
