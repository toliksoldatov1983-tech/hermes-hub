"""Task Queue — локальная очередь задач с контролем целостности.

Гарантирует:
- NEXT_TASK всегда валиден
- DONE обновляется атомарно
- ACTIVE_BATCH не отстаёт от прогресса
- pending approvals видны
- audit перехватывает нарушения последовательности
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto
from typing import Any


# ── Статусы задачи ────────────────────────────────────────────

class TaskStatus(Enum):
    PENDING = auto()
    ACTIVE = auto()
    COMPLETED = auto()
    CANCELLED = auto()
    BLOCKED = auto()


# ── Типы данных ───────────────────────────────────────────────

@dataclass(frozen=True)
class Task:
    """Одна задача в очереди."""

    id: str
    """Уникальный ID задачи (например, 'BATCH_077')."""

    name: str
    """Человекочитаемое название."""

    order: int
    """Порядковый номер в очереди (1-based)."""

    deps: tuple[str, ...] = ()
    """ID задач, которые должны быть выполнены перед этой."""

    requires_approval: bool = False
    """True если задача требует ручного подтверждения."""

    description: str = ""
    """Описание задачи."""


@dataclass
class TaskRecord:
    """Запись задачи в очереди с состоянием."""

    task: Task
    status: TaskStatus = TaskStatus.PENDING
    approved: bool = False
    completed_at: datetime | None = None
    block_reason: str = ""
    result: str = ""


@dataclass(frozen=True)
class AuditViolation:
    """Нарушение целостности, обнаруженное аудитом."""

    severity: str  # error / warning
    message: str
    task_id: str = ""


# ── Очередь задач ─────────────────────────────────────────────

class TaskQueue:
    """Очередь задач с контролем последовательности и целостности.

    Использование:
        q = TaskQueue.create_default()
        q.activate_next()          # активировать BATCH_063
        q.complete_current("OK")   # завершить
        q.activate_next()          # активировать следующий
        print(q.render_dashboard())
        print(q.audit())
    """

    def __init__(self, tasks: list[Task]):
        if not tasks:
            raise ValueError("Очередь не может быть пустой.")

        # Проверка уникальности ID
        ids = [t.id for t in tasks]
        if len(ids) != len(set(ids)):
            raise ValueError(f"Обнаружены дубликаты ID задач: {ids}")

        # Проверка последовательности order
        orders = sorted(t.order for t in tasks)
        expected = list(range(1, len(tasks) + 1))
        if orders != expected:
            raise ValueError(
                f"Порядок задач нарушен: ожидалось {expected}, получено {orders}"
            )

        # Проверка deps: все зависимости должны существовать
        known_ids = set(ids)
        for t in tasks:
            for dep in t.deps:
                if dep not in known_ids:
                    raise ValueError(
                        f"Задача {t.id} зависит от {dep}, "
                        f"но {dep} не найдена в очереди."
                    )

        # Проверка deps: зависимости должны иметь меньший order
        task_by_id = {t.id: t for t in tasks}
        for t in tasks:
            for dep in t.deps:
                if task_by_id[dep].order >= t.order:
                    raise ValueError(
                        f"Задача {t.id} (order={t.order}) зависит от {dep} "
                        f"(order={task_by_id[dep].order}), "
                        f"но зависимость должна выполняться раньше."
                    )

        self._records: list[TaskRecord] = [TaskRecord(task=t) for t in sorted(tasks, key=lambda x: x.order)]
        self._done: list[TaskRecord] = []
        self._current: TaskRecord | None = None

    # ── Свойства ──

    @property
    def current(self) -> TaskRecord | None:
        return self._current

    @property
    def current_task_label(self) -> str:
        if self._current:
            return f"{self._current.task.id}: {self._current.task.name}"
        return "—"

    @property
    def done(self) -> list[TaskRecord]:
        return list(self._done)

    @property
    def pending(self) -> list[TaskRecord]:
        return [r for r in self._records if r.status == TaskStatus.PENDING]

    @property
    def all_records(self) -> list[TaskRecord]:
        """Все записи задач, без дублирования выполненных."""
        done_ids = {r.task.id for r in self._done}
        return self._done + [r for r in self._records if r.task.id not in done_ids]

    @property
    def progress(self) -> str:
        total = len(self.all_records)
        done_count = len(self._done)
        pct = round(done_count / total * 100, 1) if total else 0
        return f"{done_count}/{total} ({pct}%)"

    @property
    def next_task_id(self) -> str | None:
        """ID следующей задачи, которая должна быть активирована."""
        for r in self._records:
            if r.status == TaskStatus.PENDING:
                return r.task.id
        return None

    # ── Активация следующей задачи ──

    def activate_next(self) -> str:
        """Активировать следующую задачу в очереди.

        Проверяет:
        - Все deps выполнены
        - Нет пропущенных задач (разрыв в order)
        - Задача не заблокирована
        """
        # Если есть текущая незавершённая — нельзя
        if self._current and self._current.status == TaskStatus.ACTIVE:
            return (
                f"ОШИБКА: задача {self._current.task.id} ещё активна. "
                f"Завершите её перед активацией следующей."
            )

        pending = self.pending
        if not pending:
            return "ОШИБКА: нет ожидающих задач. Все задачи выполнены."

        next_record = pending[0]

        # Проверка целостности: нет ли пропущенных задач?
        expected_order = (len(self._done) + 1)
        if next_record.task.order != expected_order:
            return (
                f"КРИТИЧЕСКАЯ ОШИБКА: ожидалась задача order={expected_order}, "
                f"но следующая pending задача — {next_record.task.id} (order={next_record.task.order}). "
                f"Обнаружен разрыв в последовательности!"
            )

        # Проверка зависимостей
        done_ids = {r.task.id for r in self._done}
        for dep_id in next_record.task.deps:
            if dep_id not in done_ids:
                return (
                    f"ОШИБКА: задача {next_record.task.id} требует выполнения "
                    f"{dep_id}, но она не завершена."
                )

        # Проверка: если требуется approval — отмечаем
        if next_record.task.requires_approval and not next_record.approved:
            next_record.status = TaskStatus.PENDING
            return (
                f"ОЖИДАНИЕ: задача {next_record.task.id} требует подтверждения. "
                f"Вызовите approve_current() перед активацией."
            )

        next_record.status = TaskStatus.ACTIVE
        self._current = next_record
        return f"✅ Активирована: {next_record.task.id} — {next_record.task.name}."

    # ── Завершение текущей задачи ──

    def complete_current(self, result: str = "") -> str:
        """Завершить текущую активную задачу. Атомарно перенести в DONE."""
        if not self._current:
            return "ОШИБКА: нет активной задачи для завершения."

        if self._current.status != TaskStatus.ACTIVE:
            return (
                f"ОШИБКА: задача {self._current.task.id} в статусе "
                f"{self._current.status.name}, невозможно завершить."
            )

        self._current.status = TaskStatus.COMPLETED
        self._current.completed_at = datetime.now(timezone.utc)
        self._current.result = result

        task_id = self._current.task.id
        task_name = self._current.task.name

        # Атомарный перенос в DONE
        self._done.append(self._current)
        self._current = None

        return f"✅ Завершена: {task_id} — {task_name}. Результат: {result or 'OK'}."

    # ── Подтверждение (approval) ──

    def approve_current(self) -> str:
        """Подтвердить текущую (или следующую pending) задачу."""
        target = self._current
        if not target:
            pending = self.pending
            if not pending:
                return "ОШИБКА: нет задач для подтверждения."
            target = pending[0]

        if not target.task.requires_approval:
            return (
                f"ПРЕДУПРЕЖДЕНИЕ: задача {target.task.id} не требует подтверждения. "
                f"Пропускаю."
            )

        target.approved = True
        return f"✅ Задача {target.task.id} подтверждена."

    # ── Блокировка ──

    def block_current(self, reason: str = "") -> str:
        """Заблокировать текущую активную задачу."""
        if not self._current:
            return "ОШИБКА: нет активной задачи для блокировки."

        self._current.status = TaskStatus.BLOCKED
        self._current.block_reason = reason or "Заблокирована вручную."
        self._current = None

        return (
            f"⛔ Задача {self._current.task.id if self._current else '?'} заблокирована. "
            f"Причина: {reason or 'не указана'}."
        )

    # ── Отмена ──

    def cancel_current(self) -> str:
        """Отменить текущую активную задачу."""
        if not self._current:
            return "ОШИБКА: нет активной задачи для отмены."

        task_id = self._current.task.id
        self._current.status = TaskStatus.CANCELLED
        self._done.append(self._current)
        self._current = None

        return f"❌ Задача {task_id} отменена."

    # ── Дашборд ──

    def render_dashboard(self) -> str:
        """Вывести текущее состояние очереди в консоль."""
        lines: list[str] = []
        lines.append("┌─────────────────────────────────────────────────────────────┐")
        lines.append("│              TASK QUEUE DASHBOARD                          │")
        lines.append("├─────────────────────────────────────────────────────────────┤")
        lines.append(f"│ Progress: {self.progress:<56}│")
        lines.append(f"│ Current:  {self.current_task_label:<56}│")
        lines.append(f"│ Next:     {self.next_task_id or '—':<56}│")
        lines.append("├─────────────────────────────────────────────────────────────┤")
        lines.append("│ Tasks:                                                      │")

        for r in self.all_records:
            status_char = {
                TaskStatus.PENDING: "⏳",
                TaskStatus.ACTIVE: "▶️ ",
                TaskStatus.COMPLETED: "✅",
                TaskStatus.CANCELLED: "❌",
                TaskStatus.BLOCKED: "⛔",
            }.get(r.status, "❓")

            approval = "🔒" if (r.task.requires_approval and not r.approved) else "  "
            deps_str = f" ← {','.join(r.task.deps)}" if r.task.deps else ""
            note = ""
            if r.status == TaskStatus.BLOCKED and r.block_reason:
                note = f" [{r.block_reason}]"
            if r.status == TaskStatus.COMPLETED and r.result:
                note = f" ({r.result})"

            lines.append(
                f"│  {status_char} {approval} #{r.task.order:02d} {r.task.id:<16} "
                f"{r.task.name:<30}{deps_str}{note} │"
            )

        lines.append("└─────────────────────────────────────────────────────────────┘")
        return "\n".join(lines)

    # ── Аудит целостности ──

    def audit(self) -> list[AuditViolation]:
        """Проверить целостность всей очереди.

        Возвращает список нарушений (пустой = всё чисто).
        """
        violations: list[AuditViolation] = []
        done_ids = {r.task.id for r in self._done}

        # 1. Проверка: все задачи на месте (нет пропущенных order)
        all_records = self.all_records
        expected_order = 1
        for r in all_records:
            if r.task.order != expected_order:
                violations.append(AuditViolation(
                    severity="error",
                    message=f"Разрыв последовательности: ожидался order={expected_order}, "
                            f"но {r.task.id} имеет order={r.task.order}.",
                    task_id=r.task.id,
                ))
                break
            expected_order += 1

        # 2. Проверка: deps выполнены
        for r in all_records:
            if r.status == TaskStatus.PENDING:
                for dep_id in r.task.deps:
                    if dep_id not in done_ids:
                        violations.append(AuditViolation(
                            severity="error",
                            message=f"Задача {r.task.id} зависит от {dep_id}, "
                                    f"но {dep_id} не выполнена.",
                            task_id=r.task.id,
                        ))

        # 3. Проверка: ACTIVE_BATCH соответствует прогрессу
        if self._current:
            # Текущая активная должна быть следующей по порядку
            expected_active_order = len(self._done) + 1
            if self._current.task.order != expected_active_order:
                violations.append(AuditViolation(
                    severity="warning",
                    message=f"ACTIVE_BATCH не синхронизирован: активна задача "
                            f"order={self._current.task.order}, "
                            f"но ожидается order={expected_active_order}.",
                    task_id=self._current.task.id,
                ))

        # 4. Проверка: pending approvals
        for r in all_records:
            if r.task.requires_approval and not r.approved and r.status == TaskStatus.ACTIVE:
                violations.append(AuditViolation(
                    severity="warning",
                    message=f"Задача {r.task.id} активна, но не подтверждена.",
                    task_id=r.task.id,
                ))

        # 5. Проверка: нет заблокированных без причины
        for r in all_records:
            if r.status == TaskStatus.BLOCKED and not r.block_reason:
                violations.append(AuditViolation(
                    severity="warning",
                    message=f"Задача {r.task.id} заблокирована без указания причины.",
                    task_id=r.task.id,
                ))

        return violations

    def audit_report(self) -> str:
        """Сформировать отчёт аудита."""
        violations = self.audit()
        if not violations:
            return "✅ Аудит пройден. Нарушений целостности не обнаружено."

        lines = ["📋 ОТЧЁТ АУДИТА ОЧЕРЕДИ ЗАДАЧ", "=" * 60, ""]
        errors = [v for v in violations if v.severity == "error"]
        warnings = [v for v in violations if v.severity == "warning"]

        if errors:
            lines.append(f"🔴 ОШИБКИ ({len(errors)}):")
            for v in errors:
                lines.append(f"  • [{v.task_id}] {v.message}")
            lines.append("")

        if warnings:
            lines.append(f"🟡 ПРЕДУПРЕЖДЕНИЯ ({len(warnings)}):")
            for v in warnings:
                lines.append(f"  • [{v.task_id}] {v.message}")
            lines.append("")

        lines.append(f"Итого: {len(errors)} ошибок, {len(warnings)} предупреждений.")
        return "\n".join(lines)


# ── Фабрика: стандартная очередь Hermes-Clean ──────────────────

def create_default_queue() -> TaskQueue:
    """Создать очередь задач по умолчанию (BATCH_063–076)."""
    tasks = [
        Task(id="BATCH_063C", name="Базовый перенос компонентов",
             order=1, description="validation, fixtures, dispute, export"),
        Task(id="BATCH_073", name="Ревизия и документирование",
             order=2, deps=("BATCH_063C",),
             description="5 docs/ артефактов"),
        Task(id="BATCH_074", name="Машина состояний",
             order=3, deps=("BATCH_063C",),
             description="OrderStateMachine, 7 состояний"),
        Task(id="BATCH_075", name="Preview Report",
             order=4, deps=("BATCH_074",),
             description="6 блоков, synthetic pricing"),
        Task(id="BATCH_076", name="Telegram Dialog Flow",
             order=5, deps=("BATCH_075",),
             description="Эмулятор диалога, 6 шагов"),
        Task(id="BATCH_077", name="Task Queue + Auto Next",
             order=6, deps=("BATCH_076",),
             description="Очередь задач, аудит, дашборд",
             requires_approval=True),
        Task(id="BATCH_078", name="TBD — следующий пакет",
             order=7, deps=("BATCH_077",),
             description="По согласованию с пользователем",
             requires_approval=True),
    ]
    return TaskQueue(tasks)
