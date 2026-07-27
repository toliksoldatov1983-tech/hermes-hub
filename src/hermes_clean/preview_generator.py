"""Preview Report Generator — формирование расширенного превью-отчёта.

Интегрирован с машиной состояний и модулем валидации.
Генерирует отчёт с confirmed/disputed rows, validation issues,
synthetic pricing, export block reasons и рекомендациями оператору.

Без Telegram, API, БД, секретов.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .state_machine import OrderState, OrderStateMachine, STATE_LABELS
from .export_gate import build_export_model, ExportBlockedError
from .validation import validate_order_result as _run_validation


# ── Synthetic pricing defaults ─────────────────────────────────

PRICE_PER_M2 = 150.0       # руб/м² — базовая цена
MATERIAL_COST_PER_M2 = 80.0  # руб/м² — себестоимость материала
MARGIN_THRESHOLD = 0.30     # 30% — минимальная маржа


def _calc_row_price(height_mm: int, width_mm: int, quantity: int) -> dict[str, float]:
    """Рассчитать синтетическую стоимость одной строки."""
    area_m2 = height_mm * width_mm * quantity / 1_000_000
    revenue = round(area_m2 * PRICE_PER_M2, 2)
    cost = round(area_m2 * MATERIAL_COST_PER_M2, 2)
    margin = round((revenue - cost) / revenue * 100, 1) if revenue > 0 else 0.0
    return {
        "area_m2": round(area_m2, 6),
        "revenue_rub": revenue,
        "cost_rub": cost,
        "margin_pct": margin,
    }


# ── Типы данных ────────────────────────────────────────────────

@dataclass(frozen=True)
class PreviewReport:
    """Расширенный превью-отчёт заказа."""

    # ── Блок 1: confirmed rows ──
    confirmed_total: int
    confirmed_rows_preview: list[dict[str, Any]]
    confirmed_area_m2: float

    # ── Блок 2: disputed rows ──
    disputed_total: int
    disputed_rows_preview: list[dict[str, Any]]

    # ── Блок 3: validation issues ──
    validation_valid: bool
    validation_violations: list[dict[str, Any]]
    validation_violations_count: int

    # ── Блок 4: synthetic pricing ──
    pricing_rows: list[dict[str, Any]]
    pricing_total_revenue: float
    pricing_total_cost: float
    pricing_avg_margin_pct: float
    pricing_is_profitable: bool

    # ── Блок 5: export block reasons ──
    export_blocked: bool
    export_block_reasons: list[str]
    export_ready: bool

    # ── Блок 6: next safe action ──
    current_state: str
    current_state_label: str
    next_safe_action: str

    # ── Сводка ──
    summary: str


# ── Генератор отчёта ───────────────────────────────────────────

def generate_preview(
    order_result: dict[str, Any],
    state_machine: OrderStateMachine | None = None,
    *,
    validation_result: dict[str, Any] | None = None,
) -> PreviewReport:
    """Сформировать расширенный превью-отчёт.

    Args:
        order_result: Словарь заказа (confirmed_rows, disputed_rows, total_area_m2, status).
        state_machine: Опционально — машина состояний (текущее состояние).
        validation_result: Опционально — результат валидации (если None — запускается
                           автоматически через validate_order_result).

    Returns:
        PreviewReport — замороженный dataclass со всеми блоками.
    """
    # ── Безопасные значения по умолчанию ──
    confirmed = order_result.get("confirmed_rows", [])
    disputed = order_result.get("disputed_rows", [])
    status = order_result.get("status", "unknown")
    total_area = order_result.get("total_area_m2", 0)

    # ── Блок 1: confirmed rows ──
    confirmed_preview = []
    for i, row in enumerate(confirmed[:20]):  # показываем максимум 20 строк
        h = row.get("height_mm", row.get("height", 0))
        w = row.get("width_mm", row.get("width", 0))
        q = row.get("quantity", 1)
        confirmed_preview.append({
            "index": i + 1,
            "height_mm": h,
            "width_mm": w,
            "quantity": q,
            "area_m2": round(h * w * q / 1_000_000, 6),
        })

    confirmed_total = len(confirmed)
    confirmed_area_m2 = round(sum(
        r.get("height_mm", r.get("height", 0))
        * r.get("width_mm", r.get("width", 0))
        * r.get("quantity", 1)
        for r in confirmed
    ) / 1_000_000, 6)

    # ── Блок 2: disputed rows ──
    disputed_preview = []
    for row in disputed[:20]:
        disputed_preview.append({
            "dispute_id": row.get("dispute_id", "?"),
            "source_line": row.get("source_line", "?"),
            "reason": row.get("reason", "?"),
            "raw_text": row.get("raw_text", ""),
            "suggested_question": row.get("suggested_question", ""),
        })
    disputed_total = len(disputed)

    # ── Блок 3: validation issues ──
    if validation_result is None:
        validation_result = _run_validation(order_result)
    violations = validation_result.get("violations", [])
    violations_count = len(violations)
    validation_valid = validation_result.get("valid", True)

    # ── Блок 4: synthetic pricing ──
    pricing_rows: list[dict[str, Any]] = []
    total_revenue = 0.0
    total_cost = 0.0
    profitable_rows = 0

    for row in confirmed:
        h = row.get("height_mm", row.get("height", 0))
        w = row.get("width_mm", row.get("width", 0))
        q = row.get("quantity", 1)
        if h and w:
            price = _calc_row_price(h, w, q)
            pricing_rows.append(price)
            total_revenue += price["revenue_rub"]
            total_cost += price["cost_rub"]
            if price["margin_pct"] >= MARGIN_THRESHOLD * 100:
                profitable_rows += 1

    total_revenue = round(total_revenue, 2)
    total_cost = round(total_cost, 2)
    avg_margin = round(
        (total_revenue - total_cost) / total_revenue * 100, 1
    ) if total_revenue > 0 else 0.0
    is_profitable = avg_margin >= MARGIN_THRESHOLD * 100

    # ── Блок 5: export block reasons ──
    export_block_reasons: list[str] = []
    export_blocked = False

    if status == "empty_or_invalid":
        export_blocked = True
        export_block_reasons.append("Статус 'empty_or_invalid': заказ пуст или не содержит разбираемых данных.")

    if disputed:
        export_blocked = True
        export_block_reasons.append(
            f"Обнаружено {disputed_total} спорных строк. "
            "Требуется разрешение через DisputeResolver."
        )

    if not validation_valid and violations_count > 0:
        export_blocked = True
        reason_types = {v.get("reason", "?") for v in violations}
        export_block_reasons.append(
            f"Нарушения валидации ({violations_count}): {', '.join(sorted(reason_types))}."
        )

    if order_result.get("export_blocked"):
        export_blocked = True
        export_block_reasons.append("Ручная блокировка экспорта (export_blocked=True).")

    if not export_block_reasons:
        export_block_reasons.append("Экспорт не заблокирован.")

    # ── Определяем состояние ──
    if state_machine is not None:
        current_state = state_machine.state.name
        current_state_label = state_machine.state_label
        export_ready = state_machine.can_export
    else:
        current_state = status.upper() if status != "unknown" else "UNKNOWN"
        current_state_label = STATE_LABELS.get(
            next((s for s in OrderState if s.name == current_state), None),
            status,
        )
        export_ready = (
            not export_blocked
            and validation_valid
            and disputed_total == 0
        )

    # ── Блок 6: next safe action ──
    next_safe_action = _recommend_next_action(
        current_state=current_state,
        export_blocked=export_blocked,
        disputed_total=disputed_total,
        violations_count=violations_count,
        validation_valid=validation_valid,
        export_ready=export_ready,
        disputed_rows=disputed,
    )

    # ── Сводка ──
    summary = _build_summary(
        confirmed_total=confirmed_total,
        disputed_total=disputed_total,
        violations_count=violations_count,
        export_blocked=export_blocked,
        export_ready=export_ready,
        total_revenue=total_revenue,
        avg_margin=avg_margin,
    )

    return PreviewReport(
        confirmed_total=confirmed_total,
        confirmed_rows_preview=confirmed_preview,
        confirmed_area_m2=confirmed_area_m2,
        disputed_total=disputed_total,
        disputed_rows_preview=disputed_preview,
        validation_valid=validation_valid,
        validation_violations=violations,
        validation_violations_count=violations_count,
        pricing_rows=pricing_rows,
        pricing_total_revenue=total_revenue,
        pricing_total_cost=total_cost,
        pricing_avg_margin_pct=avg_margin,
        pricing_is_profitable=is_profitable,
        export_blocked=export_blocked,
        export_block_reasons=export_block_reasons,
        export_ready=export_ready,
        current_state=current_state,
        current_state_label=current_state_label,
        next_safe_action=next_safe_action,
        summary=summary,
    )


# ── Рекомендация следующего действия ───────────────────────────

def _recommend_next_action(
    *,
    current_state: str,
    export_blocked: bool,
    disputed_total: int,
    violations_count: int,
    validation_valid: bool,
    export_ready: bool,
    disputed_rows: list[dict[str, Any]],
) -> str:
    """Сформировать текстовую рекомендацию для оператора."""

    if current_state == "RAW_INPUT":
        return "Необходимо разобрать сырые данные (выполнить парсинг)."
    if current_state == "PARSED":
        return "Необходимо запустить валидацию (transition_to_validated)."
    if current_state == "VALIDATED":
        if disputed_total > 0:
            rows_info = ", ".join(
                str(d.get("source_line", i + 1))
                for i, d in enumerate(disputed_rows[:5])
            )
            return f"Обнаружены спорные строки ({rows_info}). Запустите transition_to_disputed."
        return "Все строки чисты. Переведите статус в READY_FOR_PREVIEW (transition_to_preview)."
    if current_state == "HAS_DISPUTES":
        if export_blocked:
            detailed_disputes = ", ".join(
                f"{d.get('source_line', '?')}:{d.get('reason', '?')}"
                for d in disputed_rows[:5]
            )
            return (
                f"Необходим вызов диспут-резолвера для строк: {detailed_disputes}. "
                "После разрешения — transition_to_validated."
            )
        return "Необходимо разрешить спорные строки через DisputeResolver."
    if current_state == "EXPORT_BLOCKED":
        if disputed_total > 0:
            return (
                "Экспорт заблокирован из-за активных споров. "
                "Разрешите споры через DisputeResolver, затем transition_to_validated."
            )
        if not validation_valid:
            return (
                f"Экспорт заблокирован из-за {violations_count} нарушений валидации. "
                "Исправьте данные и повторите валидацию."
            )
        return "Экспорт заблокирован. Устраните все блокирующие факторы, затем transition_to_validated."
    if current_state == "READY_FOR_PREVIEW":
        return "Отчёт сформирован. Для одобрения выполните transition_to_export_ready."
    if current_state == "READY_FOR_FUTURE_EXPORT":
        return "Заказ готов к экспорту. Передайте в контур экспорта."

    return "Проверьте состояние заказа и выберите следующее действие."


# ── Сводка ─────────────────────────────────────────────────────

def _build_summary(
    *,
    confirmed_total: int,
    disputed_total: int,
    violations_count: int,
    export_blocked: bool,
    export_ready: bool,
    total_revenue: float,
    avg_margin: float,
) -> str:
    parts = [
        f"Строк: {confirmed_total} подтверждено"
    ]
    if disputed_total:
        parts.append(f"{disputed_total} спорно")
    if violations_count:
        parts.append(f"{violations_count} нарушений")

    if export_ready:
        parts.append("готов к экспорту")
    elif export_blocked:
        parts.append("экспорт заблокирован")
    else:
        parts.append("ожидает решения")

    parts.append(f"~{total_revenue:,.0f} руб")
    parts.append(f"маржа {avg_margin}%")

    return ". ".join(parts) + "."


# ── Markdown-формат ────────────────────────────────────────────

def preview_to_markdown(report: PreviewReport) -> str:
    """Преобразовать PreviewReport в markdown-строку."""

    lines: list[str] = []
    lines.append("# Preview Report — Hermes Clean")
    lines.append("")
    lines.append(f"**Состояние:** {report.current_state_label} (`{report.current_state}`)")
    lines.append("")

    # ── Блок 1: confirmed ──
    lines.append("## Подтверждённые строки")
    lines.append("")
    lines.append(f"- Всего: **{report.confirmed_total}**")
    lines.append(f"- Общая площадь: **{report.confirmed_area_m2:.4f} м²**")
    if report.confirmed_rows_preview:
        lines.append("")
        lines.append("| # | Высота (мм) | Ширина (мм) | Кол-во | Площадь (м²) |")
        lines.append("|---|------------|------------|-------|-------------|")
        for r in report.confirmed_rows_preview:
            lines.append(
                f"| {r['index']} | {r['height_mm']} | {r['width_mm']} "
                f"| {r['quantity']} | {r['area_m2']:.4f} |"
            )
    lines.append("")

    # ── Блок 2: disputed ──
    lines.append("## Спорные строки")
    lines.append("")
    if report.disputed_total > 0:
        lines.append(f"- Всего: **{report.disputed_total}**")
        lines.append("")
        lines.append("| ID | Строка | Причина | Текст |")
        lines.append("|----|--------|---------|-------|")
        for r in report.disputed_rows_preview:
            lines.append(
                f"| {r['dispute_id']} | {r['source_line']} "
                f"| {r['reason']} | `{r['raw_text'][:40]}` |"
            )
    else:
        lines.append("- Спорных строк нет.")
    lines.append("")

    # ── Блок 3: validation ──
    lines.append("## Валидация")
    lines.append("")
    if report.validation_valid:
        lines.append("- ✅ Валидация пройдена. Нарушений нет.")
    else:
        lines.append(f"- ❌ Нарушений: **{report.validation_violations_count}**")
        lines.append("")
        for v in report.validation_violations:
            lines.append(f"  - {v.get('message', v.get('reason', '?'))}")
    lines.append("")

    # ── Блок 4: pricing ──
    lines.append("## Стоимость (синтетическая)")
    lines.append("")
    lines.append(f"- Выручка: **{report.pricing_total_revenue:,.2f} руб**")
    lines.append(f"- Себестоимость: **{report.pricing_total_cost:,.2f} руб**")
    lines.append(f"- Средняя маржа: **{report.pricing_avg_margin_pct}%**")
    if report.pricing_is_profitable:
        lines.append("- ✅ Заказ рентабелен")
    else:
        lines.append("- ❌ Заказ нерентабелен (маржа ниже порога)")
    if report.pricing_rows:
        lines.append("")
        lines.append("| Площадь (м²) | Выручка | Себестоимость | Маржа |")
        lines.append("|-------------|---------|--------------|-------|")
        for p in report.pricing_rows:
            lines.append(
                f"| {p['area_m2']:.4f} | {p['revenue_rub']:>8.2f} руб "
                f"| {p['cost_rub']:>8.2f} руб | {p['margin_pct']:>5.1f}% |"
            )
    lines.append("")

    # ── Блок 5: export block reasons ──
    lines.append("## Экспорт")
    lines.append("")
    if report.export_blocked:
        lines.append("- ⛔ Экспорт заблокирован")
        for r in report.export_block_reasons:
            lines.append(f"  - {r}")
    elif report.export_ready:
        lines.append("- ✅ Экспорт разрешён")
    else:
        lines.append("- ⏳ Экспорт ожидает решения")
    lines.append("")

    # ── Блок 6: next safe action ──
    lines.append("## Рекомендация")
    lines.append("")
    lines.append(f"> {report.next_safe_action}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"*{report.summary}*")

    return "\n".join(lines)
