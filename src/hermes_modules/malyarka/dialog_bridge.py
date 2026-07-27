from __future__ import annotations

from dataclasses import dataclass, field

from hermes_modules.malyarka.dispute_questions import questions_for_order
from hermes_modules.malyarka.export_contract import export_blocked_until_confirmed
from hermes_modules.malyarka.order_contract import MalyarkaOrder
from hermes_modules.malyarka.parser_contract import ParserContract
from hermes_modules.malyarka.preview_contract import build_preview
from hermes_modules.malyarka.validation_contract import validate_order


SAFE_BLOCKED_ACTIONS = (
    "live_telegram_send",
    "telegram_token_read",
    "external_api_call",
    "real_order_access",
    "file_export_write",
)


@dataclass(frozen=True)
class DialogBridgeResult:
    command: str
    status: str
    message: str
    confirmed_rows: int
    pending_disputes: int
    resolved_disputes: int
    export_ready: bool
    main_module: str = "hermes_modules.malyarka"
    blocked_actions: tuple[str, ...] = SAFE_BLOCKED_ACTIONS


@dataclass
class MalyarkaDialogBridgeSession:
    parser: ParserContract = field(default_factory=ParserContract)
    order: MalyarkaOrder | None = None
    resolved_disputes: int = 0

    def run(self, line: str) -> DialogBridgeResult:
        stripped = line.strip()
        if not stripped:
            return self._result("empty", "blocked", "Пустая команда.")

        command, _, payload = stripped.partition(" ")
        command = command.lower()

        if command == "/order":
            return self._order(payload)
        if command == "/questions":
            return self._questions()
        if command == "/resolve-delete":
            return self._resolve_delete(payload)
        if command == "/resolve-all-delete":
            return self._resolve_all_delete()
        if command == "/preview":
            return self._preview()
        if command == "/export":
            return self._export()
        if command == "/report":
            return self._report()
        if command == "/reset":
            self.order = None
            self.resolved_disputes = 0
            return self._result(command, "ok", "Сессия сброшена.")
        if command == "/help":
            return self._result(command, "ok", self.help_text())

        return self._result(command, "blocked", f"Неизвестная команда: {command}")

    @staticmethod
    def help_text() -> str:
        return (
            "Команды: /order <item | quantity | unit> | /questions | "
            "/resolve-delete <row_number> | /resolve-all-delete | /preview | /export | /report | /reset"
        )

    def _order(self, payload: str) -> DialogBridgeResult:
        if not payload.strip():
            return self._result("/order", "blocked", "Нужен текст заказа.")
        self.order = self.parser.parse(payload.replace("\\n", "\n"))
        validation = validate_order(self.order)
        if validation.blocked:
            return self._result(
                "/order",
                "ok",
                f"Заказ принят. Подтверждено: {validation.confirmed_count}; спорных строк: {validation.disputed_count}.",
            )
        return self._result("/order", "ok", "Заказ принят. Спорных строк нет.")

    def _questions(self) -> DialogBridgeResult:
        if self.order is None:
            return self._result("/questions", "blocked", "Сначала нужен /order.")
        questions = questions_for_order(self.order)
        if not questions:
            return self._result("/questions", "ok", "Спорных строк нет.")
        lines = ["Вопросы по спорным строкам:"]
        for question in questions:
            lines.append(f"[{question.row_number}] {question.raw_text} — {question.question}")
        return self._result("/questions", "ok", " ".join(lines))

    def _resolve_delete(self, payload: str) -> DialogBridgeResult:
        if self.order is None:
            return self._result("/resolve-delete", "blocked", "Сначала нужен /order.")
        try:
            row_number = int(payload.strip())
        except ValueError:
            return self._result("/resolve-delete", "blocked", "Нужен номер спорной строки.")
        return self._delete_disputed_rows({row_number})

    def _resolve_all_delete(self) -> DialogBridgeResult:
        if self.order is None:
            return self._result("/resolve-all-delete", "blocked", "Сначала нужен /order.")
        row_numbers = {index for index, row in enumerate(self.order.rows, start=1) if not row.is_confirmed}
        if not row_numbers:
            return self._result("/resolve-all-delete", "ok", "Спорных строк нет.")
        return self._delete_disputed_rows(row_numbers)

    def _delete_disputed_rows(self, row_numbers: set[int]) -> DialogBridgeResult:
        assert self.order is not None
        kept = []
        removed = 0
        for index, row in enumerate(self.order.rows, start=1):
            if index in row_numbers and not row.is_confirmed:
                removed += 1
                continue
            kept.append(row)
        if removed == 0:
            return self._result("/resolve-delete", "blocked", "Спорная строка не найдена.")
        self.order = MalyarkaOrder(source_text=self.order.source_text, rows=kept)
        self.resolved_disputes += removed
        return self._result("/resolve-delete", "ok", f"Спорные строки удалены в dry-run: {removed}.")

    def _preview(self) -> DialogBridgeResult:
        if self.order is None:
            return self._result("/preview", "blocked", "Сначала нужен /order.")
        preview = build_preview(self.order)
        return self._result(
            "/preview",
            "ok",
            f"Preview: confirmed={preview['confirmed_count']}; disputed={preview['disputed_count']}; final_ready={preview['final_ready']}.",
        )

    def _export(self) -> DialogBridgeResult:
        if self.order is None:
            return self._result("/export", "blocked", "Сначала нужен /order.")
        status = export_blocked_until_confirmed(self.order, approved=True, source_type="synthetic")
        result_status = "ok" if status.startswith("READY:") else "blocked"
        return self._result("/export", result_status, status)

    def _report(self) -> DialogBridgeResult:
        if self.order is None:
            return self._result("/report", "blocked", "Сначала нужен /order.")
        validation = validate_order(self.order)
        export = export_blocked_until_confirmed(self.order, approved=True, source_type="synthetic")
        return self._result(
            "/report",
            "ok",
            f"Итог: confirmed={validation.confirmed_count}; disputed={validation.disputed_count}; export={export}",
        )

    def _result(self, command: str, status: str, message: str) -> DialogBridgeResult:
        confirmed = len(self.order.confirmed_rows) if self.order else 0
        disputed = len(self.order.disputed_rows) if self.order else 0
        export_ready = bool(self.order and self.order.final_ready and confirmed > 0)
        return DialogBridgeResult(
            command=command,
            status=status,
            message=message,
            confirmed_rows=confirmed,
            pending_disputes=disputed,
            resolved_disputes=self.resolved_disputes,
            export_ready=export_ready,
        )


def run_dialog_bridge_script(lines: list[str]) -> list[DialogBridgeResult]:
    session = MalyarkaDialogBridgeSession()
    return [session.run(line) for line in lines]
