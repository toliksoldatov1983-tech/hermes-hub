"""Order State Machine — жизненный цикл заказа.

Управляет переходами между состояниями на основе результатов
валидации и наличия диспутов. Без Telegram, API, БД, секретов.

Состояния:
  RAW_INPUT → PARSED → VALIDATED → READY_FOR_PREVIEW → READY_FOR_FUTURE_EXPORT
                    ↘ HAS_DISPUTES → EXPORT_BLOCKED
                                   ↘ VALIDATED (после разрешения споров)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto
from typing import Any


# ── Состояния ──────────────────────────────────────────────────

class OrderState(Enum):
    """Все возможные состояния заказа."""

    RAW_INPUT = auto()
    """Начальное состояние. Сырые данные получены, ещё не разобраны."""

    PARSED = auto()
    """Данные успешно разобраны в структуры (confirmed_rows, disputed_rows)."""

    VALIDATED = auto()
    """Заказ прошёл все проверки валидации. Нет нарушений."""

    HAS_DISPUTES = auto()
    """Обнаружены спорные строки или расхождения. Требуется resolve."""

    READY_FOR_PREVIEW = auto()
    """Сформирован корректный результат для предварительного просмотра."""

    EXPORT_BLOCKED = auto()
    """Шлюз закрыт. Экспорт физически невозможен (диспуты / нет аппрува)."""

    READY_FOR_FUTURE_EXPORT = auto()
    """Все споры разрешены. Заказ ждёт отправки в контур экспорта."""


# ── Типы данных ────────────────────────────────────────────────

@dataclass(frozen=True)
class StateTransition:
    """Запись одного перехода между состояниями."""

    from_state: OrderState
    to_state: OrderState
    trigger: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    reason: str = ""
    data: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class StateMachineResult:
    """Результат операции над state machine."""

    success: bool
    current_state: OrderState
    transition: StateTransition | None = None
    message: str = ""


# ── Карта разрешённых переходов ────────────────────────────────

_ALLOWED_TRANSITIONS: dict[OrderState, set[OrderState]] = {
    OrderState.RAW_INPUT: {OrderState.PARSED},
    OrderState.PARSED: {OrderState.VALIDATED, OrderState.HAS_DISPUTES},
    OrderState.VALIDATED: {OrderState.READY_FOR_PREVIEW, OrderState.HAS_DISPUTES},
    OrderState.HAS_DISPUTES: {OrderState.VALIDATED, OrderState.EXPORT_BLOCKED},
    OrderState.EXPORT_BLOCKED: {OrderState.VALIDATED},
    OrderState.READY_FOR_PREVIEW: {OrderState.READY_FOR_FUTURE_EXPORT,
                                    OrderState.HAS_DISPUTES},
    OrderState.READY_FOR_FUTURE_EXPORT: set(),  # терминальное
}


# ── Human-readable labels ──────────────────────────────────────

STATE_LABELS: dict[OrderState, str] = {
    OrderState.RAW_INPUT: "Сырые данные",
    OrderState.PARSED: "Разобрано",
    OrderState.VALIDATED: "Валидировано",
    OrderState.HAS_DISPUTES: "Есть споры",
    OrderState.READY_FOR_PREVIEW: "Готово к просмотру",
    OrderState.EXPORT_BLOCKED: "Экспорт заблокирован",
    OrderState.READY_FOR_FUTURE_EXPORT: "Готово к экспорту",
}


# ── State Machine ──────────────────────────────────────────────

class OrderStateMachine:
    """Машина состояний заказа.

    Использование:
        sm = OrderStateMachine()
        sm.transition_to_parsed(confirmed_count=3, disputed_count=0)
        sm.transition_to_validated(validation_result=...)
        sm.transition_to_preview()
        sm.transition_to_export_ready(approved_by="user")
    """

    def __init__(self, initial_state: OrderState = OrderState.RAW_INPUT):
        self._state = initial_state
        self._history: list[StateTransition] = []
        self._data: dict[str, Any] = {}

    # ── Свойства ──

    @property
    def state(self) -> OrderState:
        return self._state

    @property
    def state_label(self) -> str:
        return STATE_LABELS.get(self._state, str(self._state))

    @property
    def history(self) -> list[StateTransition]:
        return list(self._history)

    @property
    def data(self) -> dict[str, Any]:
        return dict(self._data)

    @property
    def is_terminal(self) -> bool:
        return self._state == OrderState.READY_FOR_FUTURE_EXPORT

    @property
    def can_export(self) -> bool:
        return self._state == OrderState.READY_FOR_FUTURE_EXPORT

    # ── Внутренний метод перехода ──

    def _transition(
        self, target: OrderState, trigger: str,
        reason: str = "", data: dict[str, Any] | None = None,
    ) -> StateMachineResult:
        if self._state == target:
            return StateMachineResult(
                success=True,
                current_state=self._state,
                message=f"Уже в состоянии {STATE_LABELS.get(target, target.name)}.",
            )

        allowed = _ALLOWED_TRANSITIONS.get(self._state, set())
        if target not in allowed:
            return StateMachineResult(
                success=False,
                current_state=self._state,
                message=(
                    f"Переход {STATE_LABELS.get(self._state, self._state.name)} → "
                    f"{STATE_LABELS.get(target, target.name)} запрещён."
                ),
            )

        transition = StateTransition(
            from_state=self._state,
            to_state=target,
            trigger=trigger,
            reason=reason,
            data=data or {},
        )
        self._history.append(transition)
        self._state = target
        if data:
            self._data.update(data)

        return StateMachineResult(
            success=True,
            current_state=self._state,
            transition=transition,
            message=f"Переход в {STATE_LABELS.get(target, target.name)} выполнен.",
        )

    # ── Публичные методы переходов ──

    def transition_to_parsed(
        self, *,
        confirmed_count: int = 0,
        disputed_count: int = 0,
        raw_text_length: int = 0,
    ) -> StateMachineResult:
        """RAW_INPUT → PARSED. Данные разобраны."""
        return self._transition(
            OrderState.PARSED, "parse",
            reason="Сырые данные разобраны в структуры.",
            data={
                "confirmed_count": confirmed_count,
                "disputed_count": disputed_count,
                "raw_text_length": raw_text_length,
            },
        )

    def transition_to_validated(
        self, *,
        validation_result: dict[str, Any] | None = None,
    ) -> StateMachineResult:
        """PARSED или HAS_DISPUTES или EXPORT_BLOCKED → VALIDATED."""
        violations_count = 0
        valid = True
        if validation_result:
            violations_count = len(validation_result.get("violations", []))
            valid = validation_result.get("valid", True)

        reason = "Валидация пройдена." if valid else f"Нарушений: {violations_count}."
        return self._transition(
            OrderState.VALIDATED, "validate",
            reason=reason,
            data={
                "valid": valid,
                "violations_count": violations_count,
                **(validation_result or {}),
            },
        )

    def transition_to_disputed(
        self, *,
        dispute_count: int = 0,
        dispute_reasons: list[str] | None = None,
        validation_result: dict[str, Any] | None = None,
    ) -> StateMachineResult:
        """PARSED или VALIDATED → HAS_DISPUTES."""
        return self._transition(
            OrderState.HAS_DISPUTES, "detect_disputes",
            reason=f"Обнаружено {dispute_count} спорных строк.",
            data={
                "dispute_count": dispute_count,
                "dispute_reasons": dispute_reasons or [],
                **(validation_result or {}),
            },
        )

    def transition_to_preview(self) -> StateMachineResult:
        """VALIDATED → READY_FOR_PREVIEW."""
        return self._transition(
            OrderState.READY_FOR_PREVIEW, "prepare_preview",
            reason="Сформирован результат для предварительного просмотра.",
        )

    def transition_to_export_blocked(
        self, *,
        reason: str = "",
    ) -> StateMachineResult:
        """HAS_DISPUTES → EXPORT_BLOCKED. Шлюз закрыт."""
        return self._transition(
            OrderState.EXPORT_BLOCKED, "block_export",
            reason=reason or "Экспорт заблокирован из-за активных споров.",
        )

    def transition_to_export_ready(
        self, *,
        approved_by: str = "system",
    ) -> StateMachineResult:
        """READY_FOR_PREVIEW → READY_FOR_FUTURE_EXPORT. Финальное состояние."""
        return self._transition(
            OrderState.READY_FOR_FUTURE_EXPORT, "approve_export",
            reason="Все споры разрешены. Заказ готов к экспорту.",
            data={"approved_by": approved_by},
        )

    # ── Составной метод: полный цикл RAW → EXPORT_READY ──

    def run_full_cycle(
        self,
        *,
        raw_text: str = "",
        parse_result: dict[str, Any] | None = None,
        validation_result: dict[str, Any] | None = None,
        preview_approved_by: str = "system",
    ) -> list[StateMachineResult]:
        """Выполнить полный цикл от RAW_INPUT до READY_FOR_FUTURE_EXPORT.

        Возвращает список результатов всех переходов.
        """
        results: list[StateMachineResult] = []

        # 1. Parse
        confirmed = len(parse_result.get("confirmed_rows", [])) if parse_result else 0
        disputed = len(parse_result.get("disputed_rows", [])) if parse_result else 0
        r1 = self.transition_to_parsed(
            confirmed_count=confirmed,
            disputed_count=disputed,
            raw_text_length=len(raw_text),
        )
        results.append(r1)
        if not r1.success:
            return results

        # 2. Route: disputed or validated
        has_disputes = disputed > 0 or (
            validation_result and not validation_result.get("valid", True)
        )
        if has_disputes:
            r2 = self.transition_to_disputed(
                dispute_count=disputed,
                dispute_reasons=[
                    d.get("reason", "?")
                    for d in (parse_result or {}).get("disputed_rows", [])
                ],
                validation_result=validation_result,
            )
            results.append(r2)
            if not r2.success:
                return results

            # 3. Block export
            r3 = self.transition_to_export_blocked(
                reason="Обнаружены спорные строки.",
            )
            results.append(r3)
            return results

        # 2b. Validated
        r2 = self.transition_to_validated(validation_result=validation_result)
        results.append(r2)
        if not r2.success:
            return results

        # 3. Preview
        r3 = self.transition_to_preview()
        results.append(r3)
        if not r3.success:
            return results

        # 4. Export ready
        r4 = self.transition_to_export_ready(approved_by=preview_approved_by)
        results.append(r4)

        return results

    # ── Сброс ──

    def reset(self, keep_history: bool = False) -> None:
        """Сбросить машину в RAW_INPUT."""
        if not keep_history:
            self._history.clear()
            self._data.clear()
        self._state = OrderState.RAW_INPUT
