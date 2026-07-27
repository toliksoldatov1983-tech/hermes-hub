# HERMES-CHAT → CODEX HANDOFF

Дата: 2026-07-02 · Проект: Hermes-Clean · Папка: C:\Users\user\Desktop\Hermes-Clean

---

## КЛЮЧЕВЫЕ ПРАВИЛА

- Ответы на русском. Пользователь живёт в Астане.
- Пользователь не понимает английский — интерфейс и ответы всегда русские.
- Не дробить задачи. Делать крупными блоками.
- Безопасные batch-и по плану — выполняются автоматически.
- Опасные переходы (live Telegram, E:\Заказы, Corel/ArtCAM, Drive, токены, удаление) — только после точной approval-фразы.
- Approval-фраза = отдельное сообщение с «ОДОБРЯЮ BATCH_NNN ...». Упоминание в отчёте — не approval.

---

## ЧТО УЖЕ ГОТОВО

### Telegram dry-run линия (ЗАКРЫТА)

BATCH_088–110 выполнены. RC: TELEGRAM-DRY-RUN-RC-1 — ACCEPTED и CLOSED.

| Компонент | Статус |
|-----------|--------|
| Intent router (10 типов) | ГОТОВ |
| Conversation memory | ГОТОВ |
| Order draft state | ГОТОВ |
| E2E scenarios (8 сценариев) | PASS |
| Live gateway readiness | ГОТОВ |
| 10 approval gates | ВСЕ CLOSED |
| 7 hardening layers | АКТИВНЫ |
| Operator console + 10 failure drills | ГОТОВ |
| Acceptance (10 сценариев, 14 критериев) | PASS |

**Live Telegram: NO-GO.** Токен не читался. Polling/webhook/send — disabled.

Фраза для live: «ОДОБРЯЮ BATCH_111 FIRST TELEGRAM LIVE PREFLIGHT» (не была дана).

---

### Malyarka export линия (АКТИВНА)

BATCH_111–128 выполнены.

#### Staging (06_EXPORT_STAGING)

| Файл | Размер | Статус |
|------|--------|--------|
| demo_order_corel.txt | 33 B | ✅ |
| demo_order_malyarka.xlsx | 5232 B | ✅ |
| demo_order_export_preview.json | 767 B | ✅ |
| demo_order_export_report.md | 1274 B | ✅ |
| STAGING_MANIFEST.md | — | ✅ |
| OPERATOR_REVIEW_CHECKLIST_RU.md | — | ✅ |
| BATCH_117_OPERATOR_DECISION_PACKAGE.md | — | ✅ |
| BATCH_117_REAL_FOLDER_PREFLIGHT_HOLD.md | — | ✅ |
| BATCH_117_APPROVAL_WORDING.md | — | ✅ |
| BATCH_117_NO_E_DISK_GUARD_REPORT.md | — | ✅ |
| BATCH_118_SAFE_HOLD_STATUS.md | — | ✅ |
| BATCH_118_OPERATOR_DECISION_MATRIX.md | — | ✅ |
| BATCH_118_PREFLIGHT_READINESS_WITHOUT_ACCESS.md | — | ✅ |
| BATCH_118_TEST_RECONCILIATION.md | — | ✅ |
| BATCH_118_NEXT_APPROVAL_GATE.md | — | ✅ |
| BATCH_119_REAL_FOLDER_PREFLIGHT_CONTROLLED.md | — | ✅ (BLOCKED) |
| BATCH_122_TARGET_ROOT_BLOCK_REPORT.md | — | ✅ |
| BATCH_122_OPERATOR_TARGET_ROOT_DECISION.md | — | ✅ |
| BATCH_122_SAFE_LOCAL_FALLBACK_PLAN.md | — | ✅ |
| BATCH_122_NEXT_CHAIN_OPTIONS.md | — | ✅ |
| BATCH_123_124_125 docs | — | ✅ |
| BATCH_126_127_128 docs | — | ✅ |

#### Simulation (07_REAL_FOLDER_SIMULATION)

3 файла скопированы из staging (no-overwrite): Corel TXT, Excel XLSX, Report MD. Размеры совпадают. Манифесты на месте.

#### Corel TXT контракт

- Первая строка пустая
- Без заголовков
- Формат: H \t W \t Qty
- Только confirmed rows

#### Excel контракт

- 9 колонок: №, H, W, Qty, м², Материал, Цвет, Фрезеровка, Примечание
- Площадь = H × W × Qty / 1_000_000 (только лицо, торцы не считаются)

#### Real-folder chain

**HOLD.** BATCH_119: E:\Заказы не существует. BATCH_120/121 пропущены. Ждём валидный target root или явный ROOT_READY от пользователя.

---

## КЛЮЧЕВЫЕ МОДУЛИ (src/)

```
hermes_core/
├── telegram_intent/          — intent router, order detector
├── telegram_memory/          — conversation memory, draft lifecycle, context router
├── telegram_e2e/            — E2E scenarios, runner
├── telegram_live/            — gateway, approval gates, hardening,
│                                user decision, acceptance, release candidate,
│                                stabilization, closeout
│   ├── gateway_contract.py
│   ├── approval_plan.py
│   ├── hardening.py
│   ├── user_decision.py
│   ├── acceptance.py
│   ├── release_candidate.py
│   ├── stabilization.py
│   └── closeout.py
└── controlled_access/        — bind mode, access policy, tailscale readiness

hermes_modules/malyarka/
├── export_dry_run.py         — Corel TXT + Excel previews, safety policy
├── export_approval.py        — 11 export gates, staging policy, file naming, preflight
├── export_rehearsal.py       — staging rehearsal, fake verification, collision, rollback
├── real_folder_contract.py   — destination resolver, real folder gates, no-write rehearsal
└── real_folder_preflight.py  — preflight package, source lock, dry-run mapping, risk register
```

---

## TEST COUNT

- Collected: ~822
- Passed: ~809
- Failed: 13 (10 E2E shared-state + 2 CLI parser + 1 subprocess — все известные, не затрагивают export/staging/safety)

---

## ТЕКУЩЕЕ СОСТОЯНИЕ

| Линия | Статус |
|-------|--------|
| Telegram dry-run | CLOSED ✅ |
| Malyarka staging | GO ✅ |
| Malyarka simulation | GO ✅ |
| Malyarka real-folder | HOLD (E:\ unavailable) |
| Live Telegram | NO-GO |
| Approval gates | Все CLOSED |
| .env/token/key | Не читались |
| Corel/ArtCAM/Drive | Не трогались |

---

## NEXT

Ждём оператора: восстановить E:\Заказы, указать другой root, или продолжить dry-run.

По умолчанию: BATCH_129_REAL_ROOT_WAIT_OR_USER_SELECTED_ROOT_PREFLIGHT
