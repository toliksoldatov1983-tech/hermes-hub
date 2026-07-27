"""Memory Sync — единый реестр решений, запретов и правил безопасности.

Агрегирует, сохраняет и синхронизирует:
- PROJECT_DECISIONS — принятые архитектурные и рабочие решения
- PROJECT_PROHIBITIONS — жёсткие запреты (никакой внешней сети, реальных ключей)
- Pending approvals — шаги, ожидающие ручной верификации
- Safety rules — общие правила безопасности
- Решения подсистем: Malyarka, AI provider, Telegram

Любая попытка записать решение, нарушающее запрет или safety rule,
блокируется с генерацией SafetyViolation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto
from typing import Any


# ── Исключение безопасности ───────────────────────────────────

class SafetyViolation(Exception):
    """Возбуждается при попытке нарушить PROJECT_PROHIBITIONS или safety rules."""

    def __init__(self, message: str, rule_key: str = ""):
        super().__init__(message)
        self.rule_key = rule_key


# ── Типы данных ───────────────────────────────────────────────

class Subsystem(Enum):
    """Подсистемы, для которых хранятся решения."""
    GENERAL = auto()
    MALYARKA = auto()
    AI_PROVIDER = auto()
    TELEGRAM = auto()
    EXPORT = auto()


@dataclass(frozen=True)
class Decision:
    """Одно принятое решение."""

    key: str
    value: Any
    subsystem: Subsystem = Subsystem.GENERAL
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    reason: str = ""
    immutable: bool = False
    """Если True — решение нельзя изменить после записи."""


@dataclass(frozen=True)
class Prohibition:
    """Один жёсткий запрет."""

    key: str
    description: str
    pattern: str
    """Ключевое слово/паттерн для проверки (например, 'network', 'api_key')."""

    severity: str = "error"
    """error / warning"""

    reason: str = ""


@dataclass(frozen=True)
class SafetyRule:
    """Одно правило безопасности."""

    key: str
    description: str
    check: str
    """Описание проверки."""


@dataclass
class PendingApproval:
    """Шаг, ожидающий ручной верификации."""

    id: str
    description: str
    subsystem: str = "general"
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    approved: bool = False
    approved_at: datetime | None = None
    approved_by: str = ""


@dataclass(frozen=True)
class IntegrityReport:
    """Отчёт о целостности реестра."""

    total_decisions: int
    total_prohibitions: int
    total_safety_rules: int
    pending_approvals: int
    violations_found: int
    violations: list[str]
    is_consistent: bool


# ── Реестр памяти ─────────────────────────────────────────────

class MemorySync:
    """Единый локальный реестр решений, запретов и правил.

    Использование:
        ms = MemorySync()
        ms.add_decision("architecture", "clean", Subsystem.MALYARKA)
        ms.add_decision("use_network", True)  # → SafetyViolation!
    """

    # ── Запреты по умолчанию ──
    _DEFAULT_PROHIBITIONS = [
        Prohibition(
            key="no_external_network",
            description="Запрещено сетевое взаимодействие из изолированного контура.",
            pattern="network",
            severity="error",
            reason="Hermes-Clean — локальный контур без сети.",
        ),
        Prohibition(
            key="no_real_api_keys",
            description="Запрещено использовать реальные API-ключи в коде.",
            pattern="api_key",
            severity="error",
            reason="Все секреты хранятся строго вне изолированного контура.",
        ),
        Prohibition(
            key="no_real_tokens",
            description="Запрещено хранить или передавать токены аутентификации.",
            pattern="token",
            severity="error",
            reason="Токены не должны покидать защищённое хранилище.",
        ),
        Prohibition(
            key="no_database_write",
            description="Запрещена прямая запись в БД заказов из этого контура.",
            pattern="db_write",
            severity="error",
            reason="База данных заказов — production-компонент.",
        ),
        Prohibition(
            key="no_live_telegram",
            description="Запрещено отправлять сообщения в реальный Telegram.",
            pattern="telegram_send",
            severity="warning",
            reason="Telegram-интеграция только через эмулятор диалога.",
        ),
    ]

    # ── Правила безопасности по умолчанию ──
    _DEFAULT_SAFETY_RULES = [
        SafetyRule(
            key="no_secrets_in_code",
            description="Все секреты и ключи хранятся строго в .env или переменных окружения, никогда в коде.",
            check="Ни одно значение не должно содержать 'api_key', 'token', 'secret', 'password' в коде.",
        ),
        SafetyRule(
            key="validate_before_export",
            description="Экспорт возможен только после прохождения валидации.",
            check="Перед вызовом build_export_model() должен быть вызван validate_order_result().",
        ),
        SafetyRule(
            key="approval_for_blocked",
            description="Разблокировка экспорта требует ручного подтверждения.",
            check="Состояние EXPORT_BLOCKED → разрешение споров → approval → VALIDATED.",
        ),
        SafetyRule(
            key="single_contour",
            description="Весь код работает в изолированном контуре без внешних зависимостей.",
            check="Никаких import telebot, aiogram, requests, httpx.",
        ),
        SafetyRule(
            key="no_production_touch",
            description="Запрещено изменять production-данные: .env, orders.db, реальные заказы.",
            check="Работа только с синтетическими фикстурами и изолированными данными.",
        ),
    ]

    def __init__(self):
        self._decisions: dict[str, Decision] = {}
        self._prohibitions: dict[str, Prohibition] = {}
        self._safety_rules: dict[str, SafetyRule] = {}
        self._pending_approvals: dict[str, PendingApproval] = {}
        self._subsystem_decisions: dict[Subsystem, dict[str, Decision]] = {}

        # Инициализация запретов и правил по умолчанию
        for p in self._DEFAULT_PROHIBITIONS:
            self._prohibitions[p.key] = p
        for r in self._DEFAULT_SAFETY_RULES:
            self._safety_rules[r.key] = r

    # ── Свойства ──

    @property
    def decisions(self) -> dict[str, Decision]:
        return dict(self._decisions)

    @property
    def prohibitions(self) -> dict[str, Prohibition]:
        return dict(self._prohibitions)

    @property
    def safety_rules(self) -> dict[str, SafetyRule]:
        return dict(self._safety_rules)

    @property
    def pending_approvals(self) -> list[PendingApproval]:
        return [a for a in self._pending_approvals.values() if not a.approved]

    @property
    def all_approvals(self) -> list[PendingApproval]:
        return list(self._pending_approvals.values())

    # ── Проверка на violation ──

    def _check_violation(self, key: str, value: Any, subsystem: Subsystem) -> None:
        """Проверить, не нарушает ли решение запреты или safety rules.

        Возбуждает SafetyViolation если нарушение обнаружено.
        """
        str_value = str(value).lower()
        str_key = key.lower()

        # Проверка по запретам
        for p in self._prohibitions.values():
            if p.pattern in str_key or p.pattern in str_value:
                raise SafetyViolation(
                    f"Запрет '{p.key}': {p.description} "
                    f"(обнаружено: '{p.pattern}' в '{key}={value}'). "
                    f"Причина: {p.reason}",
                    rule_key=p.key,
                )

        # Проверка по safety rules (блокирующие)
        # rule 1: secrets in code
        if subsystem != Subsystem.AI_PROVIDER:  # AI provider может обсуждать ключи
            secrets_patterns = ["api_key", "token", "secret", "password"]
            for pat in secrets_patterns:
                if pat in str_key or pat in str_value:
                    raise SafetyViolation(
                        f"Safety rule 'no_secrets_in_code': "
                        f"обнаружен паттерн '{pat}' в '{key}={value}'. "
                        f"{self._safety_rules['no_secrets_in_code'].description}",
                        rule_key="no_secrets_in_code",
                    )

    # ── Добавление решения ──

    def add_decision(
        self,
        key: str,
        value: Any,
        subsystem: Subsystem = Subsystem.GENERAL,
        *,
        reason: str = "",
        immutable: bool = False,
        skip_violation_check: bool = False,
    ) -> Decision:
        """Добавить решение. Проверяет violation если не skip.

        Raises:
            SafetyViolation: если решение нарушает запрет или safety rule.
        """
        if not skip_violation_check:
            self._check_violation(key, value, subsystem)

        decision = Decision(
            key=key,
            value=value,
            subsystem=subsystem,
            reason=reason,
            immutable=immutable,
        )

        # Если уже есть immutable — нельзя перезаписать
        if key in self._decisions and self._decisions[key].immutable:
            raise SafetyViolation(
                f"Решение '{key}' помечено как immutable. Изменение запрещено.",
                rule_key="immutable_decision",
            )

        self._decisions[key] = decision

        if subsystem not in self._subsystem_decisions:
            self._subsystem_decisions[subsystem] = {}
        self._subsystem_decisions[subsystem][key] = decision

        return decision

    # ── Получение решений ──

    def get_decision(self, key: str) -> Decision | None:
        return self._decisions.get(key)

    def get_subsystem_decisions(self, subsystem: Subsystem) -> dict[str, Decision]:
        return dict(self._subsystem_decisions.get(subsystem, {}))

    # ── Добавление запрета ──

    def add_prohibition(
        self,
        key: str,
        description: str,
        pattern: str,
        *,
        severity: str = "error",
        reason: str = "",
    ) -> Prohibition:
        """Добавить новый запрет."""
        if key in self._prohibitions:
            raise SafetyViolation(
                f"Запрет '{key}' уже существует. "
                f"Запреты нельзя перезаписывать.",
                rule_key="prohibition_exists",
            )

        prohibition = Prohibition(
            key=key, description=description, pattern=pattern,
            severity=severity, reason=reason,
        )
        self._prohibitions[key] = prohibition
        return prohibition

    # ── Добавление правила безопасности ──

    def add_safety_rule(self, key: str, description: str, check: str) -> SafetyRule:
        """Добавить новое правило безопасности."""
        if key in self._safety_rules:
            raise SafetyViolation(
                f"Safety rule '{key}' уже существует.",
                rule_key="safety_rule_exists",
            )

        rule = SafetyRule(key=key, description=description, check=check)
        self._safety_rules[key] = rule
        return rule

    # ── Pending approvals ──

    def request_approval(
        self, step_id: str, description: str, subsystem: str = "general",
    ) -> PendingApproval:
        """Добавить шаг, требующий ручной верификации."""
        if step_id in self._pending_approvals:
            raise ValueError(f"Approval '{step_id}' already exists.")

        approval = PendingApproval(
            id=step_id, description=description, subsystem=subsystem,
        )
        self._pending_approvals[step_id] = approval
        return approval

    def approve(self, step_id: str, approved_by: str = "user") -> PendingApproval:
        """Подтвердить шаг верификации."""
        if step_id not in self._pending_approvals:
            raise ValueError(f"Approval '{step_id}' not found.")

        approval = self._pending_approvals[step_id]
        approval.approved = True
        approval.approved_at = datetime.now(timezone.utc)
        approval.approved_by = approved_by
        return approval

    def reject_approval(self, step_id: str) -> None:
        """Отклонить и удалить шаг верификации."""
        if step_id not in self._pending_approvals:
            raise ValueError(f"Approval '{step_id}' not found.")
        del self._pending_approvals[step_id]

    # ── Integrity check ──

    def check_integrity(self) -> IntegrityReport:
        """Проверить целостность всего реестра."""
        violations: list[str] = []

        # Проверка: все решения не нарушают текущие запреты
        for key, decision in self._decisions.items():
            try:
                self._check_violation(key, decision.value, decision.subsystem)
            except SafetyViolation as e:
                violations.append(str(e))

        # Проверка: immutable решения не изменились
        # (они уже защищены в add_decision)

        # Проверка: pending approvals
        pending = self.pending_approvals
        unapproved = [a for a in self.all_approvals if not a.approved]

        return IntegrityReport(
            total_decisions=len(self._decisions),
            total_prohibitions=len(self._prohibitions),
            total_safety_rules=len(self._safety_rules),
            pending_approvals=len(pending),
            violations_found=len(violations),
            violations=violations,
            is_consistent=len(violations) == 0,
        )

    # ── Экспорт/импорт JSON ──

    def to_dict(self) -> dict[str, Any]:
        """Экспортировать весь реестр в словарь."""
        return {
            "decisions": {
                k: {
                    "key": d.key,
                    "value": d.value,
                    "subsystem": d.subsystem.name,
                    "timestamp": d.timestamp.isoformat(),
                    "reason": d.reason,
                    "immutable": d.immutable,
                }
                for k, d in self._decisions.items()
            },
            "prohibitions": {
                k: {
                    "key": p.key,
                    "description": p.description,
                    "pattern": p.pattern,
                    "severity": p.severity,
                    "reason": p.reason,
                }
                for k, p in self._prohibitions.items()
            },
            "safety_rules": {
                k: {
                    "key": r.key,
                    "description": r.description,
                    "check": r.check,
                }
                for k, r in self._safety_rules.items()
            },
            "pending_approvals": [
                {
                    "id": a.id,
                    "description": a.description,
                    "subsystem": a.subsystem,
                    "created_at": a.created_at.isoformat(),
                    "approved": a.approved,
                }
                for a in self._pending_approvals.values()
            ],
            "subsystem_decisions": {
                s.name: list(d.keys())
                for s, d in self._subsystem_decisions.items()
            },
        }

    # ── Дашборд ──

    def render_dashboard(self) -> str:
        """Вывести состояние реестра в консоль."""
        lines: list[str] = []
        lines.append("┌─────────────────────────────────────────────────────────────┐")
        lines.append("│              MEMORY SYNC DASHBOARD                         │")
        lines.append("├─────────────────────────────────────────────────────────────┤")
        lines.append(f"│ Decisions:        {len(self._decisions):<3}                                          │")
        lines.append(f"│ Prohibitions:     {len(self._prohibitions):<3}                                          │")
        lines.append(f"│ Safety Rules:     {len(self._safety_rules):<3}                                          │")
        lines.append(f"│ Pending Approvals: {len(self.pending_approvals):<3}                                          │")
        lines.append("├─────────────────────────────────────────────────────────────┤")

        subs = self._subsystem_decisions
        if subs:
            lines.append("│ Subsystem decisions:                                        │")
            for s, d in subs.items():
                names = ", ".join(d.keys()) if d else "—"
                lines.append(f"│   {s.name:<20} {names:<37} │")

        integrity = self.check_integrity()
        if integrity.is_consistent:
            lines.append("├─────────────────────────────────────────────────────────────┤")
            lines.append("│ ✅ Integrity: CONSISTENT                                    │")
        else:
            lines.append("├─────────────────────────────────────────────────────────────┤")
            lines.append(f"│ ❌ Integrity: {integrity.violations_found} VIOLATION(S)                            │")
            for v in integrity.violations[:2]:
                lines.append(f"│   • {v[:55]:<55} │")

        lines.append("└─────────────────────────────────────────────────────────────┘")
        return "\n".join(lines)
