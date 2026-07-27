# BATCH_111 — Malyarka Export Dry-Run + File Contracts

Дата: 2026-07-02 · Статус: **COMPLETED** · 15 new tests

---

## MALYARKA EXPORT CONTRACTS

`MalyarkaExportRequest` → `MalyarkaExportPreview`: Corel TXT + Excel preview + safety.

## COREL TXT PREVIEW

- Первая строка пустая ✓ · Без заголовков ✓
- Формат: `H\tW\tQty` ✓ · Только подтверждённые строки ✓

## MALYARKA EXCEL PREVIEW

- 9 колонок (№, H, W, Qty, м², материал, цвет, фрезеровка, примечание)
- Площадь: H×W×Qty/1M, только лицо ✓ · Торцы не считаются ✓

## DISPUTED ROWS BLOCKING

- Спорные строки → export_allowed=False ✓
- Preview доступен всегда, реальный файл не создаётся ✓

## EXPORT SAFETY POLICY

- Real file write: BLOCKED · Corel launch: BLOCKED · ArtCAM: BLOCKED
- Google Drive: BLOCKED · E:\Заказы: BLOCKED

## ORDER DRAFT INTEGRATION

Использует confirmed_rows + disputed_rows из черновика.

## USER PREVIEW

На русском, без технического мусора. Показывает статус, строки, preview, площадь, следующий шаг.

## CLI (9 команд)

malyarka-export-status, malyarka-export-contracts, malyarka-corel-txt-preview, malyarka-excel-preview, malyarka-export-dry-run, malyarka-export-disputed-demo, malyarka-export-safety-check, malyarka-export-user-preview, malyarka-export-go-no-go.

## ТЕСТЫ: 15. Core +570 по Malyarka = ~720 total.

## GO / NO-GO

| Export dry-run / TXT preview / Excel preview | GO ✅ |
| Real file creation / Corel launch / ArtCAM / Drive | NO-GO ❌ |

## БЕЗОПАСНОСТЬ

Реальные файлы не создавались. Corel/ArtCAM/Drive не трогались. E:\Заказы не трогались.

## СЛЕДУЮЩИЙ ШАГ

`BATCH_112_MALYARKA_EXPORT_APPROVAL_GATES_AND_CONTROLLED_FILE_CREATION_PLAN`
