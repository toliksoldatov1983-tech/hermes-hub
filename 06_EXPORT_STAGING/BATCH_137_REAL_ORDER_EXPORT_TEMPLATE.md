# BATCH_137 — REAL ORDER EXPORT TEMPLATE

Шаблон. НЕ ВЫПОЛНЯТЬ. Только для будущих реальных заказов.

## INPUT

- order_name: <название>
- year: <год>
- month: <месяц, формат 07_Июль>
- source_type: real
- staging_files: corel.txt + malyarka.xlsx + report.md
- root: E:\РАБОТА\01_ЗАКАЗЫ
- target_folder: E:\РАБОТА\01_ЗАКАЗЫ\{year}\{month}\{order_name}

## REQUIRED CHECKS (до copy)

1. Disputed rows = 0
2. Corel TXT contract PASS
3. Excel XLSX contract PASS
4. ROOT_READY confirmed
5. Target collision check PASS
6. No overwrite/delete/move

## FUTURE JOURNEY

1. Build/export staging files
2. Validate contracts
3. Root preflight
4. Target folder prepare
5. Collision check
6. No-overwrite copy
7. Manifest
8. Verification
9. Close report
10. Update skill

## REPORT FORMAT

ВЫПОЛНЕНО / НЕ ВЫПОЛНЕНО / ИЗМЕНЁННЫЕ ФАЙЛЫ / ПРОВЕРКИ / РИСКИ / СЛЕДУЮЩИЙ БЛОК
