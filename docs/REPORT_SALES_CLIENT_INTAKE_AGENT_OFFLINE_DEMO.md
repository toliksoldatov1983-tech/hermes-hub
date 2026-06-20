# REPORT — Sales + Client Intake Agent Offline Demo

Date: 2026-06-17
Agent: Sales + Client Intake Agent (#1)
Status: accepted, offline_module_created, not active

## Результаты

```text
Golden cases:    18/18 passed (0.08s)
Scenario tests:  23/23 passed (0.09s)
TOTAL:           41/41 passed
Demo runner:     15/15 passed
```

## Созданные файлы

| Файл | Описание |
|------|---------|
| `demo/demo_inputs.md` | 15 тестовых сообщений |
| `demo/demo_outputs.md` | Golden expected outputs |
| `demo/run_demo.py` | Offline demo runner (15 scenarios) |
| `tests/test_golden_cases.py` | 18 golden case tests (15 scenarios + 3 safety) |
| `GOLDEN_CASES.md` | Документация golden cases |

## Исправления в модуле

- RAL-номера больше не парсятся как размеры (RAL 9010 600 → 9010×600 исправлено)
- Цвет «белые» (мн.ч.) корректно определяется
- Санкт-Петербург с правильной капитализацией

## Demo Outputs (примеры)

**#9 Только покраска:**
```
Input:  Только покраска. Фасады уже есть. 1000 400 4 шт МДФ белый матовый
Status: ready_for_review
Ready:  ✅ | Manager: ❌
Resp:   Проверьте, пожалуйста, всё верно?
        1. 1000×400 мм, 4 шт, МДФ, белый, матовый
```

**#15 Все данные:**
```
Input:  1000 400 4 шт МДФ белый матовый RAL 9010
        600 300 2 шт дерево коричневый глянцевый
        Санкт-Петербург.
Status: ready_for_review
Ready:  ✅ | Manager: ❌
Resp:   Проверьте, пожалуйста, всё верно?
        1. 1000×400 мм, 4 шт, МДФ, RAL 9010, матовый
        2. 600×300 мм, 2 шт, дерево, коричневый, глянцевый
```

**#5 Скидка:**
```
Input:  1000 400 МДФ белый. Скидка будет если 10 штук?
Status: ready_for_review
Ready:  ❌ (discount blocks) | Manager: ✅
Resp:   Итоговую стоимость и возможные условия подтвердит менеджер...
```

## Safety

```
server: false | secrets: false | telegram: false | live: false
```

## Next Step

Ждать разрешения на подключение к Telegram через безопасный adapter.
