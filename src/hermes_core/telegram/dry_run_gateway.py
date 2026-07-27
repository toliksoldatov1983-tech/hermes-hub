from __future__ import annotations

from hermes_core.router import HermesRouter
from hermes_core.telegram.command_router import TelegramCommandRouter
from hermes_core.telegram.message_contract import TelegramDryRunResult, TelegramMessage
from hermes_core.types import ActionDecision, UserRequest


class TelegramDryRunGateway:
    def __init__(self, router: HermesRouter | None = None, command_router: TelegramCommandRouter | None = None) -> None:
        self.router = router or HermesRouter()
        self.command_router = command_router or TelegramCommandRouter()

    def simulate_incoming(self, message: TelegramMessage) -> TelegramDryRunResult:
        if message.text.strip().startswith("/"):
            command_response = self.command_router.route(message.text)
            return TelegramDryRunResult(
                command=command_response.command,
                planned_response=command_response.planned_response,
                blocked_actions=command_response.blocked_actions,
                warnings=command_response.warnings,
                next_step=command_response.next_step,
                payload=command_response.payload,
            )
        response = self.router.handle(UserRequest(text=message.text, channel="telegram_dry_run"))
        blocked = [a.description for a in response.planned_actions if response.decision is ActionDecision.BLOCKED]
        return TelegramDryRunResult(
            command="free_text",
            planned_response=response.text,
            blocked_actions=blocked,
            warnings=response.warnings,
            next_step=response.next_step or "No next step.",
            payload={},
        )
