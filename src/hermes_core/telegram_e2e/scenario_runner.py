"""E2E Scenario Runner — runs multi-turn scenarios and reports results.

All dry-run. No Telegram API. No tokens.
"""

from __future__ import annotations

from hermes_core.telegram_e2e.scenario_contract import E2EScenario, E2EStep, E2EResult, E2EStepStatus
from hermes_core.telegram_memory import ContextAwareRouter, get_memory_store
from hermes_core.telegram_memory.conversation_memory import ConversationMode


class E2EScenarioRunner:
    """Runs end-to-end dry-run scenarios."""

    def __init__(self) -> None:
        self._store = get_memory_store()

    def run_scenario(self, scenario: E2EScenario, session_id: str = "") -> E2EResult:
        """Run a single scenario and return results."""
        sid = session_id or f"e2e-{scenario.scenario_id}"
        self._store.reset_session(sid)
        router = ContextAwareRouter(self._store)

        result = E2EResult(scenario_id=scenario.scenario_id, total_steps=len(scenario.steps))

        for i, step in enumerate(scenario.steps):
            step.status = E2EStepStatus.RUNNING

            try:
                resp = router.route(step.user_message, session_id=sid)

                # Check intent
                intent_match = (not step.expected_mode) or (
                    resp.session_state.get("mode", "") == step.expected_mode
                )

                # Check blocked
                blocked_match = step.expected_blocked == bool(resp.blocked_reason)

                # Check draft status
                draft_match = True
                if step.expected_draft_status:
                    draft_match = bool(resp.draft_state) and (
                        resp.draft_state.get("status", "") == step.expected_draft_status
                    )

                step_ok = intent_match and blocked_match and draft_match

                if step_ok:
                    step.status = E2EStepStatus.PASSED
                    result.passed_steps += 1
                else:
                    step.status = E2EStepStatus.FAILED
                    result.failed_steps += 1
                    if not intent_match:
                        result.errors.append(f"Step {i+1}: expected mode={step.expected_mode}, got={resp.session_state.get('mode')}")
                    if not blocked_match:
                        result.errors.append(f"Step {i+1}: expected blocked={step.expected_blocked}, got={bool(resp.blocked_reason)}")
                    if not draft_match:
                        got = resp.draft_state.get("status") if resp.draft_state else "no draft"
                        result.errors.append(f"Step {i+1}: expected draft={step.expected_draft_status}, got={got}")

                # Transcript
                result.transcript.append(f"[{step.status.value.upper()}] User: {step.user_message[:60]}")
                if resp.blocked_reason:
                    result.transcript.append(f"  Bot: BLOCKED — {resp.blocked_reason[:80]}")
                else:
                    result.transcript.append(f"  Bot: {resp.text[:100]}")
                result.transcript.append(f"  Mode: {resp.session_state.get('mode', '?')} | Draft: {resp.draft_state.get('status') if resp.draft_state else 'none'}")

            except Exception as e:
                step.status = E2EStepStatus.FAILED
                result.failed_steps += 1
                result.errors.append(f"Step {i+1}: exception — {e}")

            if step.status == E2EStepStatus.BLOCKED:
                result.blocked_steps += 1

        # Final state
        session = self._store.get_session(sid)
        if session:
            result.final_mode = session.mode.value

        result.passed = result.failed_steps == 0
        return result

    def run_all(self, scenarios: list[E2EScenario]) -> list[E2EResult]:
        """Run all scenarios and return results."""
        return [self.run_scenario(s) for s in scenarios]

    def run_all_and_report(self, scenarios: list[E2EScenario]) -> tuple[list[E2EResult], str]:
        results = self.run_all(scenarios)
        total = sum(r.total_steps for r in results)
        passed = sum(r.passed_steps for r in results)
        failed = sum(r.failed_steps for r in results)
        report = f"E2E Results: {passed}/{total} steps passed"
        if failed:
            report += f", {failed} failed"
        return results, report
