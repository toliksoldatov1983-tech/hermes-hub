# CODEX_DEEPSEEK_REVIEW_LOOP

Codex writes code.

DeepSeek / DeepSig reviews.

Review findings are returned to Codex. Codex edits or rejects findings.

Maximum review/fix cycles: 2. Dangerous review suggestions are blocked by safety gate.

## Implemented local contract

- Review provider factory selects mock or disabled providers.
- Every review result has `can_edit_project=False`.
- Disabled real providers return `blocked_reason`.
- Cycle 2 returns `Review cycle limit reached.`
