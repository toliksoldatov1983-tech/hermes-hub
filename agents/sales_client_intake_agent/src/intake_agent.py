"""
Sales + Client Intake Agent — offline Python module.

BUNDLE: SALES_CLIENT_INTAKE_AGENT_OFFLINE_PYTHON_MODULE
Status: accepted (not active)

Edge-case hardened 2026-06-17:
- material_raw vs material_confirmed
- color_raw vs color_structured (RAL/NCS)
- location (renamed from city), supports СПб, Алматы, Астана
- surface_finish_raw
- Stricter ready_for_malyarka: discount/tech/manager block handoff
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Specific materials (confirmed, not ambiguous)
CONFIRMED_MATERIALS: List[str] = [
    "мдф", "mdf",
    "шпон", "шпона",
    "массив",
    "металл", "металла",
    "пластик", "пластика",
    "дсп", "двп", "лдсп",
    "фанера", "фанеры",
    "акрил", "акрила",
    "стекло", "стекла",
]

# Ambiguous materials — need clarification
AMBIGUOUS_MATERIALS: List[str] = [
    "дерево", "дерева",
]

COLOR_INDICATORS: List[str] = [
    "ral", "ncs",
    "белый", "белого", "белая", "белые",
    "чёрный", "черный", "чёрного", "черного",
    "серый", "серого",
    "коричневый", "коричневого",
    "красный", "красного",
    "синий", "синего",
    "зелёный", "зеленый", "зелёного",
    "жёлтый", "желтый",
    "бежевый", "бежевого",
    "матовый", "матового", "мат", "матов",
    "глянцевый", "глянцевого", "глянец", "гланц",
    "прозрачный",
    "кофе", "шоколад", "венге", "дуб", "орех", "ясень",
]

URGENCY_WORDS: List[str] = [
    "срочно", "срочный", "срочная",
    "очень срочно",
    "вчера",
    "как можно быстрее", "как можно скорее",
    "горит",
]

DISCOUNT_WORDS: List[str] = [
    "скидка", "скидку", "скидки", "скидкой",
    "подешевле", "дешевле",
    "цена", "стоимость", "сколько стоит", "почём",
]

TECHNICAL_QUESTION_WORDS: List[str] = [
    "что лучше", "какой лучше", "какая лучше",
    "посоветуйте", "порекомендуйте", "рекомендаци",
]

# Missing specification indicators (not technical advice)
MISSING_SPEC_WORDS: List[str] = [
    "фрезеровк", "фрезер",
]

DEADLINE_QUESTION_WORDS: List[str] = [
    "срок", "сроки", "когда", "за сколько",
    "как долго", "сколько времени",
]

SIZE_PATTERN: re.Pattern = re.compile(
    r"(\d+)\s*[xXхХ×*]\s*(\d+)(?:\s+(\d+))?|"
    r"(\d+)\s+(\d+)(?:\s+(\d+))?",
)

RAL_PATTERN: re.Pattern = re.compile(r"RAL\s*(\d{3,4})", re.IGNORECASE)
NCS_PATTERN: re.Pattern = re.compile(r"NCS\s*(S?\s*\d{4}-[A-Z]\d{0,2}[A-Z]?)", re.IGNORECASE)


# ---------------------------------------------------------------------------
# 1. analyze_client_message(text) -> dict
# ---------------------------------------------------------------------------


def analyze_client_message(text: str) -> Dict[str, Any]:
    """Analyze a raw client message and extract structured information."""
    text_lower = text.lower().strip()

    result: Dict[str, Any] = {
        "raw_text": text,
        "items": [],
        "has_sizes": False,
        "has_material": False,
        "has_color": False,
        "has_quantity": False,
        "has_urgency": False,
        "has_location": False,
        "detected_urgency": None,
        "detected_location": None,
        "material_confirmed": True,  # False if ambiguous material detected
        "material_raw": None,       # raw material text if ambiguous
        "color_raw": None,           # descriptive color (e.g., "белый")
        "color_structured": None,    # structured color (e.g., "RAL 9010")
        "surface_finish_raw": None,  # raw finish (e.g., "матовый")
        "flags": {
            "material_question": False,
            "technical_advice_requested": False,
            "discount_request": False,
            "manager_review_required": False,
        },
        "missing_fields": [],
    }

    # --- Detect sizes ---
    items = _extract_sizes(text)
    if items:
        result["items"] = items
        result["has_sizes"] = True
        result["has_quantity"] = any(it.get("quantity", 1) > 1 for it in items)

    # --- Detect material (with ambiguity check) ---
    material_info = _extract_material_v2(text_lower)
    if material_info:
        result["has_material"] = True
        result["material_raw"] = material_info["raw"]
        result["material_confirmed"] = material_info["confirmed"]
        for item in result["items"]:
            item["material"] = material_info["raw"]
            item["material_confirmed"] = material_info["confirmed"]
        if not material_info["confirmed"]:
            result["flags"]["material_question"] = True

    # --- Detect color (raw vs structured) ---
    color_info = _extract_color_v2(text)
    if color_info:
        result["has_color"] = True
        result["color_raw"] = color_info.get("raw")
        result["color_structured"] = color_info.get("structured")
        result["color_scheme"] = color_info.get("scheme")
        result["surface_finish_raw"] = color_info.get("finish")
        for item in result["items"]:
            item["color"] = color_info.get("raw") or color_info.get("structured")
            item["color_raw"] = color_info.get("raw")
            item["color_structured"] = color_info.get("structured")
            item["finish"] = color_info.get("finish")

    # --- Detect urgency ---
    urgency = _extract_urgency(text_lower)
    if urgency:
        result["has_urgency"] = True
        result["detected_urgency"] = urgency

    # --- Detect discount request ---
    if _has_discount_request(text_lower):
        result["flags"]["discount_request"] = True

    # --- Detect technical advice request ---
    if _has_technical_question(text_lower):
        result["flags"]["technical_advice_requested"] = True
        result["flags"]["manager_review_required"] = True

    # --- Detect missing specifications (disputed, not technical advice) ---
    if _has_missing_spec(text_lower):
        result["flags"]["disputed_order_field"] = True
        result["flags"]["manager_review_required"] = True

    # --- Detect deadline question ---
    if _has_deadline_question(text_lower):
        result["flags"]["manager_review_required"] = True

    # --- Detect location ---
    location = _extract_location(text)
    if location:
        result["has_location"] = True
        result["detected_location"] = location

    # --- Determine missing fields ---
    if not result["has_sizes"]:
        result["missing_fields"].append("sizes")
    if not result["has_material"]:
        result["missing_fields"].append("material")
    elif not result["material_confirmed"]:
        result["missing_fields"].append("material_clarification")
    if not result["has_color"]:
        result["missing_fields"].append("color")

    return result


# ---------------------------------------------------------------------------
# 2. build_intake_card(text) -> dict
# ---------------------------------------------------------------------------


def build_intake_card(text: str, client_name: str = "", client_id: str = "") -> Dict[str, Any]:
    """Build a full Intake Card from a client message."""
    analysis = analyze_client_message(text)

    card: Dict[str, Any] = {
        "intake_id": "",
        "created_at": "",
        "status": "needs_more_info",
        "client": {
            "name": client_name,
            "telegram_id": client_id,
            "location": analysis.get("detected_location", ""),
        },
        "items": analysis.get("items", []),
        "material": {
            "raw": analysis.get("material_raw"),
            "confirmed": analysis.get("material_confirmed", True),
        },
        "color": {
            "raw": analysis.get("color_raw"),
            "structured": analysis.get("color_structured"),
        },
        "surface_finish_raw": analysis.get("surface_finish_raw"),
        "urgency": {
            "requested": analysis.get("detected_urgency", ""),
            "deadline_requested": "",
        },
        "extra": {
            "special_requirements": "",
            "delivery_needed": False,
            "packaging_needed": False,
            "notes": "",
        },
        "flags": dict(analysis["flags"]),
        "dialogue": {
            "messages_received": 1,
            "questions_asked": 0,
            "raw_summary": text[:200],
        },
    }

    # Determine status
    needs_more = (
        not analysis["has_sizes"]
        or not analysis["has_material"]
        or not analysis["has_color"]
        or not analysis.get("material_confirmed", True)
    )
    if needs_more:
        card["status"] = "needs_more_info"
    else:
        card["status"] = "ready_for_review"

    return card


# ---------------------------------------------------------------------------
# 3. suggest_questions(card) -> list[str]
# ---------------------------------------------------------------------------


def suggest_questions(card: Dict[str, Any]) -> List[str]:
    """Suggest clarifying questions based on what's missing."""
    questions: List[str] = []
    items = card.get("items", [])
    client = card.get("client", {})
    material_info = card.get("material", {})

    # Block 1: Sizes
    if not items:
        questions.append(
            "Подскажите размеры: высоту и ширину в миллиметрах. Например: 1000 400."
        )

    # Block 2: Material (check ambiguity)
    has_material = any(it.get("material") for it in items)
    is_confirmed = material_info.get("confirmed", True)
    if not has_material:
        questions.append(
            "Какой материал? МДФ, дерево (массив/шпон), металл, пластик, другое?"
        )
        questions.append("Материал уже есть у вас или нужна закупка?")
    elif not is_confirmed:
        questions.append(
            "Вы написали «дерево». Уточните: это массив, шпон или МДФ под дерево?"
        )
        questions.append("Материал уже есть у вас или нужна закупка?")

    # Block 3: Color
    has_color = any(it.get("color") for it in items)
    if not has_color:
        questions.append(
            "Какой цвет? Если знаете номер RAL — напишите. Если нет — опишите словами."
        )
    has_finish = any(it.get("finish") for it in items)
    if not has_finish:
        questions.append("Матовый или глянцевый?")
    questions.append("Нужна ли грунтовка перед покраской?")

    # Block 4: Urgency
    if not card.get("urgency", {}).get("requested"):
        questions.append("Когда вам нужно? Срочно или в обычном порядке?")

    # Block 5: Contacts
    if not client.get("name"):
        questions.append("Как к вам обращаться?")
    if not client.get("location"):
        questions.append("Ваш город? (для понимания доставки)")

    # Block 6: Extra
    questions.append(
        "Есть ли что-то ещё, что важно знать? Особые требования, доставка, упаковка?"
    )

    # Return first relevant block
    if not items:
        return questions[:2]
    if not has_material or not is_confirmed:
        return [q for q in questions if "материал" in q.lower() or "уточните" in q.lower()][:2] or questions[2:4]
    if not has_color:
        return [q for q in questions if "цвет" in q.lower() or "ral" in q.lower()][:2] or questions[4:6]

    return questions


