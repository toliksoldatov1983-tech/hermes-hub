# REPORT — Sales + Client Intake Agent EDGE-CASE HARDENING

Date: 2026-06-17
Agent: Sales + Client Intake Agent (#1)
Status: accepted, offline_module_created, demo_verified, edge_case_hardened, not active

## Результат

```text
Tests: 48 passed, 0 failed in 0.16s
```

## Edge-case hardening — что сделано

| Edge-case | До | После |
|-----------|----|-------|
| Материал «дерево» | Считался подтверждённым | `material_raw="дерево"`, `confirmed=False` |
| Город / location | `city` | `location` + СПб, Алматы, Астана |
| Цвет «белый» | Просто `color` | `color_raw="белый"`, `structured=None` |
| RAL 9010 | Просто `color` | `color_structured="RAL 9010"` |
| Глянец/матовый | `finish` | `surface_finish_raw`, не tech decision |
| Discount + handoff | Не блокировал | Блокирует: ready=false, manager=true |
| Ready for Malyarka | При наличии размеров/материала/цвета | + material_confirmed + нет blocking flags |

## Новые тесты (7 edge-case)

1. `test_edge_material_derevo_ambiguous` — дерево → ambiguous
2. `test_edge_spb_location_preserved` — СПб → location
3. `test_edge_almaty_location` — Алматы → location
4. `test_edge_color_bely_ne_ral` — белый ≠ RAL
5. `test_edge_ral_as_structured` — RAL 9010 → structured
6. `test_edge_finish_not_technical_decision` — матовый не tech
7. `test_edge_discount_blocks_malyarka` — скидка блокирует

## Обновлённые файлы

| Файл | Действие |
|------|---------|
| `src/intake_agent.py` | Переписан (hardened) |
| `tests/test_golden_cases.py` | +7 edge-case тестов |
| `tests/test_intake_agent.py` | city→location, дерево ambiguous |
| `demo/demo_outputs.md` | Сценарии 5, 10, 15 обновлены |
| `GOLDEN_CASES.md` | +7 edge-case GC |
| `ACCEPTANCE_CRITERIA.md` | Hardened поля документированы |

## Safety

```
server: false | secrets: false | telegram: false | live: false | commit: false
```

## Next Step

Ждать разрешения на подключение к Telegram через безопасный adapter.
