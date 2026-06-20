# Malyarka Agent Pre-Implementation Report

Date: 2026-06-17
Agent: Malyarka Agent (#2, `accepted`, not active)
Autopilot: GREEN_AUTOPILOT_PASS_10_MALYARKA_AGENT_PRE_IMPLEMENTATION_SPEC

## Что подготовлено

| Документ | Назначение |
|----------|-----------|
| `AGENT_SPEC.md` | Полная спецификация (accepted) |
| `SAFETY_RULES.md` | 8 запретов + статусы результата |
| `INTAKE_CONTRACT.md` | Формат приёма от Sales Agent |
| `OUTPUT_CONTRACT.md` | Формат preliminary result |
| `TEST_SCENARIOS.md` | 15 сценариев для проверки |
| `ACCEPTANCE_CRITERIA.md` | 10 критериев приёмки |
| `FAKE_INTAKE_CARDS.md` | 10 искусственных карточек |
| `PRELIMINARY_RESULT_TEMPLATE.md` | Шаблон результата |

## Почему реализация не начата

Python-модуль для Malyarka Agent — **жёлтая зона**. Требуется:
- Явное разрешение пользователя (yellow approval)
- Подтверждение scope реализации
- Реализация = новый Python-код + tests
- После реализации — demo и golden cases

## Yellow approvals для реализации

| # | Что нужно | Почему yellow |
|---|----------|--------------|
| 1 | Создать `src/malyarka_agent.py` | Новый Python-модуль |
| 2 | Создать `tests/test_malyarka_agent.py` | Новые tests |
| 3 | Запустить tests | Исполнение кода |
| 4 | Создать demo cases | Локальный запуск |

## Что запрещено

- 🔴 Реальные заказы
- 🔴 Сервер / live Telegram
- 🔴 Secrets / token / .env
- 🔴 Финальная стоимость
- 🔴 Отправка результатов клиенту
- 🔴 Активация агента

## Следующий шаг

Запросить yellow approval у пользователя для начала реализации Python-модуля Malyarka Agent.
