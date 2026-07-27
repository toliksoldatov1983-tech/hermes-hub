"""Telegram Dialog Flow — замкнутый локальный сценарий диалога оператора.

Эмулирует цепочку состояний диалога без сетевого взаимодействия.
Всё на чистых функциях/классах. Без telebot/aiogram.

Цепочка:
  1. Ввод заказа (raw_text) → парсинг → state_machine
  2. Обнаружение споров → HAS_DISPUTES
  3. Уточняющие вопросы из dispute_resolver
  4. Исправление оператора → повторная валидация → preview
  5. Export blocked → пока споры не закрыты
  6. Итоговый отчёт
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from .validation import validate_order_result, validate_single_row
from .state_machine import OrderState, OrderStateMachine, STATE_LABELS
from .dispute_resolver import DisputeResolver, get_suggested_question
from .export_gate import build_export_model
from .preview_generator import generate_preview, preview_to_markdown


# ── Built-in парсер сырого текста ─────────────────────────────

def _parse_raw_text(raw_text: str) -> dict[str, Any]:
    """Разобрать сырой текст заказа в order_result.

    Парсит каждую строку:
    - 2 числа → candidate (height, width)
    - 3 числа → candidate (height, width, quantity)
    - текст → disputed (unparsed_order_text)
    - пустая строка → пропускается
    """
    lines = [l.strip() for l in raw_text.strip().split("\n") if l.strip()]
    confirmed_rows: list[dict[str, Any]] = []
    disputed_rows: list[dict[str, Any]] = []
    total_area_m2 = 0.0
    status = "clean"

    for i, line in enumerate(lines, start=1):
        parts = re.findall(r"-?\d+", line)

        if len(parts) == 2:
            h, w = int(parts[0]), int(parts[1])
            row = {
                "row_id": f"row-{i}",
                "height": h, "height_mm": h,
                "width": w, "width_mm": w,
                "quantity": 1,
                "source_line": i,
            }
            confirmed_rows.append(row)
            total_area_m2 += h * w / 1_000_000

        elif len(parts) == 3:
            h, w, q = int(parts[0]), int(parts[1]), int(parts[2])
            row = {
                "row_id": f"row-{i}",
                "height": h, "height_mm": h,
                "width": w, "width_mm": w,
                "quantity": q,
                "source_line": i,
            }
            confirmed_rows.append(row)
            total_area_m2 += h * w * q / 1_000_000

        elif len(parts) == 1:
            # Only one number — missing width/height
            disputed_rows.append({
                "dispute_id": f"dispute-{i}",
                "source_line": i,
                "raw_text": line,
                "reason": "missing_width" if len(line.split()) == 1 else "missing_width",
                "suggested_question": get_suggested_question("missing_width"),
            })
            if status == "clean":
                status = "has_disputes"

        elif len(parts) >= 4:
            # Too many numbers
            disputed_rows.append({
                "dispute_id": f"dispute-{i}",
                "source_line": i,
                "raw_text": line,
                "reason": "too_many_numbers",
                "suggested_question": get_suggested_question("too_many_numbers"),
            })
            if status == "clean":
                status = "has_disputes"

        else:
            # No numbers — text/garbage
            disputed_rows.append({
                "dispute_id": f"dispute-{i}",
                "source_line": i,
                "raw_text": line,
                "reason": "unparsed_order_text",
                "suggested_question": get_suggested_question("unparsed_order_text"),
            })
            if status == "clean":
                status = "has_disputes"

    if not confirmed_rows and not disputed_rows:
        status = "empty_or_invalid"
    elif not confirmed_rows and disputed_rows:
        status = "empty_or_invalid"  # весь заказ — неразбираемый текст
    elif not disputed_rows:
        status = "clean"

    return {
        "status": status,
        "confirmed_rows": confirmed_rows,
        "disputed_rows": disputed_rows,
        "total_area_m2": round(total_area_m2, 6),
    }


# ── Типы диалоговых сообщений ─────────────────────────────────

@dataclass
class DialogMessage:
    """Одно сообщение в диалоге."""

    role: str  # "operator" | "assistant" | "system"
    text: str
    step: str = ""


@dataclass
class DialogState:
    """Текущее состояние диалога."""

    phase: str
    """Текущая фаза: input / disputes / resolving / preview / blocked / done."""

    pending_questions: list[dict[str, Any]]
    """Список вопросов, ожидающих ответа оператора."""

    resolved_count: int
    """Количество разрешённых споров."""

    total_disputes: int
    """Общее количество спорных строк."""


# ── Эмулятор диалога ──────────────────────────────────────────

class TelegramDialogFlow:
    """Эмулятор диалога оператора с ИИ-помощником в Telegram.

    Всё локально. Без сетевого кода. Без библиотек Telegram.

    Использование:
        flow = TelegramDialogFlow()
        flow.receive_order("1000 400 2\\nмусор")
        flow.ask_questions()
        flow.resolve_dispute("dispute-2", {"action": "delete"})
        flow.show_preview()
        print(flow.get_last_message())
    """

    def __init__(self):
        self._order_result: dict[str, Any] = {}
        self._state_machine = OrderStateMachine()
        self._resolver = DisputeResolver()
        self._messages: list[DialogMessage] = []
        self._dialog_state = DialogState(
            phase="initial",
            pending_questions=[],
            resolved_count=0,
            total_disputes=0,
        )
        self._raw_text = ""

    # ── Свойства ──

    @property
    def messages(self) -> list[DialogMessage]:
        return list(self._messages)

    @property
    def state(self) -> DialogState:
        return self._dialog_state

    @property
    def order_result(self) -> dict[str, Any]:
        return dict(self._order_result)

    @property
    def state_machine(self) -> OrderStateMachine:
        return self._state_machine

    @property
    def current_state_name(self) -> str:
        return self._state_machine.state_label

    # ── 1. Ввод заказа ──

    def receive_order(self, raw_text: str) -> DialogMessage:
        """Принять сырой текстовый заказ. Разобрать и запустить state machine."""
        self._raw_text = raw_text

        # Парсинг
        self._order_result = _parse_raw_text(raw_text)
        status = self._order_result["status"]
        confirmed = self._order_result["confirmed_rows"]
        disputed = self._order_result["disputed_rows"]

        # State machine: RAW → PARSED
        self._state_machine.transition_to_parsed(
            confirmed_count=len(confirmed),
            disputed_count=len(disputed),
            raw_text_length=len(raw_text),
        )

        # Валидация
        validation = validate_order_result(self._order_result)

        # State machine: PARSED → VALIDATED или HAS_DISPUTES
        if disputed:
            self._state_machine.transition_to_disputed(
                dispute_count=len(disputed),
                dispute_reasons=[d.get("reason", "?") for d in disputed],
                validation_result=validation,
            )
            self._state_machine.transition_to_export_blocked(
                reason=f"Обнаружено {len(disputed)} спорных строк.",
            )
        else:
            self._state_machine.transition_to_validated(validation_result=validation)
            self._state_machine.transition_to_preview()

        # Диалоговый state
        self._dialog_state = DialogState(
            phase="input" if not disputed else "disputes",
            pending_questions=[
                {
                    "dispute_id": d["dispute_id"],
                    "source_line": d["source_line"],
                    "raw_text": d["raw_text"],
                    "reason": d["reason"],
                    "question": d.get("suggested_question", get_suggested_question(d["reason"])),
                }
                for d in disputed
            ],
            resolved_count=0,
            total_disputes=len(disputed),
        )

        # Формируем сообщение
        lines = [
            f"📦 Заказ принят.",
            f"✅ Подтверждено строк: {len(confirmed)}",
            f"📐 Площадь: {self._order_result['total_area_m2']:.4f} м²",
        ]

        if disputed:
            lines.append(f"⚠️ Спорных строк: {len(disputed)}")
            lines.append(f"⛔ Статус: {self._state_machine.state_label}")
            lines.append("")
            lines.append("Запустите ask_questions() для получения уточняющих вопросов.")
        else:
            lines.append(f"✅ Статус: {self._state_machine.state_label}")

        msg = "\n".join(lines)
        return self._add_message("assistant", msg, step="receive_order")

    # ── 2. Уточняющие вопросы ──

    def ask_questions(self) -> DialogMessage:
        """Выдать оператору варианты вопросов из dispute_resolver."""
        pending = self._dialog_state.pending_questions

        if not pending:
            return self._add_message(
                "assistant",
                "Нет ожидающих вопросов. Все споры разрешены.",
                step="ask_questions",
            )

        lines = ["❓ Уточняющие вопросы по спорным строкам:", ""]
        for q in pending:
            lines.append(f"  [{q['dispute_id']}] Строка {q['source_line']}: {q['raw_text']!r}")
            lines.append(f"      Причина: {q['reason']}")
            lines.append(f"      Вопрос: {q['question']}")
            lines.append("")

        lines.append("Доступные действия: accept , delete , clarify")
        lines.append("Пример: resolve_dispute('dispute-1', {'action': 'delete'})")

        self._dialog_state.phase = "resolving"
        return self._add_message("assistant", "\n".join(lines), step="ask_questions")

    # ── 3. Разрешение спора ──

    def resolve_dispute(
        self, dispute_id: str, resolution_data: dict[str, Any],
    ) -> DialogMessage:
        """Оператор отвечает на уточняющий вопрос. Resolver обрабатывает."""
        # Найти dispute
        pending = self._dialog_state.pending_questions
        target = None
        for q in pending:
            if q["dispute_id"] == dispute_id:
                target = q
                break

        if target is None:
            return self._add_message(
                "assistant",
                f"Спор {dispute_id} не найден или уже разрешён.",
                step="resolve_dispute",
            )

        # Найти disputed_row в order_result
        disputed_row = None
        for d in self._order_result.get("disputed_rows", []):
            if d["dispute_id"] == dispute_id:
                disputed_row = d
                break

        if disputed_row is None:
            disputed_row = {
                "dispute_id": dispute_id,
                "source_line": target["source_line"],
                "raw_text": target["raw_text"],
                "reason": target["reason"],
            }

        # Resolver
        outcome = self._resolver.resolve(disputed_row, resolution_data)

        if outcome.resolved:
            # Удаляем из pending
            self._dialog_state.pending_questions = [
                q for q in pending if q["dispute_id"] != dispute_id
            ]
            self._dialog_state.resolved_count += 1

            # Если был accept — добавляем confirmed_row
            if outcome.confirmed_row:
                self._order_result["confirmed_rows"].append(outcome.confirmed_row)
                self._order_result["total_area_m2"] = round(
                    self._order_result["total_area_m2"]
                    + outcome.confirmed_row["height"]
                    * outcome.confirmed_row["width"]
                    * outcome.confirmed_row["quantity"] / 1_000_000,
                    6,
                )

            # Обновляем disputed_rows (удаляем разрешённый)
            self._order_result["disputed_rows"] = [
                d for d in self._order_result.get("disputed_rows", [])
                if d["dispute_id"] != dispute_id
            ]

            # Добавляем new_disputes если split породил остатки
            for nd in outcome.new_disputes:
                self._order_result["disputed_rows"].append(nd)
                self._dialog_state.pending_questions.append({
                    "dispute_id": nd["dispute_id"],
                    "source_line": nd.get("source_line", "?"),
                    "raw_text": nd.get("raw_text", ""),
                    "reason": nd.get("reason", "?"),
                    "question": get_suggested_question(nd.get("reason", "")),
                })
                self._dialog_state.total_disputes += 1

            msg_parts = [
                f"✅ Спор {dispute_id} разрешён: {outcome.action}.",
            ]
            if outcome.note:
                msg_parts.append(f"   {outcome.note}")

            # Проверяем, все ли споры разрешены
            if not self._dialog_state.pending_questions:
                # Все споры закрыты → EXIT_BLOCKED → VALIDATED
                self._state_machine.reset(keep_history=True)
                self._state_machine.transition_to_parsed(
                    confirmed_count=len(self._order_result["confirmed_rows"]),
                    disputed_count=0,
                )
                validation = validate_order_result(self._order_result)
                self._state_machine.transition_to_validated(validation_result=validation)
                self._state_machine.transition_to_preview()

                # Пересчитываем order_result
                self._order_result["status"] = "clean"
                msg_parts.append("")
                msg_parts.append("🎉 Все споры разрешены!")
                msg_parts.append(f"✅ Статус: {self._state_machine.state_label}")
                msg_parts.append("Запустите show_preview() для просмотра отчёта.")
                self._dialog_state.phase = "done"

            return self._add_message("assistant", "\n".join(msg_parts), step="resolve_dispute")

        else:
            # Не удалось разрешить — нужна дополнительная информация
            msg = (
                f"⚠️ Спор {dispute_id} не разрешён: {outcome.action}.\n"
                f"   {outcome.note}\n\n"
                f"Попробуйте другое действие."
            )
            return self._add_message("assistant", msg, step="resolve_dispute")

    # ── 4. Preview ──

    def show_preview(self) -> DialogMessage:
        """Сгенерировать и показать preview report."""
        report = generate_preview(
            self._order_result,
            state_machine=self._state_machine,
        )
        md = preview_to_markdown(report)
        return self._add_message("assistant", md, step="show_preview")

    # ── 5. Статус экспорта ──

    def check_export_status(self) -> DialogMessage:
        """Проверить статус экспорта."""
        export = build_export_model(self._order_result)

        lines = ["📋 Статус экспорта:", ""]

        if export["export_blocked"]:
            lines.append("⛔ Экспорт ЗАБЛОКИРОВАН")
            lines.append(f"   Причина: {export['reason']}")
            lines.append(f"   Статус source: {export.get('source_status', '?')}")
            lines.append("")
            lines.append("Для разблокировки разрешите все споры.")
        else:
            lines.append("✅ Экспорт РАЗРЕШЁН")
            lines.append(f"   Строк к экспорту: {len(export.get('export_rows', []))}")

        lines.append("")
        lines.append(f"Состояние машины: {self._state_machine.state_label}")
        lines.append(f"Фаза диалога: {self._dialog_state.phase}")

        return self._add_message("assistant", "\n".join(lines), step="check_export_status")

    # ── 6. Финальный отчёт ──

    def show_final_report(self) -> DialogMessage:
        """Итоговый вывод отчёта (эмуляция сообщения в Telegram)."""
        order = self._order_result
        confirmed = order.get("confirmed_rows", [])
        disputed = order.get("disputed_rows", [])

        lines = [
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            "📋 ИТОГОВЫЙ ОТЧЁТ ПО ЗАКАЗУ",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            "",
            f"📦 Исходный текст: {self._raw_text[:80]}{'...' if len(self._raw_text) > 80 else ''}",
            "",
            f"✅ Подтверждено строк: {len(confirmed)}",
            f"📐 Общая площадь: {order.get('total_area_m2', 0):.4f} м²",
            f"⚠️ Спорных строк: {len(disputed)}",
            f"🔄 Разрешено: {self._dialog_state.resolved_count} / {self._dialog_state.total_disputes}",
            "",
        ]

        if confirmed:
            lines.append("Подтверждённые строки:")
            for r in confirmed:
                h = r.get("height_mm", r.get("height", "?"))
                w = r.get("width_mm", r.get("width", "?"))
                q = r.get("quantity", 1)
                lines.append(f"  📐 {h}×{w}×{q}  ({(h * w * q if isinstance(h, (int, float)) and isinstance(w, (int, float)) else 0) / 1_000_000:.4f} м²)")

        if disputed:
            lines.append("")
            lines.append("Спорные строки (нераспознанные):")
            for d in disputed:
                lines.append(f"  ⚠️ Строка {d.get('source_line', '?')}: {d.get('raw_text', '?')}  ({d.get('reason', '?')})")

        lines.append("")
        lines.append(f"🏁 Состояние: {self._state_machine.state_label}")
        lines.append(f"✅ Экспорт: {'разрешён' if not build_export_model(order)['export_blocked'] else 'заблокирован'}")

        if self._dialog_state.phase == "done":
            lines.append("")
            lines.append("🎉 Все споры разрешены. Заказ готов к дальнейшей обработке.")

        lines.append("")
        lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        return self._add_message("assistant", "\n".join(lines), step="show_final_report")

    # ── Сброс ──

    def reset(self) -> DialogMessage:
        """Сбросить диалог в начальное состояние."""
        self.__init__()
        return self._add_message("system", "🔄 Диалог сброшен. Введите новый заказ.", step="reset")

    # ── Вспомогательное ──

    def get_last_message(self) -> str:
        """Получить текст последнего сообщения ассистента."""
        for msg in reversed(self._messages):
            if msg.role == "assistant":
                return msg.text
        return ""

    def get_last_message_obj(self) -> DialogMessage | None:
        """Получить последнее сообщение."""
        for msg in reversed(self._messages):
            if msg.role == "assistant":
                return msg
        return None

    def _add_message(self, role: str, text: str, step: str = "") -> DialogMessage:
        msg = DialogMessage(role=role, text=text, step=step)
        self._messages.append(msg)
        return msg