# ---------------------------------------------------------------------------
# 4. suggest_response(card) -> str
# ---------------------------------------------------------------------------


def suggest_response(card: Dict[str, Any]) -> str:
    """Suggest what the agent should say next."""
    status = card.get("status", "needs_more_info")
    flags = card.get("flags", {})
    items = card.get("items", [])

    if flags.get("technical_advice_requested"):
        return "Я передал ваш вопрос менеджеру. С вами свяжутся. А пока — давайте уточним остальные детали заказа."

    if flags.get("discount_request"):
        return "Итоговую стоимость и возможные условия подтвердит менеджер после уточнения заказа. Я зафиксировал ваш вопрос."

    if status == "ready_for_review" and items:
        lines = ["Проверьте, пожалуйста, всё верно?\n"]
        for i, item in enumerate(items):
            h = item.get("height_mm", "?")
            w = item.get("width_mm", "?")
            q = item.get("quantity", 1)
            mat = item.get("material", "?")
            col = item.get("color", "?")
            fin = item.get("finish", "")
            line = f"  {i+1}. {h}×{w} мм, {q} шт, {mat}, {col}"
            if fin:
                line += f", {fin}"
            lines.append(line)
        lines.append("\nЕсли всё верно — напишите «да», и я передам заказ в расчёт.")
        return "\n".join(lines)

    if status == "needs_more_info":
        questions = suggest_questions(card)
        if questions:
            return "\n".join(questions[:3])
        return "Чтобы помочь с заказом, уточните, пожалуйста, размеры и материал."

    return "Я помогу оформить заказ на покраску. Напишите, пожалуйста, что нужно покрасить: размеры, материал, цвет."


