# Corel Export Agent — ACCEPTANCE CRITERIA

Date: 2026-06-17 | Status: `accepted`, not active

1. Не запускать CorelDRAW
2. Не создавать реальные .cdr файлы
3. Не работать с реальными заказами
4. Export contract только из confirmed rows
5. export_blocked=true → ready_for_corel=false
6. Corel формат: W×H (ширина × высота)
7. Всегда `not_final_export: true`
8. Not active без разрешения
