"""Local intent recognition for Free Entry / Intent Dispatcher.

Classifies free-text user messages into intents using only local signature
patterns (regex keyword matching, dimension patterns). No external AI/API
calls, no .env reads, no external database access.

Intents:
  - order    → заказ, размеры, фасады, детали
  - ideas    → обсуждение, идеи, предложения
  - engineer → инженер проекта, задачи, статус, отчёты
  - admin    → диагностика, админ (требует уточнения)
  - unknown  → намерение не определено, нужно уточнение
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class IntentResult:
    """Result of local free-text intent classification.

    Attributes:
        intent: Classified intent — order, ideas, engineer, admin, unknown.
        confidence: Confidence level 0.0–1.0.
        reason: Human-readable explanation of the classification.
        target_mode: Suggested Telegram mode for routing (None for unknown).
        clarify_question: Clarification question when intent is unknown.
        blocked: True if dangerous content was detected.
        block_message: Security block message text.
    """
    intent: str
    confidence: float
    reason: str
    target_mode: str | None = None
    clarify_question: str | None = None
    blocked: bool = False
    block_message: str | None = None

    def is_order(self) -> bool:
        return self.intent == INTENT_ORDER

    def is_ideas(self) -> bool:
        return self.intent == INTENT_IDEAS

    def is_engineer(self) -> bool:
        return self.intent == INTENT_ENGINEER

    def is_admin(self) -> bool:
        return self.intent == INTENT_ADMIN

    def is_unknown(self) -> bool:
        return self.intent == INTENT_UNKNOWN


# --- Intent constants ---

INTENT_ORDER = "order"
INTENT_IDEAS = "ideas"
INTENT_ENGINEER = "engineer"
INTENT_ADMIN = "admin"
INTENT_UNKNOWN = "unknown"

# --- Target mode constants ---

MODE_ORDER = "order"
MODE_IDEAS = "ideas"
MODE_ENGINEER = "engineer"
MODE_ADMIN = "admin"

# --- Thresholds ---

DEFAULT_CONFIDENCE_THRESHOLD = 0.7

# Gap below which the top two intents are considered too close
AMBIGUITY_GAP = 0.15

# --- Dangerous patterns (block immediately, do not route) ---

_DANGEROUS_PATTERNS: list[re.Pattern] = [
    re.compile(r'\.env\b'),
    re.compile(r'\btoken[s]?\b', re.IGNORECASE),
    re.compile(r'orders?\.db\b'),
    re.compile(r'\bbot\.py\b'),
    re.compile(r'\bgit\s+add\b'),
    re.compile(r'\bgit\s+commit\b'),
    re.compile(r'\bgit\s+push\b'),
]

# --- Stop phrases (greetings, single words — need clarification) ---

_STOP_PHRASES: list[re.Pattern] = [
    re.compile(r'^\s*привет\s*$', re.IGNORECASE),
    re.compile(r'^\s*здравствуй[те]?\s*$', re.IGNORECASE),
    re.compile(r'^\s*спасибо\s*$', re.IGNORECASE),
    re.compile(r'^\s*ок\s*$', re.IGNORECASE),
    re.compile(r'^\s*окей\s*$', re.IGNORECASE),
    re.compile(r'^\s*да\s*$', re.IGNORECASE),
    re.compile(r'^\s*нет\s*$', re.IGNORECASE),
    re.compile(r'^\s*пока\s*$', re.IGNORECASE),
    re.compile(r'^\s*добрый\s+день\s*$', re.IGNORECASE),
    re.compile(r'^\s*доброе\s+утро\s*$', re.IGNORECASE),
    re.compile(r'^\s*добрый\s+вечер\s*$', re.IGNORECASE),
]

# --- Dimension patterns ---

_DIMENSION_PATTERNS: list[re.Pattern] = [
    # 1000*400 or 1000*400*2
    re.compile(r'\d+\s*[*]\s*\d+'),
    # 1000 x 400 or 1000 x 400 x 2 (Latin and Cyrillic x, ×)
    re.compile(r'\d+\s*[xхXХ×]\s*\d+'),
    # Pure space-separated: "1000 400" or "1000 400 2" (whole text)
    re.compile(r'^\s*\d+\s+\d+(\s+\d+)?\s*$'),
    # Inline: "1000 400" within text but guarded to avoid false positives
    # with single numbers
    re.compile(r'(?<!\d)\d{3,5}\s+\d{2,4}(?:\s+\d+)?(?!\d)'),
]

# --- Keyword signatures with per-match weight ---

_ORDER_SIGNATURES: list[tuple[re.Pattern, float]] = [
    (re.compile(r'\bновый\s+заказ\b', re.IGNORECASE), 0.80),
    (re.compile(r'\bзаказ\b', re.IGNORECASE), 0.75),
    (re.compile(r'\bфасад\b', re.IGNORECASE), 0.70),
    (re.compile(r'\bдеталь\b', re.IGNORECASE), 0.70),
    (re.compile(r'\bразмер', re.IGNORECASE), 0.70),
    (re.compile(r'\bприми\b', re.IGNORECASE), 0.60),
    (re.compile(r'\bпринять\b', re.IGNORECASE), 0.55),
    (re.compile(r'\bоформи\b', re.IGNORECASE), 0.55),
    (re.compile(r'\bнов[ыо]е?\b', re.IGNORECASE), 0.15),  # "новый заказ" handled above
    (re.compile(r'\bсделай\b', re.IGNORECASE), 0.15),  # weak alone
    (re.compile(r'\bсделать\b', re.IGNORECASE), 0.15),  # weak alone
    (re.compile(r'\bраспиши\b', re.IGNORECASE), 0.40),
    (re.compile(r'\bэксель\b', re.IGNORECASE), 0.55),
    (re.compile(r'\bexcel\b', re.IGNORECASE), 0.55),
    (re.compile(r'\bкорел\b', re.IGNORECASE), 0.75),
    (re.compile(r'\bcorel\b', re.IGNORECASE), 0.75),
]

_IDEAS_SIGNATURES: list[tuple[re.Pattern, float]] = [
    (re.compile(r'\bиде[яиюй]\b', re.IGNORECASE), 0.75),
    (re.compile(r'\bдавай\b', re.IGNORECASE), 0.25),
    (re.compile(r'\bобсудим\b', re.IGNORECASE), 0.70),
    (re.compile(r'\bподумать\b', re.IGNORECASE), 0.65),
    (re.compile(r'\bподумай\b', re.IGNORECASE), 0.55),
    (re.compile(r'\bкак\s+думаешь\b', re.IGNORECASE), 0.60),
    (re.compile(r'\bа\s+что\s+если\b', re.IGNORECASE), 0.70),
    (re.compile(r'\bпредлагаю\b', re.IGNORECASE), 0.70),
    (re.compile(r'\bпредложение\b', re.IGNORECASE), 0.70),
    (re.compile(r'\bулучшени', re.IGNORECASE), 0.65),
    (re.compile(r'\bоптимизаци', re.IGNORECASE), 0.70),
    (re.compile(r'\bпоговорить\b', re.IGNORECASE), 0.55),
    (re.compile(r'\bпоговори\b', re.IGNORECASE), 0.55),
    (re.compile(r'\bдумаю\b', re.IGNORECASE), 0.30),
    (re.compile(r'\bинтервью\b', re.IGNORECASE), 0.60),
    (re.compile(r'\bопрос', re.IGNORECASE), 0.50),
]

_ENGINEER_SIGNATURES: list[tuple[re.Pattern, float]] = [
    (re.compile(r'\bстатус\b', re.IGNORECASE), 0.75),
    (re.compile(r'\bчто\s+сделано\b', re.IGNORECASE), 0.80),
    (re.compile(r'\bследующий\s+шаг\b', re.IGNORECASE), 0.80),
    (re.compile(r'\bпроверь\b', re.IGNORECASE), 0.60),
    (re.compile(r'\bпроверить\b', re.IGNORECASE), 0.60),
    (re.compile(r'\bпроверка\b', re.IGNORECASE), 0.60),
    (re.compile(r'\bотчёт\b', re.IGNORECASE), 0.75),
    (re.compile(r'\bотчет\b', re.IGNORECASE), 0.75),
    (re.compile(r'\bзадача\b', re.IGNORECASE), 0.70),
    (re.compile(r'\bзадачи\b', re.IGNORECASE), 0.70),
    (re.compile(r'\bэтап\b', re.IGNORECASE), 0.70),
    (re.compile(r'\bзадание\b', re.IGNORECASE), 0.70),
    (re.compile(r'\bинженер\b', re.IGNORECASE), 0.75),
    (re.compile(r'\bплан\b', re.IGNORECASE), 0.55),
    (re.compile(r'\bтехническое\s+задание\b', re.IGNORECASE), 0.80),
    (re.compile(r'\bhermes\b', re.IGNORECASE), 0.70),
    (re.compile(r'\bcodex\b', re.IGNORECASE), 0.70),
]

_ADMIN_SIGNATURES: list[tuple[re.Pattern, float]] = [
    (re.compile(r'\bадмин\b', re.IGNORECASE), 0.55),
    (re.compile(r'\bдиагностик\b', re.IGNORECASE), 0.55),
    (re.compile(r'\bпроверь\s+режим\b', re.IGNORECASE), 0.55),
    (re.compile(r'\bсброс\b', re.IGNORECASE), 0.40),
    (re.compile(r'\bсбрось\b', re.IGNORECASE), 0.40),
    (re.compile(r'\bдиагностика\b', re.IGNORECASE), 0.55),
]

# --- Clarification question text ---

_CLARIFICATION_QUESTION: str = (
    "Я не совсем понял, что вы хотите сделать. Выберите:\n\n"
    "🧾 Новый заказ\n"
    "💬 Идея / обсуждение\n"
    "🛠 Инженер проекта\n"
    "← Отмена"
)

# ======================================================================
# Internal helpers
# ======================================================================


def _check_dangerous(text: str) -> str | None:
    """Check if text contains dangerous substrings.

    Returns a block message string if dangerous content is found,
    or None if the text is safe.
    """
    for pattern in _DANGEROUS_PATTERNS:
        if pattern.search(text):
            return (
                "⚠️ Обнаружено упоминание служебных файлов или команд. "
                "Этот запрос заблокирован по соображениям безопасности."
            )
    return None


def _is_stop_phrase(text: str) -> bool:
    """Return True if text is a greeting, thank-you, or other stop word.

    These are too short or generic for reliable intent classification.
    """
    stripped = text.strip()
    if not stripped or len(stripped) < 2:
        return True
    for pattern in _STOP_PHRASES:
        if pattern.search(text):
            return True
    return False


def _has_dimension_pattern(text: str) -> bool:
    """Return True if text contains patterns that look like dimensions.

    Matches:
      - 1000*400, 1000*400*2
      - 1000 x 400, 1000 x 400 x 2
      - "1000 400" (whole text) or inline large numbers
    """
    for pattern in _DIMENSION_PATTERNS:
        if pattern.search(text):
            return True
    return False


def _score_intent(text: str, signatures: list[tuple[re.Pattern, float]]) -> float:
    """Score text against a set of weighted signature patterns.

    Returns the capped sum of matched weights (max 1.0).
    """
    score = 0.0
    for pattern, weight in signatures:
        if pattern.search(text):
            score += weight
    return min(score, 1.0)


def _build_unknown(text: str) -> IntentResult:
    """Build an unknown-intent result with a clarification question."""
    return IntentResult(
        intent=INTENT_UNKNOWN,
        confidence=0.0,
        reason="Намерение не определено. Требуется уточнение.",
        target_mode=None,
        clarify_question=_CLARIFICATION_QUESTION,
    )


# ======================================================================
# Public API
# ======================================================================


def classify_intent(text: str) -> IntentResult:
    """Classify free-text user message into an intent using local signatures.

    This is the main entry point for local intent recognition.

    No external AI/API calls, no .env reads, no external database access.

    Args:
        text: Raw user message text.

    Returns:
        IntentResult with classification details.
    """
    text = text.strip()

    # --- Empty text ---
    if not text:
        return _build_unknown(text)

    # --- Step 1: Dangerous content check ---
    block_msg = _check_dangerous(text)
    if block_msg is not None:
        return IntentResult(
            intent=INTENT_UNKNOWN,
            confidence=0.0,
            reason="Заблокировано: опасное содержимое.",
            target_mode=None,
            clarify_question=None,
            blocked=True,
            block_message=block_msg,
        )

    # --- Step 2: Stop / greeting phrases ---
    if _is_stop_phrase(text):
        return _build_unknown(text)

    # --- Step 3: Dimension detection ---
    has_dimensions = _has_dimension_pattern(text)

    # --- Step 4: Score each intent category ---
    order_score = _score_intent(text, _ORDER_SIGNATURES)
    ideas_score = _score_intent(text, _IDEAS_SIGNATURES)
    engineer_score = _score_intent(text, _ENGINEER_SIGNATURES)
    admin_score = _score_intent(text, _ADMIN_SIGNATURES)

    # Boost order confidence if dimensions are present
    if has_dimensions:
        order_score = max(0.85, min(order_score + 0.5, 1.0))

    # Build scored list
    candidates = [
        (INTENT_ORDER, order_score, MODE_ORDER, "заказ"),
        (INTENT_IDEAS, ideas_score, MODE_IDEAS, "идеи"),
        (INTENT_ENGINEER, engineer_score, MODE_ENGINEER, "инженер"),
        (INTENT_ADMIN, admin_score, MODE_ADMIN, "админ"),
    ]
    candidates.sort(key=lambda x: x[1], reverse=True)

    best_intent, best_conf, best_mode, best_label = candidates[0]
    second_conf = candidates[1][1]

    # --- Step 5: Apply clarification rules ---

    # 5a. All scores below threshold
    if best_conf < DEFAULT_CONFIDENCE_THRESHOLD:
        return _build_unknown(text)

    # 5b. Admin intent — always clarify unless very confident
    if best_intent == INTENT_ADMIN and best_conf < 0.85:
        return _build_unknown(text)

    # 5c. Top two intents too close (< AMBIGUITY_GAP difference)
    if (best_conf - second_conf) < AMBIGUITY_GAP and best_conf < 0.9:
        return _build_unknown(text)

    # --- Step 6: Build result ---
    reason_parts = []
    if best_intent == INTENT_ORDER and has_dimensions:
        reason_parts.append("Обнаружены размеры")
    reason_parts.append(f"Ключевые слова: {best_label} ({best_conf:.2f})")

    return IntentResult(
        intent=best_intent,
        confidence=best_conf,
        reason=". ".join(reason_parts),
        target_mode=best_mode,
        clarify_question=None,
    )