# ---------------------------------------------------------------------------
# 5. determine_handoff_status(card) -> dict
# ---------------------------------------------------------------------------


def determine_handoff_status(card: Dict[str, Any]) -> Dict[str, Any]:
    """Determine whether the Intake Card is ready for Malyarka Agent.

    Stricter rules (edge-case hardened):
    - discount_request → blocks handoff
    - technical_advice_requested → blocks handoff
    - manager_review_required → blocks handoff
    - material not confirmed → blocks handoff
    """
    status = card.get("status", "")
    flags = card.get("flags", {})
    items = card.get("items", [])
    material_info = card.get("material", {})

    result: Dict[str, Any] = {
        "ready_for_malyarka_agent": False,
        "needs_clarification": False,
        "needs_manager_review": False,
        "reason": "",
        "blockers": [],
    }

    # --- Manager review blockers ---
    if flags.get("manager_review_required") or flags.get("technical_advice_requested"):
        result["needs_manager_review"] = True
        result["blockers"].append("manager_review_required")

    if flags.get("discount_request"):
        result["needs_manager_review"] = True
        if "discount_request" not in str(result["blockers"]):
            result["blockers"].append("discount_request — менеджер должен подтвердить условия")

    # --- Material ambiguity ---
    if not material_info.get("confirmed", True):
        result["needs_clarification"] = True
        result["blockers"].append("material_ambiguous — уточнить тип материала")

    # --- Data completeness ---
    if not items:
        result["needs_clarification"] = True
        result["blockers"].append("no_items")
        result["reason"] = "Нет размеров — нужны уточнения"
        return result

    for item in items:
        if not item.get("height_mm") or not item.get("width_mm"):
            result["needs_clarification"] = True
            result["blockers"].append("incomplete_sizes")
            result["reason"] = "Не все размеры указаны"
            return result
        if not item.get("material"):
            result["needs_clarification"] = True
            result["blockers"].append("missing_material")
            result["reason"] = "Не указан материал"
            return result
        if not item.get("color"):
            result["needs_clarification"] = True
            result["blockers"].append("missing_color")
            result["reason"] = "Не указан цвет"
            return result

    # Status check
    if status != "ready_for_review":
        result["needs_clarification"] = True
        result["reason"] = f"Статус: {status} — требуется подтверждение клиента"
        return result

    # All checks passed — ready for Malyarka
    if not result["blockers"]:
        result["ready_for_malyarka_agent"] = True
        result["reason"] = "Готово к передаче в Malyarka Agent"
    else:
        result["reason"] = f"Блокировано: {', '.join(result['blockers'])}"

    return result


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _extract_sizes(text: str) -> List[Dict[str, Any]]:
    """Extract size items from text."""
    text_clean = RAL_PATTERN.sub(" ", text)
    items: List[Dict[str, Any]] = []
    for match in SIZE_PATTERN.finditer(text_clean):
        groups = match.groups()
        if groups[0] and groups[1]:
            h, w = int(groups[0]), int(groups[1])
            q = int(groups[2]) if groups[2] else 1
        elif groups[3] and groups[4]:
            h, w = int(groups[3]), int(groups[4])
            q = int(groups[5]) if groups[5] else 1
        else:
            continue
        if h > 0 and w > 0 and q > 0:
            items.append({
                "height_mm": h, "width_mm": w, "quantity": q,
                "material": "", "material_confirmed": True,
                "color": "", "color_raw": None, "color_structured": None,
                "finish": "", "surface_ready": False,
                "needs_primer": False, "notes": "",
            })
    return items


