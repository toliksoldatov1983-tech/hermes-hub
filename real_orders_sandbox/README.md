# Real Orders Sandbox

Date: 2026-06-17 | Gate: YELLOW — GATE 1 PREPARE ONLY

## Что это

Безопасная изолированная зона для тестирования offline chain на safe copies реальных заказов.

## Что НЕЛЬЗЯ

- ❌ Читать реальные рабочие папки (`E:\Заказы...`, и т.д.)
- ❌ Сканировать диски
- ❌ Открывать оригиналы заказов
- ❌ Обрабатывать .cdr, .art, CNC, Corel, ArtCAM файлы
- ❌ Считать результат производственным заказом

## Структура

```
real_orders_sandbox/
├── input_safe_copies/    ← пользователь кладёт safe copy ВРУЧНУЮ
├── output_results/       ← Hermes пишет результат ТОЛЬКО после Gate 2
├── review_reports/       ← human review обязателен
├── README.md
├── SAFE_COPY_RULES.md
├── PROCESSING_PLAN.md
└── ORDER_COPY_MANIFEST_TEMPLATE.md
```

## Статус

GATE 1: PREPARE ONLY — зона создана. Обработка запрещена без Gate 2.
