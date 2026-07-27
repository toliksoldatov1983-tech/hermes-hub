# BATCH_136 — PRODUCTION GATES BEFORE REAL ORDERS

До запуска export на реальном клиентском заказе все 11 gates должны быть пройдены.

| Gate | Условие |
|------|---------|
| 1 | Real order input confirmed — пользователь дал заказ явно, это не demo_order |
| 2 | Disputed rows = 0 — спорные строки блокируют final export |
| 3 | Corel TXT contract PASS — первая строка пустая, H\tW\tQty |
| 4 | Excel XLSX contract PASS — 9 колонок, площадь лицо |
| 5 | ROOT_READY confirmed — E:\РАБОТА\01_ЗАКАЗЫ |
| 6 | Target folder planned — year/month/order по правилам, стиль 07_Июль |
| 7 | Collision check — target не занят, no overwrite |
| 8 | Copy mode — copy only, no move/overwrite/delete |
| 9 | Manifest — создаётся в target папке |
| 10 | Verification — sizes match, source intact |
| 11 | Dangerous zones closed — .env/Corel/ArtCAM/Drive/Telegram/network/DB |

**Default: все gates closed. Открываются только после проверки.**