def _extract_material_v2(text_lower: str) -> Optional[Dict[str, Any]]:
    """Extract material with ambiguity detection.

    Returns {"raw": str, "confirmed": bool} or None.
    """
    # Check ambiguous first (more general)
    for keyword in AMBIGUOUS_MATERIALS:
        if keyword in text_lower:
            return {"raw": "дерево", "confirmed": False}

    # Check confirmed (more specific)
    material_map = [
        ("мдф", "МДФ"), ("mdf", "МДФ"),
        ("лдсп", "ЛДСП"), ("дсп", "ДСП"), ("двп", "ДВП"),
        ("фанера", "фанера"), ("фанеры", "фанера"),
        ("шпон", "шпон"), ("шпона", "шпон"),
        ("массив", "массив"),
        ("акрил", "акрил"), ("акрила", "акрил"),
        ("стекло", "стекло"), ("стекла", "стекло"),
        ("металл", "металл"), ("металла", "металл"),
        ("пластик", "пластик"), ("пластика", "пластик"),
    ]
    for keyword, value in material_map:
        if keyword in text_lower:
            return {"raw": value, "confirmed": True}
    return None


def _extract_color_v2(text: str) -> Optional[Dict[str, str]]:
    """Extract color with raw/structured distinction."""
    result: Dict[str, str] = {}
    text_lower = text.lower()

    # Try RAL → structured
    ral_match = RAL_PATTERN.search(text)
    if ral_match:
        result["structured"] = f"RAL {ral_match.group(1)}"
        result["raw"] = result["structured"]

    # Try NCS → structured
    ncs_match = NCS_PATTERN.search(text)
    if ncs_match and "structured" not in result:
        result["structured"] = f"NCS {ncs_match.group(1)}"
        result["raw"] = ncs_match.group(0)  # Full original: "NCS S4050-R"
        result["normalized"] = f"NCS {ncs_match.group(1).replace(' ', '')}"
        result["scheme"] = "NCS"

    # If no structured, look for descriptive color
    if "raw" not in result:
        color_map = [
            ("белый", "белый"), ("белого", "белый"), ("белая", "белый"), ("белые", "белый"),
            ("чёрный", "чёрный"), ("черный", "чёрный"),
            ("серый", "серый"),
            ("коричневый", "коричневый"),
            ("красный", "красный"),
            ("синий", "синий"),
            ("зелёный", "зелёный"), ("зеленый", "зелёный"),
            ("жёлтый", "жёлтый"), ("желтый", "жёлтый"),
            ("бежевый", "бежевый"),
            ("кофе с молоком", "кофе с молоком"),
            ("венге", "венге"),
            ("дуб", "дуб"),
            ("орех", "орех"),
        ]
        for keyword, value in color_map:
            if keyword in text_lower:
                result["raw"] = value
                break

    # Finish — raw only, never invent
    if any(w in text_lower for w in ["матовый", "мат", "матов"]):
        result["finish"] = "матовый"
    elif any(w in text_lower for w in ["глянцевый", "глянец", "гланц"]):
        result["finish"] = "глянцевый"

    return result if result else None


def _extract_urgency(text_lower: str) -> Optional[str]:
    if "очень срочно" in text_lower or "вчера" in text_lower or "горит" in text_lower:
        return "очень срочно"
    if any(w in text_lower for w in ["срочно", "срочный", "как можно"]):
        return "срочно"
    return None


def _extract_location(text: str) -> Optional[str]:
    """Extract location (city) from text. Supports extended city list."""
    known_locations = [
        "москва", "санкт-петербург", "спб", "питер",
        "новосибирск", "екатеринбург", "казань",
        "нижний новгород", "челябинск", "самара",
        "омск", "ростов", "уфа", "красноярск",
        "воронеж", "пермь", "волгоград", "краснодар",
        "алматы", "алмата", "астана", "нур-султан",
        "минск", "киев",
    ]
    location_map = {
        "спб": "Санкт-Петербург",
        "питер": "Санкт-Петербург",
        "санкт-петербург": "Санкт-Петербург",
        "алматы": "Алматы",
        "алмата": "Алматы",
        "астана": "Астана",
        "нур-султан": "Астана",
        "москва": "Москва",
    }
    text_lower = text.lower()
    for loc in known_locations:
        if loc in text_lower:
            if loc in location_map:
                return location_map[loc]
            if len(loc) <= 4:
                return loc.upper()
            return loc.capitalize()
    return None


def _has_discount_request(text_lower: str) -> bool:
    return any(w in text_lower for w in DISCOUNT_WORDS)


def _has_technical_question(text_lower: str) -> bool:
    return any(w in text_lower for w in TECHNICAL_QUESTION_WORDS)


def _has_missing_spec(text_lower: str) -> bool:
    """Detect missing specifications (e.g. milling type not specified)."""
    return any(w in text_lower for w in MISSING_SPEC_WORDS)


def _has_deadline_question(text_lower: str) -> bool:
    return any(w in text_lower for w in DEADLINE_QUESTION_WORDS)
